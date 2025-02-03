import pytest
from unittest.mock import Mock, patch
from scrapegen.scraper_main import (
    ConfigurationError,
    ScrapeConfig,
    ScrapeGen,
    ScrapingError,
    WebsiteScraper
)

from typing import List, Optional
from pydantic import BaseModel
### This class is created as an example 
class CompanyInfo(BaseModel):
    """
Represents information about a company.

Attributes:
    company_name (Optional[str]): The name of the company.
    company_description (Optional[str]): A brief description of the company.
    funding_amount (Optional[str]): The amount of funding the company has received.
    ceo_name (Optional[str]): The name of the company's CEO.
    company_url (Optional[str]): The URL of the company's website.
"""
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    funding_amount: Optional[str] = None
    ceo_name: Optional[str] = None
    company_url: Optional[str] = None

### This class is created as an example 
class CompaniesInfo(BaseModel):
    """
Represents a collection of company information.

Attributes:
    companies (List[CompanyInfo]): A list of CompanyInfo objects containing details about various companies.
"""
    companies: List[CompanyInfo]


@pytest.fixture
def valid_scraper():
    return ScrapeGen(api_key="valid-key")

@pytest.fixture
def mock_company_info():
    return CompaniesInfo(
        companies=[
            CompanyInfo(
                company_name="Test Corp",
                company_description="A test company",
                funding_amount="$10M",
                ceo_name="John Doe",
                company_url="https://example.com"
            )
        ]
    )

def test_scrapegen_initialization():
    # Test empty API key
    with pytest.raises(ConfigurationError):
        ScrapeGen(api_key="")
    
    # Test valid initialization
    scraper = ScrapeGen(api_key="valid-key")
    assert isinstance(scraper.config, ScrapeConfig)

def test_scrapegen_config_update(valid_scraper):
    # Test valid config update
    valid_scraper.update_config(max_pages=30, max_depth=2)
    assert valid_scraper.config.max_pages == 30
    assert valid_scraper.config.max_depth == 2
    
    # Test invalid config update
    with pytest.raises(ConfigurationError):
        valid_scraper.update_config(invalid_param="value")

def test_scrapegen_scrape(valid_scraper, mock_company_info):
    # Setup mock extractor
    mock_extractor = Mock()
    mock_extractor.extract.return_value = mock_company_info
    valid_scraper._extractor = mock_extractor

    # Mock the WebsiteScraper to return predefined content
    mock_content = [["Sample content 1"], ["Sample content 2"]]
    with patch.object(WebsiteScraper, 'scrape', return_value=mock_content) as mock_scrape:
        # Perform scraping
        result = valid_scraper.scrape("https://example.com", CompaniesInfo)
        
        # Verify results
        assert isinstance(result, CompaniesInfo)
        assert len(result.companies) == 1
        assert result.companies[0].company_name == "Test Corp"
        
        # Verify scraper was called with correct parameters
        mock_scrape.assert_called_once_with(
            "https://example.com",
            max_page=valid_scraper.config.max_pages,
            max_subpage=valid_scraper.config.max_subpages,
            max_depth=valid_scraper.config.max_depth
        )
        
        # Verify extractor was called with mock content
        mock_extractor.extract.assert_called_once_with(mock_content)
def test_scrapegen_scrape_error(valid_scraper):
    # Test scraping with invalid URL
    with pytest.raises(ConfigurationError):
        valid_scraper.scrape("", CompaniesInfo)
    
    # Test scraping with network error
    with patch('requests.get', side_effect=Exception("Network error")):
        with pytest.raises(ScrapingError) as exc_info:
            valid_scraper.scrape("https://example.com", CompaniesInfo)
        assert "No content was scraped from the URL" in str(exc_info.value)