import urllib.parse
from typing import Any, Optional
from pydantic import BaseModel

from .config import ScrapeConfig
from .exceptions import ConfigurationError, ExtractionError, ScrapeGenError, ScrapingError
from .extractors.content import ContentExtractor
from .extractors.info_extractor import InfoExtractorAi
from .manager.llm_manager import LlmManager
from .models.llm import LlmType
from .scrapers.anchor import AnchorScraper
from .scrapers.url import URLScraper
from .scrapers.website import WebsiteScraper
from .utils.normalizer import UrlNormalizer
from .utils.url_parser import UrlParser
class ScrapeGen:
    """A class for web scraping and data extraction using AI.

    This class combines web scraping capabilities with AI-powered data extraction
    to collect and structure information from websites according to a specified model.

    Attributes:
        api_key (str): API key for the AI service.
        config (ScrapeConfig): Configuration settings for scraping.
        _scraper (Optional[WebsiteScraper]): Instance of WebsiteScraper.
        _extractor (Optional[InfoExtractorAi]): Instance of InfoExtractorAi.
    """

    def __init__(self, api_key: str, model , config: Optional[ScrapeConfig] = None):
        """Initialize ScrapeGen with API key and optional configuration.

        Args:
            api_key (str): API key for the AI service.
            config (Optional[ScrapeConfig]): Configuration settings for scraping.

        Raises:
            ConfigurationError: If api_key is empty or invalid.
        """
        if not api_key or not isinstance(api_key, str):
            raise ConfigurationError("Valid API key is required")
        
        self.api_key = api_key
        self.config = config or ScrapeConfig()
        self._scraper = None
        self._extractor = None
        self.model = model

    def _initialize_components(self, base_model: BaseModel) -> None:
        """Initialize scraper and extractor components.

        Args:
            base_model (BaseModel): The Pydantic model for data extraction.
        """
        if not self._scraper:
            self._scraper = WebsiteScraper(
                UrlNormalizer(),
                AnchorScraper(),
                UrlParser(),
                URLScraper(),
                ContentExtractor()
            )

        if not self._extractor:
            self._extractor = InfoExtractorAi(
                basemodel=base_model,
                llm_manager=LlmManager(LlmType(is_gemini=True), api_key=self.api_key , model=self.model),
            )

    def _validate_url(self, url: str) -> None:
        """Validate the provided URL.

        Args:
            url (str): URL to validate.

        Raises:
            ConfigurationError: If URL is invalid.
        """
        if not url or not isinstance(url, str):
            raise ConfigurationError("Valid URL is required")
        
        try:
            result = urllib.parse.urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ConfigurationError("Invalid URL format")
        except Exception as e:
            raise ConfigurationError(f"URL validation failed: {str(e)}")

    def scrape(self, url: str , base_model: BaseModel, prompt: str = None ,**kwargs: Any) -> Any:
        """Scrape website and extract data according to the specified model.

        Args:
            url (str): URL to scrape.
            base_model (BaseModel): Pydantic model defining the data structure.
            **kwargs: Additional arguments to override default configuration.

        Returns:
            Any: Extracted data in the format specified by base_model.

        Raises:
            ScrapingError: If scraping fails.
            ExtractionError: If data extraction fails.
        """
        try:
            self._validate_url(url)
            self._initialize_components(base_model)

            # Update config with any provided kwargs
            config_dict = {**self.config.__dict__, **kwargs}
            
            try:
                content = self._scraper.scrape(
                    url,
                    max_page=config_dict['max_pages'],
                    max_subpage=config_dict['max_subpages'],
                    max_depth=config_dict['max_depth']
                )
            except Exception as e:
                raise ScrapingError(f"Scraping failed: {str(e)}")

            if not content:
                raise ScrapingError("No content was scraped from the URL")

            try:
                data = self._extractor.extract(content , prompt=prompt)
                return data
            except Exception as e:
                raise ExtractionError(f"Data extraction failed: {str(e)}")

        except ScrapeGenError:
            raise
        except Exception as e:
            raise ScrapeGenError(f"Unexpected error: {str(e)}")

    def update_config(self, **kwargs: Any) -> None:
        """Update scraping configuration.

        Args:
            **kwargs: Configuration parameters to update.

        Raises:
            ConfigurationError: If invalid configuration parameters are provided.
        """
        try:
            current_config = self.config.__dict__.copy()
            current_config.update(kwargs)
            self.config = ScrapeConfig(**current_config)
        except Exception as e:
            raise ConfigurationError(f"Invalid configuration: {str(e)}")
