
from abc import ABC, abstractmethod


class Normalizer(ABC):
    """
Abstract base class for normalizing data.

This class defines the interface for normalization operations. 
Subclasses must implement the `normalize` method to provide 
specific normalization logic.
"""
    @abstractmethod
    def normalize():
        pass


class UrlNormalizer(Normalizer):
    """
    A class for normalizing URLs by converting relative links to absolute URLs.

    This class extends the Normalizer abstract base class and provides a 
    static method to normalize links based on the given base URL and page path.

    Methods:
        normalize(link: str, base_url: str, page_path: str) -> str:
            Converts a relative link to an absolute URL using the base URL 
            and page path.

    Attributes:
        None
    """
    @staticmethod
    def normalize(link: str, base_url: str, page_path: str) -> str:
        """
        Normalizes relative links into absolute URLs.
        :param link: The link to normalize (could be relative or absolute).
        :param base_url: The base URL for relative links starting with '/'.
        :param page_path: The page path for relative links not starting with '/'.
        :return: The normalized link as an absolute URL.
        """
        if link.startswith('/'):
            return base_url + link
        if not link.startswith('http'):
            return page_path + link
        return link

