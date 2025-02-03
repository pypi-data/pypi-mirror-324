
from typing import List
from ..extractors.base import Extractor
from  .url import URLScraper
from ..utils.url_parser import UrlParserInterface
from ..utils.normalizer import Normalizer
from .base import Scraper


class WebsiteScraper(Scraper):
    """
        Scrapes a website starting from the given URL, follows links, and collects content.

        Args:
            start_url (str): The initial URL to start scraping.
            max_page (int, optional): The maximum number of pages to scrape per depth level. Defaults to 20.
            max_subpage (int, optional): The maximum number of subpages to scrape per page. Defaults to 2.
            max_depth (int, optional): The maximum depth to follow links. Defaults to 1.
            current_depth (int, optional): The current depth level of scraping. Defaults to 0.

        Returns:
            set[str]: A set of content extracted from the scraped pages.
        """
    def __init__(self, normalizer, anchorScraper, urlParser, urlScraper, contentExtractor):
        self.normalizer: Normalizer = normalizer
        self.anchorScraper: Scraper = anchorScraper
        self.urlParser: UrlParserInterface = urlParser
        self.urlScraper: URLScraper = urlScraper
        self.contentExtractor: Extractor = contentExtractor
        self.content_list = []
        self.scraped_urls = set()
    def scrape(
        self,
        start_url: str,
        max_page: int = 20,
        max_subpage: int = 2,
        max_depth: int = 1,
        current_depth=0,
    ) -> List[List[str]]:  # Update return type hint
        if max_depth <= current_depth:
            return self.content_list
            
        try:
            count = 0
            base_url = self.urlParser.get_base_url(start_url)
            # get all the subUrls in the url (Page)
            page_content = self.urlScraper.scrape(start_url)
            if not page_content:  # Add check for None
                return self.content_list
                
            links = self.anchorScraper.scrape(page_content, base_url)
            urls_to_process = [link for link in links if link not in self.scraped_urls]

            print(f"processing urls {urls_to_process[:max_page]}")
            urls_to_process = urls_to_process[:max_page]
            
            for url in urls_to_process:
                try:
                    self.scraped_urls.add(url)
                    print(f'[{count}] Processing {url}')
                    # content of the sub-links in the main given url
                    content = self.urlScraper.scrape(url)
                    # skip if the content is None
                    if not content:
                        continue
                        
                    self.content_list.append(self.contentExtractor.extract(content))
                    # list of links present in the content of the sub-link
                    links = self.anchorScraper.scrape(content, base_url)
                    max_depth_links = links[:max_subpage]
                    
                    for link in max_depth_links:
                        try:
                            # add all the content of the following link into the content_list
                            link_content = self.urlScraper.scrape(link)
                            if link_content:  # Add check for None
                                self.content_list.extend(self.contentExtractor.extract(link_content))
                        except Exception as e:
                            print(f"Error processing sublink {link}: {str(e)}")
                            continue
                            
                    count += 1
                except Exception as e:
                    print(f"Error processing URL {url}: {str(e)}")
                    continue
                    
            return self.content_list
            
        except Exception as e:
            print(f"Error in scrape method: {str(e)}")
            return self.content_list  # Return empty list on error
