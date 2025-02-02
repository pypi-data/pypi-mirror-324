import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
import os

# Import CLI before setting up mocks
from paperpulseai.core import cli

@pytest.fixture(autouse=True)
def setup_environment():
    """Set up required environment variables for testing."""
    os.environ['ENTREZ_EMAIL'] = 'test@example.com'
    yield
    if 'ENTREZ_EMAIL' in os.environ:
        del os.environ['ENTREZ_EMAIL']

def test_cli_commands_available():
    """Test that all CLI commands are available."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    
    # Check for expected commands in help output
    expected_commands = [
        'search',
        'download-single',
        'download-multiple',
        'convert-to-pdf',
        'retry-downloads',
        'download-from-excel',
        'summarize-pdfs',
        'resume-pdf'
    ]
    
    for command in expected_commands:
        assert command in result.output, f"Command {command} not found in CLI"

def test_search_command_help():
    """Test that search command help works."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--email', 'test@example.com', 'search', '--help'])
    assert result.exit_code == 0
    
    # Check for important options in help output
    expected_options = [
        '--days',
        '--output',
        '--min-score',
        '--download-papers',
        '--download-dir',
        '--model-path',
        '--no-ai',
        '--detailed',
        '--threads',
        '--temp-file',
        '--search-terms',
        '--custom-query'
    ]
    
    for option in expected_options:
        assert option in result.output, f"Option {option} not found in search command help"

def test_cli_requires_email():
    """Test that CLI requires email parameter when not set in environment."""
    runner = CliRunner()
    # Temporarily remove email from environment
    if 'ENTREZ_EMAIL' in os.environ:
        stored_email = os.environ['ENTREZ_EMAIL']
        del os.environ['ENTREZ_EMAIL']
    else:
        stored_email = None
    
    try:
        result = runner.invoke(cli, ['search'])
        assert result.exit_code == 2
        assert "Missing option '--email'" in result.output
    finally:
        # Restore email if it was previously set
        if stored_email is not None:
            os.environ['ENTREZ_EMAIL'] = stored_email

@pytest.mark.integration
def test_search_basic_functionality(tmp_path):
    """Test basic search functionality with minimal query."""
    runner = CliRunner()
    output_file = tmp_path / "test_output.xlsx"
    
    mock_paper = {
        'title': 'Test Article',
        'abstract': 'Test abstract',
        'date': '2024',
        'pmid': '12345',
        'doi': '10.1234/test.12345',  # Added DOI
        'journal': 'Test Journal',
        'authors': ['Test Author'],
        'relevance_score': 10.0,
        'cluster': 0,
        'matched_keywords': ['test'],
        'url': None
    }
    
    with patch('paperpulseai.core.search_pubmed') as mock_search, \
         patch('paperpulseai.core.calculate_relevance_scores') as mock_scores, \
         patch('paperpulseai.core.group_similar_papers') as mock_group, \
         patch('paperpulseai.core.extract_keywords_from_query') as mock_keywords, \
         patch('paperpulseai.core.save_intermediate_results') as mock_save:
        
        # Mock search results
        mock_search.return_value = [mock_paper]
        mock_scores.return_value = [mock_paper]  # Return same paper with score
        mock_group.return_value = [mock_paper]  # Return same paper with cluster
        mock_keywords.return_value = ['test', 'keywords']  # Return test keywords
        mock_save.return_value = None  # Mock saving intermediate results
        
        result = runner.invoke(cli, [
            '--email', 'test@example.com',
            'search',
            '--days', '1',
            '--output', str(output_file),
            '--no-ai',  # Skip AI features for testing
            '--search-terms', 'tb_diagnostics',
            '--min-score', '1'  # Set low min score to ensure paper is included
        ])
        
        # Print output for debugging
        print("\nCommand output:")
        print(result.output)
        if result.exception:
            print("\nException:")
            print(result.exception)
        
        assert result.exit_code == 0
        assert os.path.exists(output_file) 