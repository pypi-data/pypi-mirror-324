import pytest
from urllib.parse import urljoin

from scrapegen.scraper_main import UrlNormalizer

def test_url_normalizer():
    normalizer = UrlNormalizer()
    base_url = "https://example.com"
    page_path = "https://example.com/blog/"

    # Test absolute URL
    assert normalizer.normalize("https://example.com/about", base_url, page_path) == "https://example.com/about"
    
    # Test relative URL with leading slash
    assert normalizer.normalize("/contact", base_url, page_path) == "https://example.com/contact"
    
    # Test relative URL without leading slash
    assert normalizer.normalize("post/1", base_url, page_path) == "https://example.com/blog/post/1"
