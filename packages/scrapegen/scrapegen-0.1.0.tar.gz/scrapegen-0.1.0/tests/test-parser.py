import pytest

from scrapegen.scraper_main import UrlParser

def test_url_parser():
    parser = UrlParser()
    url = "https://example.com/blog/post/1"
    
    assert parser.get_base_url(url) == "https://example.com"
    assert parser.get_page_path(url) == "https://example.com/blog/post/"

    # Test URL without path
    url_no_path = "https://example.com"
    assert parser.get_base_url(url_no_path) == "https://example.com"
    assert parser.get_page_path(url_no_path) == "https://example.com"