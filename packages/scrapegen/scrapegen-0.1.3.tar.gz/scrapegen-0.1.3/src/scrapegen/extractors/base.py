from abc import ABC, abstractmethod


class Extractor(ABC):
    """Abstract method to extract data.

        This method must be implemented by subclasses to define
        the specific extraction logic.
        """
    @abstractmethod
    def extract():
        pass
