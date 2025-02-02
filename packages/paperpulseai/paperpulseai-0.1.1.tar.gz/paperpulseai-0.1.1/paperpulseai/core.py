#!/usr/bin/env python3

import click
import requests
import pandas as pd
from datetime import datetime, timedelta
from Bio import Entrez
from rich.console import Console
from rich.table import Table
from pathlib import Path
import time
import json
from typing import List, Dict, Any, Tuple
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import numpy as np
import re
from urllib.parse import quote, urljoin
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import concurrent.futures
from queue import Queue
from threading import Lock
from functools import partial
import backoff
import tenacity
from reportlab.lib import colors
from reportlab.lib.pagesizes import A5, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table as RLTable, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import hashlib
import json
from pathlib import Path
import diskcache
import PyPDF2
from bs4 import BeautifulSoup
from deepseek_model import model as deepseek_model

# Global variables for thread safety
progress_lock = Lock()
papers_lock = Lock()
entrez_lock = Lock()  # Add lock for Entrez API calls

# Rate limiting settings
ENTREZ_RATE_LIMIT = 0.34  # seconds between requests (3 requests per second)
MAX_RETRIES = 5
RETRY_DELAY = 1.0
BATCH_SIZE = 100  # Increased batch size for better throughput
MAX_WORKERS = min(32, os.cpu_count() * 4)  # Optimize worker count

# Create connection pool for requests
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=MAX_WORKERS,
    pool_maxsize=MAX_WORKERS,
    max_retries=MAX_RETRIES,
    pool_block=False
)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Initialize cache
cache = diskcache.Cache('.cache')

# Add Sci-Hub URL
SCIHUB_URL = "https://sci-hub.se"  # This can be updated if the domain changes

# Retry decorator for Entrez API calls
@tenacity.retry(
    stop=tenacity.stop_after_attempt(MAX_RETRIES),
    wait=tenacity.wait_exponential(multiplier=RETRY_DELAY, min=RETRY_DELAY, max=10),
    retry=tenacity.retry_if_exception_type((Exception)),
    before_sleep=lambda retry_state: click.echo(f"Retrying after error: {retry_state.outcome.exception()}")
)
def safe_entrez_fetch(db: str, **kwargs) -> Any:
    """Thread-safe Entrez fetch with rate limiting and retries."""
    with entrez_lock:
        time.sleep(ENTREZ_RATE_LIMIT)  # Rate limiting
        handle = Entrez.efetch(db=db, **kwargs)
        try:
            result = Entrez.read(handle)
            return result
        finally:
            handle.close()

@tenacity.retry(
    stop=tenacity.stop_after_attempt(MAX_RETRIES),
    wait=tenacity.wait_exponential(multiplier=RETRY_DELAY, min=RETRY_DELAY, max=10),
    retry=tenacity.retry_if_exception_type((Exception)),
    before_sleep=lambda retry_state: click.echo(f"Retrying after error: {retry_state.outcome.exception()}")
)
def safe_entrez_search(db: str, **kwargs) -> Any:
    """Thread-safe Entrez search with rate limiting and retries."""
    with entrez_lock:
        time.sleep(ENTREZ_RATE_LIMIT)  # Rate limiting
        handle = Entrez.esearch(db=db, **kwargs)
        try:
            result = Entrez.read(handle)
            return result
        finally:
            handle.close()

def get_paper_url(doi: str, pmid: str) -> str:
    """Get the paper URL from PubMed Central or Sci-Hub."""
    # Try PubMed Central first
    if pmid:
        try:
            handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid)
            record = Entrez.read(handle)
            handle.close()
            
            if record[0]["LinkSetDb"]:
                pmc_id = record[0]["LinkSetDb"][0]["Link"][0]["Id"]
                return f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf"
        except Exception as e:
            click.echo(f"Error checking PMC: {str(e)}", err=True)
    
    # Fallback to Sci-Hub if DOI is available
    if doi:
        return f"{SCIHUB_URL}/{doi}"
    
    return None

