from typing import List, Optional
from pydantic import BaseModel
import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup

from ..src. scrapegen.scraper_main import ContentExtractor, InfoExtractorAi

class CompanyInfo(BaseModel):
    """Represents information about a company."""
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    funding_amount: Optional[str] = None
    ceo_name: Optional[str] = None
    company_url: Optional[str] = None

class CompaniesInfo(BaseModel):
    """Represents a collection of company information."""
    companies: List[CompanyInfo]

@pytest.fixture
def mock_html_content():
    return """
    <html>
        <body>
            <h1>Company Name</h1>
            <p>Company Description</p>
            <a href="/about">About Us</a>
            <h2>CEO: John Doe</h2>
            <p>Funding: $10M</p>
        </body>
    </html>
    """

class TestContentExtractor:
    def test_successful_extraction(self, mock_html_content):
        # Arrange
        extractor = ContentExtractor()
        
        # Act
        content = extractor.extract(mock_html_content)
        
        # Assert
        assert isinstance(content, list)
        assert "Company Name" in content
        assert "Company Description" in content
        assert "CEO: John Doe" in content
        assert "Funding: $10M" in content

    def test_empty_content(self):
        # Arrange
        extractor = ContentExtractor()
        
        # Act
        content = extractor.extract("")
        
        # Assert
        assert isinstance(content, list)
        assert len(content) == 0

    def test_invalid_html(self):
        # Arrange
        extractor = ContentExtractor()
        invalid_html = "<invalid><<<>>>"
        
        # Act
        content = extractor.extract(invalid_html)
        
        # Assert
        assert isinstance(content, list)
        assert len(content) == 0

class TestInfoExtractorAi:
    def test_successful_extraction(self):
        # Arrange
        mock_llm_manager = Mock()
        mock_response = Mock()
        mock_response.content = """```json
        {
            "companies": [
                {
                    "company_name": "Test Corp",
                    "company_description": "A test company",
                    "funding_amount": "$10M",
                    "ceo_name": "John Doe",
                    "company_url": "https://example.com"
                }
            ]
        }
        ```"""
        mock_llm_manager.create_instance.return_value.invoke.return_value = mock_response

        extractor = InfoExtractorAi(
            basemodel=CompaniesInfo,
            llm_manager=mock_llm_manager
        )

        # Act
        result = extractor.extract("some content")
        
        # Assert
        assert isinstance(result, CompaniesInfo)
        assert len(result.companies) == 1
        assert result.companies[0].company_name == "Test Corp"
        assert result.companies[0].company_description == "A test company"
        assert result.companies[0].funding_amount == "$10M"
        assert result.companies[0].ceo_name == "John Doe"
        assert result.companies[0].company_url == "https://example.com"

    def test_invalid_json_response(self):
        # Arrange
        mock_llm_manager = Mock()
        mock_response = Mock()
        mock_response.content = "Invalid JSON"
        mock_llm_manager.create_instance.return_value.invoke.return_value = mock_response

        extractor = InfoExtractorAi(
            basemodel=CompaniesInfo,
            llm_manager=mock_llm_manager
        )

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            extractor.extract("some content")

    def test_empty_companies_list(self):
        # Arrange
        mock_llm_manager = Mock()
        mock_response = Mock()
        mock_response.content = """```json
        {
            "companies": []
        }
        ```"""
        mock_llm_manager.create_instance.return_value.invoke.return_value = mock_response

        extractor = InfoExtractorAi(
            basemodel=CompaniesInfo,
            llm_manager=mock_llm_manager
        )

        # Act
        result = extractor.extract("some content")
        
        # Assert
        assert isinstance(result, CompaniesInfo)
        assert len(result.companies) == 0