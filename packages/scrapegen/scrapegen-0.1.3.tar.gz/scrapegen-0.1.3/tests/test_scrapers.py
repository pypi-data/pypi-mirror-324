import pytest
from unittest.mock import patch, Mock
from scrapegen.scraper_main import (
    AnchorScraper, 
    ContentExtractor, 
    URLScraper, 
    UrlNormalizer, 
    UrlParser, 
    WebsiteScraper
)

@pytest.fixture
def mock_html_content():
    return """
    <html>
        <body>
            <h1>Test Corp</h1>
            <p>A test company</p>
            <a href="/about">About Us</a>
            <a href="https://example.com/contact">Contact</a>
            <h2>CEO: John Doe</h2>
            <p>Funding: $10M</p>
        </body>
    </html>
    """

@pytest.fixture
def mock_scraper_response(mock_html_content):
    mock = Mock()
    mock.text = mock_html_content
    mock.raise_for_status = Mock()
    return mock

@pytest.fixture
def website_scraper():
    return WebsiteScraper(
        normalizer=UrlNormalizer(),
        anchorScraper=AnchorScraper(),
        urlParser=UrlParser(),
        urlScraper=URLScraper(),
        contentExtractor=ContentExtractor()
    )

class TestAnchorScraper:
    def test_successful_scraping(self, mock_html_content):
        # Arrange
        scraper = AnchorScraper()
        base_url = "https://example.com"
        
        # Act
        links = scraper.scrape(mock_html_content, base_url)
        
        # Assert
        assert isinstance(links, list)
        assert "https://example.com/about" in links
        assert "https://example.com/contact" in links

    def test_empty_content(self):
        # Arrange
        scraper = AnchorScraper()
        base_url = "https://example.com"
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            scraper.scrape(None, base_url)
        assert "The given content is null" in str(exc_info.value)

class TestUrlScraper:
    def test_successful_scraping(self, mock_scraper_response):
        # Arrange
        scraper = URLScraper()
        
        # Act
        with patch('requests.get') as mock_get:
            mock_get.return_value = mock_scraper_response
            content = scraper.scrape("https://example.com")
            
            # Assert
            assert content == mock_scraper_response.text
            mock_get.assert_called_once_with("https://example.com")

    def test_request_error(self):
        # Arrange
        scraper = URLScraper()
        
        # Act
        with patch('requests.get', side_effect=Exception("Network error")):
            content = scraper.scrape("https://example.com")
            
            # Assert
            assert content is None

class TestWebsiteScraper:
    def test_successful_scraping(self, website_scraper, mock_scraper_response):
        # Arrange
        expected_content = ["Test Corp", "A test company", "CEO: John Doe", "Funding: $10M"]
        
        # Act
        with patch('requests.get') as mock_get:
            mock_get.return_value = mock_scraper_response
            content = website_scraper.scrape(
                "https://example.com",
                max_page=1,
                max_subpage=1,
                max_depth=1
            )
            
            # Assert
            assert isinstance(content, list)
            assert len(content) > 0
            # Flatten the content list since it contains nested lists
            flattened_content = [item for sublist in content for item in sublist]
            for expected_item in expected_content:
                assert any(expected_item in item for item in flattened_content)

    def test_max_depth_limit(self, website_scraper, mock_scraper_response):
        # Arrange & Act
        with patch('requests.get') as mock_get:
            mock_get.return_value = mock_scraper_response
            content = website_scraper.scrape(
                "https://example.com",
                max_page=1,
                max_subpage=1,
                max_depth=0
            )
            
            # Assert
            assert len(content) == 0

    def test_error_handling(self, website_scraper):
        # Act
        with patch('requests.get', side_effect=Exception("Network error")):
            content = website_scraper.scrape(
                "https://example.com",
                max_page=1,
                max_subpage=1,
                max_depth=1
            )
            
            # Assert
            assert isinstance(content, list)
            assert len(content) == 0