def group_similar_papers(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Group similar papers based on their abstracts and titles using DBSCAN clustering."""
    # Prepare text data for clustering
    texts = []
    for paper in papers:
        combined_text = f"{paper['title']} {paper['abstract']}"
        texts.append(combined_text)
    
    # Convert text to TF-IDF features
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(texts)
    
    # Perform clustering
    clustering = DBSCAN(eps=0.7, min_samples=2, metric='cosine')
    clusters = clustering.fit_predict(X)
    
    # Add cluster information to papers
    for paper, cluster_id in zip(papers, clusters):
        paper['cluster'] = int(cluster_id)
    
    # Sort papers by cluster for better organization
    papers.sort(key=lambda x: (x['cluster'], x['date']), reverse=True)
    
    return papers

def extract_keywords_from_query(query: str) -> List[str]:
    """Extract meaningful keywords from a PubMed search query."""
    # Remove common operators and parentheses
    cleaned = query.replace('AND', ' ').replace('OR', ' ').replace('(', ' ').replace(')', ' ')
    
    # Split into words and clean up
    words = cleaned.lower().split()
    
    # Remove common words and operators
    stopwords = {'the', 'a', 'an', 'and', 'or', 'not', 'in', 'on', 'at', 'to', 'for', 'of'}
    keywords = [word for word in words if word not in stopwords]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    
    return unique_keywords

def calculate_relevance_scores(papers: List[Dict[str, Any]], search_keywords: List[str]) -> List[Dict[str, Any]]:
    """Calculate relevance scores for papers using TF-IDF with dynamic keywords."""
    if not papers:
        return []
    
    if not search_keywords:
        click.echo("Warning: No keywords provided for scoring. Using default scoring.", err=True)
        search_keywords = [
            'tuberculosis', 'mycobacterium', 'tb', 'mtb', 'diagnostic',
            'detection', 'screening', 'testing', 'novel', 'innovative',
            'method', 'technique', 'approach', 'assay', 'test'
        ]
    
    # Prepare documents for TF-IDF
    documents = []
    for paper in papers:
        text = f"{paper['title']} {paper['abstract']}".lower()
        documents.append(text)
    
    # Calculate TF-IDF
    vectorizer = TfidfVectorizer(vocabulary=search_keywords)
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calculate relevance scores
    for i, paper in enumerate(papers):
        # Get the TF-IDF scores for this document
        scores = tfidf_matrix[i].toarray()[0]
        
        # Calculate weighted score (title matches count more)
        title_score = sum(paper['title'].lower().count(kw) * 2 for kw in search_keywords)
        tfidf_score = np.sum(scores)
        
        # Combine scores
        relevance_score = tfidf_score + title_score
        paper['relevance_score'] = float(relevance_score)
        
        # Add matched keywords for reference
        matched_keywords = [kw for kw in search_keywords 
                          if kw in paper['title'].lower() or kw in paper['abstract'].lower()]
        paper['matched_keywords'] = matched_keywords
    
    # Sort papers by relevance score
    papers.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    return papers

def generate_local_summary(text: str, num_sentences: int = 3) -> str:
    """Generate a local summary using extractive summarization."""
    # Split text into sentences
    sentences = text.replace('\n', ' ').split('. ')
    if not sentences:
        return text
    
    # Calculate sentence scores based on word importance
    word_freq = {}
    for sentence in sentences:
        for word in sentence.lower().split():
            if word not in ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of']:
                word_freq[word] = word_freq.get(word, 0) + 1
    
    # Score sentences based on word frequency
    sentence_scores = []
    for sentence in sentences:
        score = sum(word_freq.get(word.lower(), 0) for word in sentence.split())
        sentence_scores.append((score, sentence))
    
    # Get top sentences
    top_sentences = sorted(sentence_scores, reverse=True)[:num_sentences]
    top_sentences = sorted([(i, s[1]) for i, s in enumerate(top_sentences)], key=lambda x: x[0])
    
    # Format summary with bullet points
    summary = "\n• " + "\n• ".join(s[1] for s in top_sentences)
    return summary

def extract_diagnostic_metrics(abstract: str) -> Dict[str, str]:
    """Extract diagnostic metrics from the abstract."""
    metrics = {
        'sample_type': 'Not specified',
        'sample_size': 'Not specified',
        'main_test': 'Not specified',
        'comparator_test': 'Not specified',
        'technique': 'Not specified',
        'accuracy': 'Not specified',
        'sensitivity': 'Not specified',
        'specificity': 'Not specified'
    }
    
    # Convert to lowercase for easier matching
    text = abstract.lower()
    
    # Sample type patterns
    sample_types = ['sputum', 'blood', 'urine', 'csf', 'tissue', 'plasma', 'serum']
    for sample in sample_types:
        if sample in text:
            metrics['sample_type'] = sample
            break
    
    # Sample size pattern
    sample_patterns = [
        r'(\d+)\s+(?:samples|specimens|patients|participants|subjects)',
        r'n\s*=\s*(\d+)',
        r'total\s+of\s+(\d+)\s+(?:samples|specimens|patients|participants|subjects)'
    ]
    for pattern in sample_patterns:
        match = re.search(pattern, text)
        if match:
            metrics['sample_size'] = match.group(1)
            break
    
    # Accuracy metrics patterns
    accuracy_pattern = r'accuracy.*?(\d+\.?\d*%|\d+\.?\d*)'
    sensitivity_pattern = r'sensitivity.*?(\d+\.?\d*%|\d+\.?\d*)'
    specificity_pattern = r'specificity.*?(\d+\.?\d*%|\d+\.?\d*)'
    
    for pattern, key in [(accuracy_pattern, 'accuracy'),
                        (sensitivity_pattern, 'sensitivity'),
                        (specificity_pattern, 'specificity')]:
        match = re.search(pattern, text)
        if match:
            metrics[key] = match.group(1)
    
    # Technique patterns
    techniques = {
        'pcr': 'PCR',
        'naat': 'NAAT',
        'lamp': 'LAMP',
        'crispr': 'CRISPR',
        'culture': 'Culture',
        'microscopy': 'Microscopy',
        'sequencing': 'Sequencing',
        'microarray': 'Microarray'
    }
    
    for tech_key, tech_name in techniques.items():
        if tech_key in text:
            metrics['technique'] = tech_name
            break
    
    # Extract main test and comparator
    test_patterns = [
        r'compared?\s+(?:to|with)\s+([^\.]+)',
        r'against\s+([^\.]+)',
        r'versus\s+([^\.]+)'
    ]
    
    for pattern in test_patterns:
        match = re.search(pattern, text)
        if match:
            comparator = match.group(1).strip()
            metrics['comparator_test'] = comparator
            # Try to find the main test in the preceding text
            preceding_text = text[:match.start()].split('.')[-1]
            if preceding_text:
                metrics['main_test'] = preceding_text.strip()
            break
    
    return metrics

def generate_structured_summary(abstract: str, title: str, full_text: str = None) -> Dict[str, str]:
    """Generate a structured summary using DeepSeek with caching."""
    if not abstract and not full_text:
        return None
    
    # Use full text if available, otherwise use abstract
    text_to_summarize = full_text if full_text else abstract
    summary_source = "Full Paper" if full_text else "Abstract"
    
    # Generate cache key based on the text being used
    cache_key = f"structured_summary_{hashlib.md5(text_to_summarize.encode()).hexdigest()}"
    
    # Try to get from cache
    cached_summary = cache.get(cache_key)
    if cached_summary is not None:
        cached_summary['summary_source'] = summary_source  # Add source to cached result
        return cached_summary
    
    try:
        # Generate summary using DeepSeek
        sections = deepseek_model.generate_summary(title, text_to_summarize)
        
        if sections:
            # Add source information
            sections['summary_source'] = summary_source
            
            # Cache the result
            cache.set(cache_key, sections, expire=7 * 24 * 60 * 60)  # Cache for 7 days
            return sections
        
        return None
        
    except Exception as e:
        click.echo(f"Error generating summary: {str(e)}", err=True)
        return None

def parse_summary_sections(summary_text: str) -> Dict[str, str]:
    """Parse the sections from the summary text."""
    sections = {
        'objective': '',
        'methods': '',
        'results': '',
        'conclusions': '',
        'limitations': ''
    }
    
    current_section = None
    current_text = []
    
    for line in summary_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        lower_line = line.lower()
        for section in sections:
            if f"{section}:" in lower_line:
                if current_section and current_text:
                    sections[current_section] = ' '.join(current_text)
                current_section = section
                current_text = [line.split(':', 1)[1].strip()]
                break
        else:
            if current_section:
                current_text.append(line)
    
    # Add the last section
    if current_section and current_text:
        sections[current_section] = ' '.join(current_text)
    
    # Fill in empty sections
    for key in sections:
        if not sections[key]:
            sections[key] = 'Not available in abstract'
    
    return sections

def search_pubmed(query: str, days: int = 30, use_ai: bool = True, progress=None, main_progress=None) -> List[Dict[str, Any]]:
    """Search PubMed for recent papers matching the query."""
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Format dates for PubMed
    date_range = f"{start_date.strftime('%Y/%m/%d')}:{end_date.strftime('%Y/%m/%d')}[Date - Publication]"
    
    # Perform the search
    search_query = f"({query}) AND {date_range}"
    
    # First get total count
    record = safe_entrez_search(db="pubmed", term=search_query, retmax=0)
    total_count = int(record["Count"])
    
    if total_count == 0:
        if progress:
            with progress_lock:
                progress.advance(1)
        return []
    
    # Create a task for this query's papers
    papers_task = None
    if main_progress:
        papers_task = main_progress.add_task(
            f"[blue]Processing papers",
            total=total_count
        )
    
    # Extract keywords from this query for scoring
    query_keywords = extract_keywords_from_query(query)
    
    # Fetch all results in optimized batches
    papers = []
    
    # Process in larger batches for better throughput
    for start in range(0, total_count, BATCH_SIZE):
        try:
            # Get batch of IDs
            record = safe_entrez_search(
                db="pubmed",
                term=search_query,
                retstart=start,
                retmax=BATCH_SIZE
            )
            id_list = record["IdList"]
            
            # Split into sub-batches for parallel processing
            sub_batches = [id_list[i:i + 20] for i in range(0, len(id_list), 20)]
            
            # Process sub-batches in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = []
                for sub_batch in sub_batches:
                    future = executor.submit(process_paper_batch, sub_batch, len(sub_batch), main_progress, papers_task)
                    futures.append(future)
                
                # Collect results as they complete
                for future in concurrent.futures.as_completed(futures):
                    try:
                        batch_papers = future.result()
                        with papers_lock:
                            papers.extend(batch_papers)
                    except Exception as e:
                        continue
            
        except Exception as e:
            continue
    
    if progress:
        with progress_lock:
            progress.advance(1)
    
    if not papers:
        return []
    
    # Score and filter papers using keywords from this specific query
    scored_papers = calculate_relevance_scores(papers, query_keywords)
    
    return scored_papers

def process_paper_batch(id_list: List[str], batch_size: int, progress=None, task=None) -> List[Dict[str, Any]]:
    """Process a batch of paper IDs with proper rate limiting."""
    papers = []
    
    try:
        # Fetch all papers in batch with a single API call
        records = safe_entrez_fetch(db="pubmed", id=",".join(id_list), rettype="xml", retmode="xml")
        
        if 'PubmedArticle' in records:
            for article in records['PubmedArticle']:
                try:
                    paper = extract_paper_details(article)
                    if paper:
                        papers.append(paper)
                    if progress and task:
                        with progress_lock:
                            progress.advance(task, 1)
                except Exception as e:
                    if progress and task:
                        with progress_lock:
                            progress.advance(task, 1)
                    continue
    except Exception as e:
        # Fallback to individual processing if batch fails
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(5, batch_size)) as executor:
            futures = []
            for pmid in id_list:
                future = executor.submit(fetch_paper_details, pmid)
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    paper = future.result()
                    if paper:
                        papers.append(paper)
                    if progress and task:
                        with progress_lock:
                            progress.advance(task, 1)
                except Exception as e:
                    if progress and task:
                        with progress_lock:
                            progress.advance(task, 1)
    
    return papers

def extract_paper_details(article: Dict[str, Any]) -> Dict[str, Any]:
    """Extract paper details from PubMed article data."""
    try:
        medline_citation = article['MedlineCitation']
        article_data = medline_citation['Article']
        pmid = str(medline_citation['PMID'])
        
        # Extract abstract
        abstract_text = ""
        if 'Abstract' in article_data:
            abstract_parts = article_data['Abstract'].get('AbstractText', [])
            if abstract_parts:
                if isinstance(abstract_parts, list):
                    abstract_text = ' '.join(str(part) for part in abstract_parts)
                else:
                    abstract_text = str(abstract_parts)
        
        # Extract DOI
        doi = None
        if 'ArticleIdList' in article['PubmedData']:
            for id_obj in article['PubmedData']['ArticleIdList']:
                if id_obj.attributes.get('IdType') == 'doi':
                    doi = str(id_obj)
                    break
        
        # Extract year
        year = ''
        if 'PubDate' in article_data['Journal']['JournalIssue']:
            pub_date = article_data['Journal']['JournalIssue']['PubDate']
            year = pub_date.get('Year', '')
        
        # Extract metrics
        metrics = extract_diagnostic_metrics(abstract_text)
        
        # Generate structured summary
        title = str(article_data['ArticleTitle'])
        structured_summary = generate_structured_summary(abstract_text, title)
        
        paper_details = {
            'title': title,
            'abstract': abstract_text,
            'doi': doi,
            'date': year,
            'pmid': pmid,
            'local_summary': generate_local_summary(abstract_text) if abstract_text else "No abstract available",
            'sample_type': metrics['sample_type'],
            'sample_size': metrics['sample_size'],
            'main_test': metrics['main_test'],
            'comparator_test': metrics['comparator_test'],
            'technique': metrics['technique'],
            'accuracy': metrics['accuracy'],
            'sensitivity': metrics['sensitivity'],
            'specificity': metrics['specificity']
        }
        
        # Add structured summary and source if available
        if structured_summary:
            paper_details['structured_summary'] = structured_summary
            paper_details['summary_source'] = structured_summary.get('summary_source', 'Abstract')
        
        return paper_details
    except Exception as e:
        return None

@tenacity.retry(
    stop=tenacity.stop_after_attempt(MAX_RETRIES),
    wait=tenacity.wait_exponential(multiplier=RETRY_DELAY, min=RETRY_DELAY, max=10),
    retry=tenacity.retry_if_exception_type((requests.exceptions.RequestException, Exception)),
    before_sleep=lambda retry_state: click.echo(f"Retrying download after error: {retry_state.outcome.exception()}")
)
def safe_download_request(url: str, stream: bool = True) -> requests.Response:
    """Make a download request with rate limiting and retries."""
    with entrez_lock:  # Use the same lock for rate limiting
        time.sleep(ENTREZ_RATE_LIMIT)  # Use the same rate limit as Entrez
        response = requests.get(url, stream=stream)
        response.raise_for_status()  # Raise exception for bad status codes
        return response

def download_paper(doi: str, pmid: str, title: str, output_dir: str) -> str:
    """Download paper using PubMed Central first, then Sci-Hub as fallback."""
    if not doi and not pmid:
        return "No identifiers available"
    
    # Create sanitized filename
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"{safe_title[:100]}_{pmid or doi}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    if os.path.exists(output_path):
        return "Already downloaded"
    
    # Try PubMed Central first
    if pmid:
        try:
            handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid)
            record = Entrez.read(handle)
            handle.close()
            
            if record[0]["LinkSetDb"]:
                pmc_id = record[0]["LinkSetDb"][0]["Link"][0]["Id"]
                url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf"
                
                try:
                    response = safe_download_request(url)
                    if 'application/pdf' in response.headers.get('content-type', '').lower():
                        with open(output_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        return "Downloaded via PMC"
                except Exception as e:
                    click.echo(f"PMC download failed: {str(e)}", err=True)
        except Exception as e:
            click.echo(f"PMC lookup failed: {str(e)}", err=True)
    
    # Try Sci-Hub if DOI is available
    if doi:
        try:
            url = f"{SCIHUB_URL}/{doi}"
            try:
                response = safe_download_request(url, stream=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    pdf_iframe = soup.find('iframe', id='pdf')
                    
                    if pdf_iframe and pdf_iframe.get('src'):
                        pdf_url = pdf_iframe['src']
                        if not pdf_url.startswith('http'):
                            pdf_url = 'https:' + pdf_url if pdf_url.startswith('//') else SCIHUB_URL + pdf_url
                        
                        try:
                            pdf_response = safe_download_request(pdf_url)
                            if 'application/pdf' in pdf_response.headers.get('content-type', '').lower():
                                with open(output_path, 'wb') as f:
                                    for chunk in pdf_response.iter_content(chunk_size=8192):
                                        f.write(chunk)
                                return "Downloaded via Sci-Hub"
                        except Exception as e:
                            click.echo(f"Sci-Hub PDF download failed: {str(e)}", err=True)
            except Exception as e:
                click.echo(f"Sci-Hub page access failed: {str(e)}", err=True)
        except Exception as e:
            click.echo(f"Sci-Hub download failed: {str(e)}", err=True)
    
    return "Download failed"

def parallel_download_papers(papers: List[Dict[str, Any]], download_dir: str, progress=None, task=None) -> List[str]:
    """Download papers in parallel."""
    download_statuses = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, len(papers))) as executor:
        futures = []
        for paper in papers:
            future = executor.submit(
                download_paper,
                paper.get('doi'),
                paper.get('pmid'),
                paper['title'],
                download_dir
            )
            futures.append(future)
        
        for future in concurrent.futures.as_completed(futures):
            try:
                status = future.result()
                download_statuses.append(status)
                if progress and task:
                    with progress_lock:
                        progress.advance(task)
            except Exception as e:
                download_statuses.append("Download failed")
                if progress and task:
                    with progress_lock:
                        progress.advance(task)
    
    return download_statuses

def download_single_paper(doi: str, pmid: str, title: str, download_dir: str, session: requests.Session) -> str:
    """Download a single paper."""
    try:
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title[:100]}_{pmid}.pdf"
        output_path = os.path.join(download_dir, filename)
        
        if os.path.exists(output_path):
            return "Already downloaded"
        
        # Try different download methods
        if download_from_pubmed_central(pmid, output_path):
            return "Downloaded via PMC"
        if download_from_doi(session, doi, output_path):
            return "Downloaded via DOI"
        if download_from_publisher(session, get_paper_url(doi, pmid), output_path):
            return "Downloaded via publisher"
        
        return "Download failed"
    except Exception as e:
        return f"Error: {str(e)}"

def parallel_generate_summaries(papers: List[Dict[str, Any]], use_ai: bool) -> List[Dict[str, Any]]:
    """Generate summaries in parallel with optimized batching."""
    if not use_ai:
        return papers
    
    # Group papers by whether they need AI processing
    need_processing = []
    for i, paper in enumerate(papers):
        if paper.get('abstract') and not paper.get('structured_summary'):
            # Check cache first
            cache_key = f"structured_summary_{hashlib.md5(paper['abstract'].encode()).hexdigest()}"
            cached_summary = cache.get(cache_key)
            if cached_summary is not None:
                paper['structured_summary'] = cached_summary
            else:
                need_processing.append((i, paper))
    
    if not need_processing:
        return papers
    
    # Process papers in optimized batches
    batch_size = 5  # Process 5 papers at a time to avoid rate limits
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i in range(0, len(need_processing), batch_size):
            batch = need_processing[i:i + batch_size]
            for idx, paper in batch:
                future = executor.submit(
                    generate_structured_summary_with_cache,
                    paper['abstract'],
                    paper['title']
                )
                futures.append((idx, future))
            
            # Small delay between batches to avoid rate limits
            if i + batch_size < len(need_processing):
                time.sleep(1)
        
        # Collect results
        for idx, future in futures:
            try:
                summary = future.result()
                if summary:
                    papers[idx]['structured_summary'] = summary
                    # Cache the result
                    cache_key = f"structured_summary_{hashlib.md5(papers[idx]['abstract'].encode()).hexdigest()}"
                    cache.set(cache_key, summary, expire=7 * 24 * 60 * 60)  # Cache for 7 days
            except Exception as e:
                continue
    
    return papers

def generate_structured_summary_with_cache(abstract: str, title: str) -> Dict[str, str]:
    """Generate a structured summary using DeepSeek with caching."""
    if not abstract:
        return None
    
    # Generate cache key
    cache_key = f"structured_summary_{hashlib.md5(abstract.encode()).hexdigest()}"
    
    # Try to get from cache
    cached_summary = cache.get(cache_key)
    if cached_summary is not None:
        return cached_summary
    
    try:
        # Generate summary using DeepSeek
        sections = deepseek_model.generate_summary(title, abstract)
        
        if sections:
            # Cache the result
            cache.set(cache_key, sections, expire=7 * 24 * 60 * 60)  # Cache for 7 days
            return sections
        
        return None
        
    except Exception as e:
        click.echo(f"Error generating summary: {str(e)}", err=True)
        return None

def sanitize_text(text: str) -> str:
    """Sanitize text by removing HTML/XML tags and converting special characters."""
    if not text:
        return ""
    
    try:
        # First try to balance any unclosed tags
        text = re.sub(r'<([^/][^>]*)(?<!/)>', r'<\1></\1>', text)
        
        # Remove any remaining HTML/XML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Convert special characters
        text = text.replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&amp;', '&').replace('&quot;', '"')
        text = text.replace('&apos;', "'")
        
        # Remove any remaining XML/HTML artifacts
        text = re.sub(r'</?\w+[^>]*>', '', text)  # Remove any remaining tags
        text = re.sub(r'&[^;]+;', '', text)  # Remove any remaining HTML entities
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        
        # Clean up any special characters that might cause issues
        text = ''.join(char for char in text if ord(char) < 128 or char.isspace())
        
        return text.strip()
    except Exception as e:
        # If anything goes wrong, return a maximally stripped version
        return ''.join(char for char in re.sub(r'<[^>]*>', '', str(text)) if ord(char) < 128 or char.isspace()).strip()

def save_summaries_to_pdf(papers: List[Dict[str, Any]], output_path: str):
    """Save structured summaries to a nicely formatted PDF."""
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A5),
            rightMargin=30,
            leftMargin=30,
            topMargin=20,
            bottomMargin=20
        )
        
        # Prepare styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.HexColor('#2E5C8A')
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=10,
            textColor=colors.HexColor('#4A4A4A')
        )
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=9,
            leading=11
        )
        cluster_style = ParagraphStyle(
            'ClusterHeader',
            parent=styles['Heading1'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#1B4F72'),
            backColor=colors.HexColor('#EBF5FB')
        )
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666')
        )
        source_style = ParagraphStyle(
            'SourceStyle',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#008000')  # Green color for source
        )
        
        # Build the document
        story = []
        
        # Group papers by cluster
        cluster_papers = {}
        for paper in papers:
            if not paper.get('structured_summary'):
                continue
            cluster = paper.get('cluster', -1)  # Default to -1 for papers without cluster
            if cluster not in cluster_papers:
                cluster_papers[cluster] = []
            cluster_papers[cluster].append(paper)
        
        # Sort clusters
        sorted_clusters = sorted(cluster_papers.keys())
        
        # Process each cluster
        for cluster in sorted_clusters:
            try:
                # Add cluster header with background
                cluster_label = "Unique Papers" if cluster < 0 else f"Group {cluster}"
                story.append(Paragraph(sanitize_text(cluster_label), cluster_style))
                
                # Sort papers in this cluster by date (most recent first)
                cluster_papers[cluster].sort(
                    key=lambda x: pd.to_datetime(x.get('date', '1900-01-01'), errors='coerce', format='mixed'),
                    reverse=True
                )
                
                # Add papers in this cluster
                for i, paper in enumerate(cluster_papers[cluster]):
                    try:
                        # Add page break before each paper (except the first paper after a cluster header)
                        if i > 0:
                            story.append(PageBreak())
                        
                        # Add paper title
                        clean_title = sanitize_text(paper['title'])
                        if clean_title:
                            story.append(Paragraph(clean_title, title_style))
                        
                        # Add date and identifiers in a single line
                        info_parts = []
                        if paper.get('date'):
                            info_parts.append(f"Date: {paper['date']}")
                        if paper.get('doi'):
                            clean_doi = sanitize_text(paper['doi'])
                            if clean_doi:
                                info_parts.append(f"DOI: {clean_doi}")
                        if paper.get('relevance_score'):
                            info_parts.append(f"Score: {paper['relevance_score']:.1f}")
                        
                        if info_parts:
                            story.append(Paragraph(" | ".join(info_parts), date_style))
                        
                        # Add summary source with proper fallbacks
                        summary_source = (
                            paper.get('summary_source') or  # First try direct source
                            paper.get('structured_summary', {}).get('summary_source') or  # Then try source in summary
                            ('Full Paper' if paper.get('full_text') else 'Abstract')  # Finally infer from content
                        )
                        if summary_source:
                            story.append(Paragraph(f"Summary Source: {summary_source}", source_style))
                        
                        story.append(Spacer(1, 0.1 * inch))
                        
                        summary = paper['structured_summary']
                        
                        # Create a table for the structured summary
                        data = []
                        sections = ['objective', 'methods', 'results', 'technical_details', 'conclusions', 'limitations']
                        for section in sections:
                            if section in summary and summary[section]:
                                # Capitalize first letter of section name
                                section_title = section.replace('_', ' ').capitalize()
                                content = summary[section]
                                if content != 'Not available in paper' and content != 'Not available in abstract':
                                    clean_content = sanitize_text(content)
                                    if clean_content:  # Only add if we have clean content
                                        data.append([
                                            Paragraph(sanitize_text(section_title), heading_style),
                                            Paragraph(clean_content, normal_style)
                                        ])
                        
                        if data:
                            # Create table with specific column widths
                            col_widths = [1.2 * inch, 5.8 * inch]  # Total should be less than A5 landscape width
                            table = RLTable(data, colWidths=col_widths)
                            
                            # Add table style
                            table.setStyle(TableStyle([
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
                                ('PADDING', (0, 0), (-1, -1), 6),
                                ('ROWSPLIT', (0, 0), (-1, -1), 'SPAN'),
                            ]))
                            
                            story.append(table)
                            story.append(Spacer(1, 0.2 * inch))
                        
                    except Exception as e:
                        click.echo(f"Warning: Skipped paper due to error: {str(e)}", err=True)
                        continue
                
                # Add a thicker separator between clusters if not the last cluster
                if cluster != sorted_clusters[-1]:
                    story.append(Spacer(1, 0.2 * inch))
                    story.append(HRFlowable(
                        width="100%",
                        thickness=2,
                        color=colors.HexColor('#2E86C1'),
                        spaceBefore=15,
                        spaceAfter=15
                    ))
                    story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                click.echo(f"Warning: Skipped cluster {cluster} due to error: {str(e)}", err=True)
                continue
        
        # Build the PDF
        doc.build(story)
    except Exception as e:
        click.echo(f"Error generating PDF: {str(e)}", err=True)
        raise

@click.group()
@click.option('--email', required=True, help="Email address for PubMed API access (required)")
def cli(email):
    """CureConnect: Track recent developments in TB research and diagnostic techniques."""
    # Configure email for Entrez
    Entrez.email = email

@cli.command()
@click.argument('excel_file', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), help='Output PDF path (default: input filename with _summaries.pdf)')
@click.option('--temp-file', type=click.Path(), default='.temp_papers.json', help='Temporary file with saved paper data')
@click.option('--min-score', type=float, default=0.0, help='Minimum relevance score for papers (typically ranges 1-20)')
def resume_pdf(excel_file: str, output: str, temp_file: str, min_score: float):
    """Resume PDF generation from a failed attempt using saved data."""
    if not output:
        output = os.path.splitext(excel_file)[0] + '_summaries.pdf'
    
    click.echo(f"Attempting to resume PDF generation...")
    
    try:
        # First try to load from temp file if it exists
        if os.path.exists(temp_file):
            click.echo(f"Found temporary saved data, loading...")
            with open(temp_file, 'r') as f:
                papers = json.load(f)
            click.echo(f"Loaded {len(papers)} papers from temporary file")
        else:
            # If no temp file, read from Excel
            click.echo(f"No temporary file found, reading from Excel...")
            df = pd.read_excel(excel_file, sheet_name=None)
            
            papers = []
            if 'Papers' in df and 'Structured Summaries' in df:
                papers_df = df['Papers']
                summaries_df = df['Structured Summaries']
                
                # Create a mapping of titles to relevance scores
                title_to_score = dict(zip(papers_df['title'], papers_df['relevance_score']))
                
                for _, row in summaries_df.iterrows():
                    title = row['Title']
                    score = title_to_score.get(title, 0.0)
                    
                    if score >= min_score:
                        paper = {
                            'title': title,
                            'doi': row['DOI'],
                            'relevance_score': score,
                            'structured_summary': {
                                'objective': row['Objective'],
                                'methods': row['Methods'],
                                'results': row['Results'],
                                'conclusions': row['Conclusions'],
                                'limitations': row['Limitations']
                            }
                        }
                        papers.append(paper)
            else:
                click.echo("Error: Required sheets not found in the Excel file.", err=True)
                return
        
        # Filter papers by score if loaded from temp file
        if min_score > 0:
            original_count = len(papers)
            papers = [p for p in papers if p.get('relevance_score', 0) >= min_score]
            click.echo(f"Filtered {original_count - len(papers)} papers below score threshold of {min_score}")
        
        if not papers:
            click.echo("No papers with summaries found to process.", err=True)
            return
        
        click.echo(f"Generating PDF summaries for {len(papers)} papers...")
        save_summaries_to_pdf(papers, output)
        click.echo(f"PDF summaries saved to {output}")
        
        # Clean up temp file if it exists
        if os.path.exists(temp_file):
            os.remove(temp_file)
            click.echo("Cleaned up temporary file")
        
    except Exception as e:
        click.echo(f"Error during PDF generation: {str(e)}", err=True)
        # Save current state to temp file if we have papers data
        if papers:
            with open(temp_file, 'w') as f:
                json.dump(papers, f)
            click.echo(f"Saved current state to {temp_file}")
        raise

def save_intermediate_results(papers: List[Dict[str, Any]], temp_file: str = '.temp_papers.json'):
    """Save intermediate results to a temporary file."""
    try:
        with open(temp_file, 'w') as f:
            json.dump(papers, f)
    except Exception as e:
        click.echo(f"Warning: Could not save intermediate results: {str(e)}", err=True)

@cli.command()
@click.option('--days', default=30, help='Number of days to look back')
@click.option('--output', type=click.Path(), default='research_updates.xlsx',
              help='Output file path (Excel format)')
@click.option('--min-score', default=5, help='Minimum relevance score for papers (typically ranges 1-20)')
@click.option('--download-papers', is_flag=True, help='Download PDFs of papers when available')
@click.option('--download-dir', type=click.Path(), default='papers',
              help='Directory to save downloaded papers')
@click.option('--model-path', default="deepseek-ai/deepseek-coder-7b-base",
              help='Path to DeepSeek model or model identifier')
@click.option('--no-ai', is_flag=True, help='Skip AI-powered features (summaries and analysis)')
@click.option('--detailed', is_flag=True, help='Show detailed table of all papers')
@click.option('--threads', default=min(32, os.cpu_count() * 4), 
              help='Number of threads for parallel processing')
@click.option('--temp-file', type=click.Path(), default='.temp_papers.json',
              help='File to save intermediate results')
@click.option('--search-terms', type=click.Choice([
    'tb_vaccine',
    'tb_diagnostics',
    'tb_molecular',
    'tb_resistance',
    'general_diagnostics',
    'emerging_tech',
    'custom'
], case_sensitive=False), multiple=True, default=['tb_diagnostics'],
    help='Search terms to use (multiple allowed)')
@click.option('--custom-query', help='Custom search query to use if search-terms includes "custom"')
def search(days: int, output: str, min_score: float, download_papers: bool, download_dir: str,
          model_path: str, no_ai: bool, detailed: bool, threads: int, temp_file: str,
          search_terms: tuple, custom_query: str):
    """Search for recent papers on TB research and diagnostic techniques."""
    use_ai = not no_ai
    
    if use_ai:
        # Initialize DeepSeek model with specified path
        deepseek_model.model_path = model_path
        click.echo(f"Initializing DeepSeek model from {model_path}...")
        if not deepseek_model.load_model():
            click.echo("Failed to load DeepSeek model. Continuing without AI features...", err=True)
            use_ai = False
    
    # Create papers directory at startup
    os.makedirs(download_dir, exist_ok=True)
    
    # Define search queries with specific focus areas
    SEARCH_QUERIES = {
        'tb_vaccine': "(tuberculosis OR mycobacterium tuberculosis OR mtb) AND (t cell OR t-cell OR Tcell) AND (vaccine OR antigen OR adjuvant)",
        'tb_diagnostics': "(tuberculosis OR mycobacterium tuberculosis OR mtb) AND (diagnostic OR detection OR screening OR assay) AND (novel OR new OR innovative OR rapid OR point-of-care)",
        'tb_molecular': "(tuberculosis OR mycobacterium tuberculosis OR mtb) AND (PCR OR sequencing OR molecular OR genomic) AND (method OR technique OR approach)",
        'tb_resistance': "(tuberculosis OR mycobacterium tuberculosis OR mtb) AND (resistance OR resistant OR MDR OR XDR) AND (detection OR diagnostic OR testing OR screening)",
        'general_diagnostics': "(diagnostic OR detection OR screening) AND (infectious disease OR pathogen) AND (novel OR innovative OR new) AND (method OR technique OR technology)",
        'emerging_tech': "(CRISPR OR nanopore OR microfluidic OR biosensor) AND (diagnostic OR detection OR screening) AND (infectious disease OR pathogen OR bacteria)"
    }
    
    # Build list of queries based on selected search terms
    queries = []
    for term in search_terms:
        if term == 'custom':
            if not custom_query:
                click.echo("Error: Custom search term selected but no custom query provided", err=True)
                return
            queries.append(custom_query)
        else:
            queries.append(SEARCH_QUERIES[term])
    
    if not queries:
        click.echo("Error: No search terms selected", err=True)
        return
    
    click.echo(f"Using the following search queries:")
    for i, query in enumerate(queries, 1):
        click.echo(f"{i}. {query}")
        click.echo(f"   Keywords: {', '.join(extract_keywords_from_query(query))}\n")
    
    all_papers = []
    console = Console()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=Console(force_terminal=True)
    ) as progress:
        # Create main task for queries
        queries_task = progress.add_task(
            "[cyan]Searching PubMed...",
            total=len(queries)
        )
        
        # Process queries in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for i, query in enumerate(queries, 1):
                future = executor.submit(
                    search_pubmed,
                    query,
                    days,
                    use_ai,
                    progress,
                    progress  # Pass the same progress object for paper tasks
                )
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    papers = future.result()
                    if papers:
                        with papers_lock:
                            all_papers.extend(papers)
                except Exception as e:
                    continue
    
    if not all_papers:
        click.echo("\nNo papers found matching the search criteria.")
        return
    
    # Remove duplicates and filter by score
    unique_papers = []
    seen_dois = set()
    for paper in all_papers:
        if paper['doi'] and paper['doi'] not in seen_dois and paper.get('relevance_score', 0) >= min_score:
            seen_dois.add(paper['doi'])
            unique_papers.append(paper)
    
    if not unique_papers:
        click.echo("\nNo papers found with scores above the minimum threshold.")
        return
    
    # Save intermediate results after filtering
    save_intermediate_results(unique_papers, temp_file)
    
    # Group similar papers
    click.echo("\nGrouping similar papers...")
    grouped_papers = group_similar_papers(unique_papers)
    
    # Save intermediate results after grouping
    save_intermediate_results(grouped_papers, temp_file)
    
    # Generate summaries in parallel if AI is enabled
    if use_ai:
        click.echo("\nGenerating summaries...")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=Console(force_terminal=True)
        ) as progress:
            summary_task = progress.add_task("[cyan]Generating summaries...", total=len(grouped_papers))
            grouped_papers = parallel_generate_summaries(grouped_papers, use_ai)
            
            # Save intermediate results after summaries
            save_intermediate_results(grouped_papers, temp_file)
    
    # Download papers in parallel if requested
    if download_papers:
        click.echo("\nDownloading papers...")
        session = get_authenticated_session()
        if session:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=Console(force_terminal=True)
            ) as progress:
                download_task = progress.add_task("[cyan]Downloading papers...", total=len(grouped_papers))
                download_statuses = parallel_download_papers(grouped_papers, download_dir, progress, download_task)
                
                # Add download status to papers
                for paper, status in zip(grouped_papers, download_statuses):
                    paper['download_status'] = status
                
                # Save intermediate results after downloads
                save_intermediate_results(grouped_papers, temp_file)
    
    # After generating summaries and before saving Excel file, save PDF summaries
    if use_ai and grouped_papers:
        pdf_output = os.path.splitext(output)[0] + '_summaries.pdf'
        click.echo(f"\nGenerating PDF summaries...")
        try:
            save_summaries_to_pdf(grouped_papers, pdf_output)
            click.echo(f"PDF summaries saved to {pdf_output}")
        except Exception as e:
            click.echo(f"Error generating PDF summaries: {str(e)}", err=True)
            click.echo(f"You can retry PDF generation later using the resume-pdf command")
    
    # Create DataFrame and save results
    df = pd.DataFrame(grouped_papers)
    
    # Save to Excel with grouped formatting and multiple sheets
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Main papers sheet
        df.to_excel(writer, index=False, sheet_name='Papers')
        workbook = writer.book
        worksheet = writer.sheets['Papers']
        
        # Add formatting
        current_cluster = None
        for idx, row in enumerate(df.itertuples(), start=2):
            if current_cluster != row.cluster:
                current_cluster = row.cluster
                if idx > 2:
                    worksheet.insert_rows(idx)
                    idx += 1
        
        # Create structured summaries sheet if AI is enabled
        if use_ai:
            summaries_data = []
            for paper in grouped_papers:
                if paper.get('structured_summary'):
                    summary = paper['structured_summary']
                    summaries_data.append({
                        'Title': paper['title'],
                        'DOI': paper['doi'],
                        'Objective': summary.get('objective', ''),
                        'Methods': summary.get('methods', ''),
                        'Results': summary.get('results', ''),
                        'Conclusions': summary.get('conclusions', ''),
                        'Limitations': summary.get('limitations', '')
                    })
            
            if summaries_data:
                summaries_df = pd.DataFrame(summaries_data)
                summaries_df.to_excel(writer, index=False, sheet_name='Structured Summaries')
    
    # Clean up temp file
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    # Display results...

@cli.command()
@click.argument('doi')
@click.option('--download-dir', type=click.Path(), default='papers',
              help='Directory to save downloaded papers')
def download_single(doi: str, download_dir: str):
    """Download a single paper by DOI."""
    # Create papers directory
    os.makedirs(download_dir, exist_ok=True)
    
    # First get paper metadata from PubMed
    click.echo("="*80)
    click.echo(f"Looking up paper metadata for DOI: {doi}")
    click.echo("="*80)
    
    try:
        # Search PubMed for the DOI
        handle = Entrez.esearch(db="pubmed", term=f"{doi}[DOI]")
        record = Entrez.read(handle)
        handle.close()
        
        if not record["IdList"]:
            click.echo("Could not find paper in PubMed.", err=True)
            return
        
        pmid = record["IdList"][0]
        
        # Get paper details
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        
        if 'PubmedArticle' not in records:
            click.echo("Could not fetch paper details.", err=True)
            return
            
        article = records['PubmedArticle'][0]
        article_data = article['MedlineCitation']['Article']
        title = str(article_data['ArticleTitle'])
        
        click.echo("\nPaper details:")
        click.echo("-"*40)
        click.echo(f"Title: {title}")
        click.echo(f"PMID: {pmid}")
        click.echo(f"DOI: {doi}")
        click.echo("-"*40)
        
        click.echo("\nStarting download process...")
        status = download_paper(doi, pmid, title, download_dir)
        
        click.echo("\nFinal status:")
        click.echo("="*40)
        click.echo(status)
        click.echo("="*40)
        
    except Exception as e:
        click.echo("="*40)
        click.echo(f"Error: {str(e)}", err=True)
        click.echo("="*40)

@cli.command()
@click.argument('dois', nargs=-1)
@click.option('--download-dir', type=click.Path(), default='papers',
              help='Directory to save downloaded papers')
def download_multiple(dois: tuple, download_dir: str):
    """Download multiple papers by DOI."""
    # Create papers directory
    os.makedirs(download_dir, exist_ok=True)
    
    for doi in dois:
        click.echo("\n" + "="*80)
        click.echo(f"Processing DOI: {doi}")
        click.echo("="*80)
        
        try:
            # Search PubMed for the DOI
            handle = Entrez.esearch(db="pubmed", term=f"{doi}[DOI]")
            record = Entrez.read(handle)
            handle.close()
            
            if not record["IdList"]:
                click.echo("Could not find paper in PubMed.", err=True)
                continue
            
            pmid = record["IdList"][0]
            
            # Get paper details
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            
            if 'PubmedArticle' not in records:
                click.echo("Could not fetch paper details.", err=True)
                continue
                
            article = records['PubmedArticle'][0]
            article_data = article['MedlineCitation']['Article']
            title = str(article_data['ArticleTitle'])
            
            click.echo("\nPaper details:")
            click.echo("-"*40)
            click.echo(f"Title: {title}")
            click.echo(f"PMID: {pmid}")
            click.echo(f"DOI: {doi}")
            click.echo("-"*40)
            
            # Create sanitized filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_title[:100]}_{pmid}.pdf"
            output_path = os.path.join(download_dir, filename)
            
            if os.path.exists(output_path):
                click.echo("File already exists, skipping...")
                continue
            
            status = download_paper(doi, pmid, title, download_dir)
            click.echo(f"Download status: {status}")
            
        except Exception as e:
            click.echo(f"Error processing {doi}: {str(e)}", err=True)
            continue

@cli.command()
@click.argument('excel_file', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), help='Output PDF path (default: input filename with _summaries.pdf)')
def convert_to_pdf(excel_file: str, output: str):
    """Convert an existing Excel file's structured summaries to PDF format."""
    # Default output path if not specified
    if not output:
        output = os.path.splitext(excel_file)[0] + '_summaries.pdf'
    
    click.echo(f"Reading {excel_file}...")
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file, sheet_name=None)
        
        # Check if we have structured summaries
        papers = []
        if 'Structured Summaries' in df:
            summaries_df = df['Structured Summaries']
            papers_df = df['Papers']  # Main sheet with paper details
            
            # Convert DataFrame rows to paper dictionaries
            for _, row in summaries_df.iterrows():
                paper = {
                    'title': row['Title'],
                    'doi': row['DOI'],
                    'structured_summary': {
                        'objective': row['Objective'],
                        'methods': row['Methods'],
                        'results': row['Results'],
                        'conclusions': row['Conclusions'],
                        'limitations': row['Limitations']
                    }
                }
                papers.append(paper)
        else:
            click.echo("Error: No structured summaries found in the Excel file.", err=True)
            click.echo("Make sure the file was generated with AI features enabled (without --no-ai).")
            click.echo("You can download the latest version of CureConnect from: https://github.com/jasonlimberis/CureConnect")
            click.echo("You can download the latest version of CureConnect from: https://github.com/jasonlimberis/CureConnect")
            return
        
        if not papers:
            click.echo("No papers with summaries found in the Excel file.", err=True)
            return
        
        click.echo(f"Converting {len(papers)} summaries to PDF...")
        save_summaries_to_pdf(papers, output)
        click.echo(f"PDF summaries saved to {output}")
        
    except Exception as e:
        click.echo(f"Error converting file: {str(e)}", err=True)

