
    
from bs4 import BeautifulSoup
from .base import Extractor


class ContentExtractor(Extractor):
    """Extracts text content from specified HTML tags in the given content.

Args:
    content (str): The HTML content to extract text from.

Returns:
    List[str]: A list of extracted text from the specified tags.
"""
    def __init__(self):
        self.tags = ["a", "h1", "p", "h2", "h3"]
        self.allTagsContent = []

    def extract(self, content: str):
        """Extracts text content from specific HTML tags."""
        extracted_content = []  # Store extracted text
        
        soup = BeautifulSoup(content, 'lxml')

        for tag in self.tags:
            for tag_in in soup.find_all(tag):
                text = tag_in.get_text(strip=True)  # Extract text from the tag
                extracted_content.append(text)
                self.allTagsContent.append(text)  # Save it in class variable
        return extracted_content
        