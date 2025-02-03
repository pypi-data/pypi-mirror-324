
from typing import List
from bs4 import BeautifulSoup
import urllib

from .base import Scraper

class AnchorScraper(Scraper):
    """Extracts and returns a list of absolute URLs from anchor tags in the given HTML content.

    Args:
        content (str): The HTML content to parse for anchor tags.
        baseUrl (str): The base URL to resolve relative URLs found in anchor tags.

    Returns:
        List[str]: A list of absolute URLs extracted from the anchor tags.

    Raises:
        Exception: If the provided content is null.
    """
    @staticmethod
    def scrape(content: str, baseUrl: str) -> List[str]:
        if content:
            soup = BeautifulSoup(content, 'lxml')
            return [
                urllib.parse.urljoin(baseUrl, anchor.get("href"))
                for anchor in soup.find_all("a")
                if anchor.get("href")
            ]
        raise Exception("The given content is null")