@cli.command()
@click.argument('excel_file', type=click.Path(exists=True))
@click.option('--download-dir', type=click.Path(), default='papers',
              help='Directory to save downloaded papers')
def retry_downloads(excel_file: str, download_dir: str):
    """Retry downloading papers that previously failed."""
    click.echo(f"Reading {excel_file}...")
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Filter for failed or not attempted downloads
        failed_papers = []
        for _, row in df.iterrows():
            status = str(row.get('download_status', '')).lower()
            if 'fail' in status or 'error' in status or pd.isna(row.get('download_status')):
                paper = {
                    'title': row['title'],
                    'doi': row.get('doi', None),
                    'pmid': row.get('pmid', None)
                }
                if paper['doi'] or paper['pmid']:  # Only include if we have at least one identifier
                    failed_papers.append(paper)
        
        if not failed_papers:
            click.echo("No failed downloads found to retry.")
            return
        
        # Create download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        # Get authenticated session
        click.echo("\nSetting up authentication...")
        session = get_authenticated_session()
        if not session:
            click.echo("Failed to authenticate. Please try again.", err=True)
            return
        
        # Show progress bar for downloads
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=Console(force_terminal=True)
        ) as progress:
            download_task = progress.add_task(
                f"[cyan]Retrying {len(failed_papers)} downloads...",
                total=len(failed_papers)
            )
            
            # Download papers
            download_statuses = parallel_download_papers(
                failed_papers,
                download_dir,
                session,
                progress,
                download_task
            )
        
        # Show results
        success_count = sum(1 for status in download_statuses if 'downloaded' in status.lower())
        already_count = sum(1 for status in download_statuses if 'already' in status.lower())
        fail_count = len(download_statuses) - success_count - already_count
        
        # Create results table
        table = Table(title="Download Retry Results")
        table.add_column("Paper", style="cyan")
        table.add_column("Status", style="green")
        
        for paper, status in zip(failed_papers, download_statuses):
            title = paper['title'][:100] + "..." if len(paper['title']) > 100 else paper['title']
            table.add_row(title, status)
        
        console = Console()
        console.print("\n")
        console.print(table)
        
        # Print summary
        click.echo(f"\nSummary:")
        click.echo(f"Successfully downloaded: {success_count}")
        click.echo(f"Already present: {already_count}")
        click.echo(f"Failed: {fail_count}")
        
    except Exception as e:
        click.echo(f"Error processing file: {str(e)}", err=True)

