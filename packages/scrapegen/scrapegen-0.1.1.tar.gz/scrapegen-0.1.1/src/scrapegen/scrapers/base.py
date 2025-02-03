
from abc import ABC, abstractmethod


class Scraper(ABC):
    """Abstract method to perform web scraping.

    This method should be implemented by subclasses to define
    the specific scraping logic for extracting data from web pages.
    """
    @abstractmethod
    def scrape():
        pass