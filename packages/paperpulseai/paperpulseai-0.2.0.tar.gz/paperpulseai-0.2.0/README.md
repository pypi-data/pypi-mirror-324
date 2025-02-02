# PaperPulseAI

A Python package that searches for recently published papers about tuberculosis research and new diagnostic techniques. It creates a comprehensive table of paper details including titles, DOI links, abstracts, and AI-generated summaries of the main points.

## Features

- Searches PubMed for recent papers about tuberculosis and diagnostic techniques
- Generates AI-powered summaries of paper abstracts using DeepSeek
- Exports results to Excel with detailed information
- Displays a clean table output in the terminal
- Includes progress bars for all operations
- Downloads full-text PDFs when available
- Groups similar papers together
- Generates PDF summaries with structured analysis
- Supports multiple predefined search categories
- Caches summaries for faster subsequent runs

## Installation

Install PaperPulseAI using pip:

```bash
pip install paperpulseai
```

## Testing

To run the tests, first install the package with test dependencies:

```bash
pip install paperpulseai[test]
```

Then run the tests using pytest:

```bash
pytest paperpulseai/tests/
```

The tests verify:
- CLI commands are available and properly configured
- Basic functionality works as expected
- Required parameters are enforced
- Help documentation is complete

## Configuration

You need to set up the following:

1. Set your email address for PubMed API access using one of these methods:
   - Environment variable: `export ENTREZ_EMAIL=your.email@example.com`
   - Configuration file: Create `~/.paperpulseai/config.ini` with:
     ```ini
     [email]
     entrez_email = your.email@example.com
     ```
   - Command line: Use the `--email` option with any command
   - Python code: Set `paperpulseai.set_email("your.email@example.com")`

2. Ensure you have enough disk space for the DeepSeek model (approximately 7GB)

The email address is required by NCBI to track API usage and contact you if there are any issues with your requests. Your email will not be shared or used for marketing purposes.

## Usage

After installation, you can use PaperPulseAI directly from the command line:

### Search for Papers
```bash
paperpulseai search [OPTIONS]
```

Options:
- `--days`: Number of days to look back (default: 30)
- `--output`: Output file path (default: research_updates.xlsx)
- `--min-score`: Minimum relevance score for papers (default: 5, range: 1-20)
- `--download-papers`: Download PDFs of papers when available
- `--download-dir`: Directory to save downloaded papers (default: papers)
- `--model-path`: Path to DeepSeek model (default: deepseek-ai/deepseek-coder-7b-base)
- `--no-ai`: Skip AI-powered features
- `--detailed`: Show detailed table of all papers
- `--threads`: Number of threads for parallel processing
- `--temp-file`: File to save intermediate results
- `--email`: Email address for PubMed API access (overrides other config methods)
- `--search-terms`: Search categories to use (multiple allowed):
  - `tb_vaccine`: TB vaccine research
  - `tb_diagnostics`: TB diagnostic techniques
  - `tb_molecular`: Molecular/genomic methods
  - `tb_resistance`: Drug resistance detection
  - `general_diagnostics`: General diagnostic innovations
  - `emerging_tech`: Emerging technologies
  - `custom`: Use custom search query
- `--custom-query`: Custom search query to use with 'custom' search term

### Download Papers by DOI
```bash
paperpulseai download-single DOI [OPTIONS]
```

### Download Multiple Papers by DOI
```bash
paperpulseai download-multiple [DOIS]... [OPTIONS]
```

### Download Papers from Excel
```bash
paperpulseai download-from-excel EXCEL_FILE [OPTIONS]
```

### Retry Failed Downloads
```bash
paperpulseai retry-downloads EXCEL_FILE [OPTIONS]
```

### Generate PDF Summaries
```bash
paperpulseai resume-pdf EXCEL_FILE [OPTIONS]
```

### Convert Excel to PDF
```bash
paperpulseai convert-to-pdf EXCEL_FILE [OPTIONS]
```

### Summarize Local PDFs
```bash
paperpulseai summarize-pdfs PDF_DIR [OPTIONS]
```

## Output

The program generates several types of output:

1. Excel File (default: research_updates.xlsx):
   - Papers sheet with basic information
   - Structured Summaries sheet with AI-generated analysis
   - Includes titles, DOIs, abstracts, relevance scores, and more

2. PDF Summaries:
   - Structured analysis of each paper
   - Organized by topic clusters
   - Includes objectives, methods, results, conclusions, and limitations
   - Beautiful and professional layout

3. Downloaded Papers:
   - Full-text PDFs when available
   - Organized in the specified download directory
   - Named using paper titles and PMIDs
   - Supports multiple download methods (PubMed Central, DOI, Sci-Hub)

4. Terminal Output:
   - Progress bars for all operations
   - Clean tables showing results
   - Summary statistics and status updates

## Caching

The program implements caching for AI-generated summaries to improve performance:
- Summaries are cached for 7 days
- Cached summaries are automatically reused when processing the same abstract
- Cache is stored in the `.cache` directory

## Error Handling

The program includes robust error handling:
- Automatic retries for failed API calls
- Intermediate results saving during long operations
- Ability to resume failed PDF generation
- Parallel processing with proper rate limiting

## License

This project is licensed under the MIT License - see the LICENSE file for details. 