@cli.command()
@click.argument('excel_file', type=click.Path(exists=True))
@click.option('--download-dir', type=click.Path(), default='papers',
              help='Directory to save downloaded papers')
@click.option('--min-score', type=float, default=0.0,
              help='Minimum relevance score for papers to download (typically ranges 1-20)')
def download_from_excel(excel_file: str, download_dir: str, min_score: float):
    """Download papers from an existing research_updates.xlsx file."""
    click.echo(f"Reading {excel_file}...")
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Filter by score if specified
        if min_score > 0:
            original_count = len(df)
            df = df[df['relevance_score'] >= min_score]
            click.echo(f"Filtered {original_count - len(df)} papers below score threshold of {min_score}")
        
        if df.empty:
            click.echo("No papers found to download.")
            return
        
        # Create papers directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        # Get authenticated session
        click.echo("\nSetting up authentication...")
        session = get_authenticated_session()
        if not session:
            click.echo("Failed to authenticate. Please try again.", err=True)
            return
        
        # Prepare papers list for download
        papers = []
        for _, row in df.iterrows():
            paper = {
                'title': row['title'],
                'doi': row.get('doi'),
                'pmid': row.get('pmid'),
                'relevance_score': row.get('relevance_score', 0.0)
            }
            if paper['doi'] or paper['pmid']:  # Only include if we have at least one identifier
                papers.append(paper)
        
        if not papers:
            click.echo("No papers with valid identifiers found.")
            return
        
        # Show progress bar for downloads
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=Console(force_terminal=True)
        ) as progress:
            download_task = progress.add_task(
                f"[cyan]Downloading {len(papers)} papers...",
                total=len(papers)
            )
            
            # Download papers
            download_statuses = parallel_download_papers(
                papers,
                download_dir,
                session,
                progress,
                download_task
            )
        
        # Show results
        success_count = sum(1 for status in download_statuses if 'downloaded' in status.lower())
        already_count = sum(1 for status in download_statuses if 'already' in status.lower())
        fail_count = len(download_statuses) - success_count - already_count
        
        # Create results table
        table = Table(title="Download Results")
        table.add_column("Paper", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Score", style="yellow", justify="right")
        
        for paper, status in zip(papers, download_statuses):
            title = paper['title'][:100] + "..." if len(paper['title']) > 100 else paper['title']
            score = f"{paper.get('relevance_score', 0.0):.1f}"
            table.add_row(title, status, score)
        
        console = Console()
        console.print("\n")
        console.print(table)
        
        # Print summary
        click.echo(f"\nSummary:")
        click.echo(f"Successfully downloaded: {success_count}")
        click.echo(f"Already present: {already_count}")
        click.echo(f"Failed: {fail_count}")
        
    except Exception as e:
        click.echo(f"Error processing file: {str(e)}", err=True)

def process_local_pdfs(pdf_dir: str, use_ai: bool = True, threads: int = MAX_WORKERS) -> List[Dict[str, Any]]:
    """Process local PDFs and generate summaries."""
    papers = []
    pdf_files = list(Path(pdf_dir).glob('*.pdf'))
    
    if not pdf_files:
        click.echo("No PDF files found in the specified directory.")
        return papers
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=Console(force_terminal=True)
    ) as progress:
        # Create task for processing PDFs
        pdf_task = progress.add_task(
            "[cyan]Processing PDFs...",
            total=len(pdf_files)
        )
        
        # Process PDFs in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for pdf_file in pdf_files:
                future = executor.submit(extract_pdf_info, pdf_file, use_ai)
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    paper = future.result()
                    if paper:
                        papers.append(paper)
                    with progress_lock:
                        progress.advance(pdf_task)
                except Exception as e:
                    click.echo(f"Error processing PDF: {str(e)}", err=True)
                    with progress_lock:
                        progress.advance(pdf_task)
    
    return papers

