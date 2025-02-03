
from typing import Optional

import requests

from .base import Scraper
import requests.exceptions as request_exception


class URLScraper(Scraper):
    """Scrapes the content of a given URL.

    Args:
        url (str): The URL of the web page to scrape.

    Returns:
        str: The HTML content of the web page.

    Raises:
        request_exception.RequestException: If there is an error during the request.
        request_exception.MissingSchema: If the URL schema is missing.
        request_exception.ConnectionError: If there is a connection error.
    """
    @staticmethod
    def scrape(url: str) -> Optional[str]:  # Add Optional to return type hint
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except (
            request_exception.RequestException,
            request_exception.MissingSchema,
            request_exception.ConnectionError,
            Exception  # Add general Exception to catch all errors
        ) as e:
            print(f'There was a request error: {str(e)}')
            return None

