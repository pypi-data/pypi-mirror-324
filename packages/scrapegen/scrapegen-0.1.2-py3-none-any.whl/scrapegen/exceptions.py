class ScrapeGenError(Exception):
    """Base exception class for ScrapeGen errors."""
    pass

class ConfigurationError(ScrapeGenError):
    """Raised when there's an error in the configuration."""
    pass

class ScrapingError(ScrapeGenError):
    """Raised when there's an error during the scraping process."""
    pass

class ExtractionError(ScrapeGenError):
    """Raised when there's an error during the data extraction process."""
    pass