def extract_pdf_info(pdf_path: Path, use_ai: bool) -> Dict[str, Any]:
    """Extract information from a PDF file."""
    try:
        # Extract text from PDF
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Extract all text from the PDF
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()
            
            # Extract first few pages for title and abstract
            num_pages = min(5, len(reader.pages))
            initial_text = ""
            for i in range(num_pages):
                initial_text += reader.pages[i].extract_text()
            
            # Try to extract title (usually first line or after specific keywords)
            title_patterns = [
                r'^(.*?)\n',  # First line
                r'Title[:\s]+(.*?)\n',  # After "Title:"
                r'TITLE[:\s]+(.*?)\n',  # After "TITLE:"
            ]
            
            title = pdf_path.stem  # Default to filename
            for pattern in title_patterns:
                match = re.search(pattern, initial_text)
                if match:
                    potential_title = match.group(1).strip()
                    if len(potential_title) > 10:  # Reasonable title length
                        title = potential_title
                        break
            
            # Try to extract abstract
            abstract_patterns = [
                r'Abstract[:\s]+(.*?)(?=\n\n|\n[A-Z]{2,})',  # After "Abstract:" until double newline or all-caps section
                r'ABSTRACT[:\s]+(.*?)(?=\n\n|\n[A-Z]{2,})',  # After "ABSTRACT:"
                r'Summary[:\s]+(.*?)(?=\n\n|\n[A-Z]{2,})',   # After "Summary:"
            ]
            
            abstract = ""
            for pattern in abstract_patterns:
                match = re.search(pattern, initial_text, re.DOTALL)
                if match:
                    abstract = match.group(1).strip()
                    break
            
            # If no abstract found, use first 1000 characters after title
            if not abstract:
                text_after_title = initial_text[initial_text.find(title) + len(title):].strip()
                abstract = text_after_title[:1000]
            
            paper = {
                'title': title,
                'abstract': abstract,
                'full_text': full_text,
                'filename': pdf_path.name,
                'date': datetime.now().strftime('%Y-%m-%d'),  # Use current date as fallback
            }
            
            # Generate AI summary if enabled
            if use_ai:
                try:
                    summary = generate_structured_summary(abstract, title, full_text)
                    if summary:
                        paper['structured_summary'] = summary
                        paper['summary_source'] = summary.get('summary_source', 'Unknown')
                except Exception as e:
                    click.echo(f"Error generating summary: {str(e)}", err=True)
            
            return paper
            
    except Exception as e:
        click.echo(f"Error processing {pdf_path}: {str(e)}", err=True)
        return None

