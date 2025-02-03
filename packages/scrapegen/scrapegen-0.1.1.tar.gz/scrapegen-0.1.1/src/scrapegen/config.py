from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class ScrapeConfig:
    """Configuration settings for web scraping.

    Attributes:
        max_pages (int): Maximum number of pages to scrape per depth level.
        max_subpages (int): Maximum number of subpages to scrape per page.
        max_depth (int): Maximum depth to follow links.
        timeout (int): Request timeout in seconds.
        retries (int): Number of times to retry failed requests.
        user_agent (str): User agent string for requests.
        headers (Optional[Dict[str, str]]): Additional HTTP headers.
    """
    max_pages: int = 20
    max_subpages: int = 2
    max_depth: int = 1
    timeout: int = 30
    retries: int = 3
    user_agent: str = "Mozilla/5.0 (compatible; ScrapeGen/1.0)"
    headers: Optional[Dict[str, str]] = None

