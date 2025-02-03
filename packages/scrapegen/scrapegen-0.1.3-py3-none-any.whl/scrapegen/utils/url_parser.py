from abc import ABC, abstractmethod

import urllib


class UrlParserInterface(ABC):
    """Interface for parsing URLs, providing methods to extract the base URL and page path."""
    @staticmethod
    @abstractmethod
    def get_base_url(url: str) -> str:

        """Extracts the base URL (scheme and netloc) from a given URL."""

    @staticmethod
    @abstractmethod
    def get_page_path(url: str) -> str:

        """Extracts the page path from the given URL."""


class UrlParser(UrlParserInterface):
    """
A concrete implementation of the UrlParserInterface for parsing URLs.

This class provides methods to extract the base URL and page path from a given URL.
"""
    @staticmethod
    def get_base_url(url: str) -> str:
        """
        Extracts the base URL (scheme and netloc) from a given URL.
        :param url: The full URL from which to extract the base.
        :return: The base URL in the form 'scheme://netloc'.
        """
        parts = urllib.parse.urlsplit(url)
        return '{0.scheme}://{0.netloc}'.format(parts)

    @staticmethod
    def get_page_path(url: str) -> str:
        """
        Extracts the page path from the given URL, used to normalize relative links.
        :param url: The full URL from which to extract the page path.
        :return: The page path (URL up to the last '/').
        """
        parts = urllib.parse.urlsplit(url)
        return url[: url.rfind('/') + 1] if '/' in parts.path else url