def sanitize_for_excel(text: str) -> str:
    """Sanitize text for Excel by removing or replacing problematic characters."""
    if not isinstance(text, str):
        return str(text)
    
    # Remove or replace problematic characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)  # Remove control characters
    text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')  # Replace newlines with spaces
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = text.strip()
    
    # Truncate if too long (Excel has a 32,767 character limit)
    if len(text) > 32000:
        text = text[:32000] + "..."
    
    return text

def prepare_for_excel(papers: List[Dict[str, Any]]) -> pd.DataFrame:
    """Prepare papers data for Excel export by sanitizing all text fields."""
    excel_data = []
    for paper in papers:
        row = {
            'Title': sanitize_for_excel(paper.get('title', '')),
            'Filename': sanitize_for_excel(paper.get('filename', '')),
            'Abstract': sanitize_for_excel(paper.get('abstract', '')),
            'Date': paper.get('date', ''),
            'Cluster': paper.get('cluster', -1)
        }
        
        # Add summary fields if available
        if paper.get('structured_summary'):
            summary = paper['structured_summary']
            row.update({
                'Objective': sanitize_for_excel(summary.get('objective', '')),
                'Methods': sanitize_for_excel(summary.get('methods', '')),
                'Results': sanitize_for_excel(summary.get('results', '')),
                'Conclusions': sanitize_for_excel(summary.get('conclusions', '')),
                'Limitations': sanitize_for_excel(summary.get('limitations', ''))
            })
        
        excel_data.append(row)
    
    return pd.DataFrame(excel_data)

@cli.command()
@click.argument('pdf_dir', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), help='Output PDF path (default: summaries.pdf)')
@click.option('--model-path', default="deepseek-ai/deepseek-coder-7b-base",
              help='Path to DeepSeek model or model identifier')
@click.option('--no-ai', is_flag=True, help='Skip AI-powered summaries')
@click.option('--threads', default=min(32, os.cpu_count() * 4), 
              help='Number of threads for parallel processing')
def summarize_pdfs(pdf_dir: str, output: str, model_path: str, no_ai: bool, threads: int):
    """Generate summaries from a directory of PDF files."""
    use_ai = not no_ai
    
    if use_ai:
        # Initialize DeepSeek model with specified path
        deepseek_model.model_path = model_path
        click.echo(f"Initializing DeepSeek model from {model_path}...")
        if not deepseek_model.load_model():
            click.echo("Failed to load DeepSeek model. Continuing without AI features...", err=True)
            use_ai = False
    
    if not output:
        output = 'summaries.pdf'
    
    click.echo(f"Processing PDFs in {pdf_dir}...")
    
    try:
        # Process PDFs and generate summaries
        papers = process_local_pdfs(pdf_dir, use_ai, threads)
        
        if not papers:
            click.echo("No papers were successfully processed.")
            return
        
        # Group similar papers
        click.echo("\nGrouping similar papers...")
        grouped_papers = group_similar_papers(papers)
        
        # Generate PDF with summaries
        click.echo(f"\nGenerating PDF summaries...")
        save_summaries_to_pdf(grouped_papers, output)
        click.echo(f"PDF summaries saved to {output}")
        
        # Also save to Excel for reference
        excel_output = os.path.splitext(output)[0] + '.xlsx'
        
        # Prepare data for Excel
        df = prepare_for_excel(grouped_papers)
        
        # Save to Excel
        with pd.ExcelWriter(excel_output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Papers')
            
            # Create structured summaries sheet if AI was used
            if use_ai:
                summaries_data = []
                for paper in grouped_papers:
                    if paper.get('structured_summary'):
                        summary = paper['structured_summary']
                        summaries_data.append({
                            'Title': sanitize_for_excel(paper['title']),
                            'Filename': sanitize_for_excel(paper['filename']),
                            'Objective': sanitize_for_excel(summary.get('objective', '')),
                            'Methods': sanitize_for_excel(summary.get('methods', '')),
                            'Results': sanitize_for_excel(summary.get('results', '')),
                            'Conclusions': sanitize_for_excel(summary.get('conclusions', '')),
                            'Limitations': sanitize_for_excel(summary.get('limitations', ''))
                        })
                
                if summaries_data:
                    summaries_df = pd.DataFrame(summaries_data)
                    summaries_df.to_excel(writer, index=False, sheet_name='Structured Summaries')
        
        click.echo(f"Excel file saved to {excel_output}")
        
        # Show results table
        table = Table(title="Processing Results")
        table.add_column("Filename", style="cyan")
        table.add_column("Status", style="green")
        
        for paper in grouped_papers:
            filename = paper['filename']
            status = "Processed" if paper.get('structured_summary') else "No summary generated"
            table.add_row(filename, status)
        
        console = Console()
        console.print("\n")
        console.print(table)
        
        # Print summary
        total_papers = len(grouped_papers)
        with_summaries = sum(1 for p in grouped_papers if p.get('structured_summary'))
        click.echo(f"\nSummary:")
        click.echo(f"Total PDFs processed: {total_papers}")
        click.echo(f"Summaries generated: {with_summaries}")
        click.echo(f"Failed to generate summaries: {total_papers - with_summaries}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise

def get_authenticated_session() -> requests.Session:
    """Create an authenticated session for downloading papers."""
    session = requests.Session()
    
    # Configure session with reasonable defaults
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Configure connection pooling
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=MAX_WORKERS,
        pool_maxsize=MAX_WORKERS,
        max_retries=MAX_RETRIES,
        pool_block=False
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session

if __name__ == '__main__':
    cli()

