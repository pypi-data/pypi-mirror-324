# ScrapeGen

<img src="https://github.com/user-attachments/assets/2f458a05-66f9-47a4-bc40-6069e3c9e849" alt="Logo" width="80" height="80">

ScrapeGen 🚀 is a powerful Python library that combines web scraping with AI-driven data extraction to collect and structure information from websites efficiently. It leverages Google's Gemini models for intelligent data processing and provides a flexible, configurable framework for web scraping operations.

## ✨ Features

- **🤖 AI-Powered Data Extraction**: Utilizes Google's Gemini models for intelligent parsing
- **⚙️ Configurable Web Scraping**: Supports depth control and flexible extraction rules
- **📊 Structured Data Modeling**: Uses Pydantic for well-defined data structures
- **🛡️ Robust Error Handling**: Implements retry mechanisms and detailed error reporting
- **🔧 Customizable Scraping Configurations**: Adjust settings dynamically based on needs
- **🌐 Comprehensive URL Handling**: Supports both relative and absolute URLs
- **📦 Modular Architecture**: Ensures clear separation of concerns for maintainability

## 📥 Installation

```bash
pip install scrapegen
```

## 📌 Requirements

- Python 3.7+
- Google API Key (for Gemini models)
- Required Python packages:
  - requests
  - beautifulsoup4
  - langchain
  - langchain-google-genai
  - pydantic

## 🚀 Quick Start with Custom Prompts

```python
from scrapegen import ScrapeGen, CompanyInfo, CompaniesInfo

# Initialize ScrapeGen with your Google API key
scraper = ScrapeGen(api_key="your-google-api-key", model="gemini-1.5-pro")

# Define target URL and custom prompt
url = "https://example.com"
custom_prompt = """
Analyze the website content and extract:
- Company name
- Core technologies
- Industry focus areas
- Key product features
"""

# Scrape with custom prompt and model
companies_data = scraper.scrape(
    url=url,
    prompt=custom_prompt,
    base_model=CompaniesInfo
)

# Display extracted data
for company in companies_data.companies:
    print(f"🏢 {company.company_name}")
    print(f"🔧 Technologies: {', '.join(company.core_technologies)}")
    print(f"📈 Focus Areas: {', '.join(company.industry_focus)}")
```

## ⚙️ Configuration

### 🔹 ScrapeConfig Options

```python
from scrapegen import ScrapeConfig

config = ScrapeConfig(
    max_pages=20,      # Max pages to scrape per depth level
    max_subpages=2,    # Max subpages to scrape per page
    max_depth=1,       # Max depth to follow links
    timeout=30,        # Request timeout in seconds
    retries=3,         # Number of retry attempts
    user_agent="Mozilla/5.0 (compatible; ScrapeGen/1.0)",
    headers=None       # Additional HTTP headers
)
```

### 🔄 Updating Configuration

```python
scraper = ScrapeGen(api_key="your-api-key", model="gemini-1.5-pro", config=config)

# Dynamically update configuration
scraper.update_config(max_pages=30, timeout=45)
```

## 📌 Custom Data Models

Define Pydantic models to structure extracted data:

```python
from pydantic import BaseModel
from typing import Optional, List

class CustomDataModel(BaseModel):
    title: str
    description: Optional[str]
    date: str
    tags: List[str]

class CustomDataCollection(BaseModel):
    items: List[CustomDataModel]

# Scrape using the custom model
data = scraper.scrape(url, CustomDataCollection)
```

## 🤖 Supported Gemini Models

- gemini-1.5-flash-8b
- gemini-1.5-pro
- gemini-2.0-flash-exp
- gemini-1.5-flash

## 🆕 Custom Prompt Engineering Guide

### 1️⃣ Basic Prompt Structure

```python
basic_prompt = """
Extract the following details from the content:
- Company name
- Founding year
- Headquarters location
- Main products/services
"""
```

### 2️⃣ Tech-Focused Extraction

```python
tech_prompt = """
Identify and categorize technologies mentioned in the content:
1. AI/ML Technologies
2. Cloud Infrastructure
3. Data Analytics Tools
4. Cybersecurity Solutions
Include version numbers and implementation details where available.
"""
```

### 3️⃣ Multi-Level Extraction

```python
multi_level_prompt = """
Perform hierarchical extraction:
1. Company Overview:
   - Name
   - Mission statement
   - Key executives
2. Technical Capabilities:
   - Core technologies
   - Development stack
   - Infrastructure
3. Market Position:
   - Competitors
   - Market share
   - Growth metrics
"""
```

## 📌 Specialized Prompt Examples

### 🔍 Competitive Analysis Prompt

```python
competitor_prompt = """
Identify and compare key competitors:
- Competitor names
- Feature differentiators
- Pricing models
- Market positioning
Output as a comparison table with relative strengths.
"""
```

### 🌱 Sustainability Focused Prompt

```python
green_prompt = """
Extract environmental sustainability information:
1. Green initiatives
2. Carbon reduction targets
3. Eco-friendly technologies
4. Sustainability certifications
5. Renewable energy usage
Prioritize quantitative metrics and timelines.
"""
```

### 💡 Innovation Tracking Prompt

```python
innovation_prompt = """
Analyze R&D activities and innovations:
- Recent patents filed
- Research partnerships
- New product launches (last 24 months)
- Technology breakthroughs
- Investment in R&D (% of revenue)
"""
```

## 🛠️ Prompt Optimization Tips

1. **Be Specific**: Clearly define required fields and formats

   ```python
   "Format output as JSON with 'company_name', 'employees', 'revenue' keys"
   ```
2. **Add Context**:

   ```python
   "Analyze content from CEO interviews for strategic priorities"
   ```
3. **Define Output Structure**:

   ```python
   "Categorize findings under 'basic_info', 'tech_stack', 'growth_metrics'"
   ```
4. **Set Priorities**:

   ```python
   "Focus on technical specifications over marketing content"
   ```

## ⚠️ Error Handling

ScrapeGen provides specific exception classes for detailed error handling:

- **❗ ScrapeGenError**: Base exception class
- **⚙️ ConfigurationError**: Errors related to scraper configuration
- **🕷️ ScrapingError**: Issues encountered during web scraping
- **🔍 ExtractionError**: Problems with AI-driven data extraction

Example usage:

```python
try:
    data = scraper.scrape(
        url=url,
        prompt=complex_prompt,
        base_model=MarketAnalysis
    )
except ExtractionError as e:
    print(f"🔍 Extraction failed with custom prompt: {e}")
    print(f"🧠 Prompt used: {complex_prompt}")
except ScrapingError as e:
    print(f"🌐 Scraping error: {str(e)}")
```

## 🏗️ Architecture

ScrapeGen follows a modular design for scalability and maintainability:

1. **🕷️ WebsiteScraper**: Handles core web scraping logic
2. **📑 InfoExtractorAi**: Performs AI-driven content extraction
3. **🤖 LlmManager**: Manages interactions with language models
4. **🔗 UrlParser**: Parses and normalizes URLs
5. **📥 ContentExtractor**: Extracts structured data from HTML elements

## ✅ Best Practices

### 1️⃣ Rate Limiting

- ⏳ Use delays between requests
- 📜 Respect robots.txt guidelines
- ⚖️ Configure max_pages and max_depth responsibly

### 2️⃣ Error Handling

- 🔄 Wrap scraping operations in try-except blocks
- 📋 Implement proper logging for debugging
- 🔁 Handle network timeouts and retries effectively

### 3️⃣ Resource Management

- 🖥️ Monitor memory usage for large-scale operations
- 📚 Implement pagination for large datasets
- ⏱️ Adjust timeout settings based on expected response times

## 🤝 Contributing

Contributions are welcome! 🎉 Feel free to submit a Pull Request to improve ScrapeGen.

## ✨ Features

- **🤖 AI-Powered Data Extraction**: Utilizes Google's Gemini models for intelligent parsing.
- **⚙️ Configurable Web Scraping**: Supports depth control and flexible extraction rules.
- **📊 Structured Data Modeling**: Uses Pydantic for well-defined data structures.
- **🛡️ Robust Error Handling**: Implements retry mechanisms and detailed error reporting.
- **🔧 Customizable Scraping Configurations**: Adjust settings dynamically based on needs.
- **🌐 Comprehensive URL Handling**: Supports both relative and absolute URLs.
- **📦 Modular Architecture**: Ensures clear separation of concerns for maintainability.

## 📥 Installation

```bash
pip install scrapegen  # Package name may vary
```

## 📌 Requirements

- Python 3.7+
- Google API Key (for Gemini models)
- Required Python packages:
  - requests
  - beautifulsoup4
  - langchain
  - langchain-google-genai
  - pydantic

## 🚀 Quick Start

```python
from scrapegen import ScrapeGen, CompanyInfo, CompaniesInfo

# Initialize ScrapeGen with your Google API key
scraper = ScrapeGen(api_key="your-google-api-key", model="gemini-1.5-pro")

# Define the target URL
url = "https://example.com"

# Scrape and extract company information
companies_data = scraper.scrape(url, CompaniesInfo)

# Display extracted data
for company in companies_data.companies:
    print(f"🏢 Company Name: {company.company_name}")
    print(f"📄 Description: {company.company_description}")
```

## ⚙️ Configuration

### 🔹 ScrapeConfig Options

```python
from scrapegen import ScrapeConfig

config = ScrapeConfig(
    max_pages=20,      # Max pages to scrape per depth level
    max_subpages=2,    # Max subpages to scrape per page
    max_depth=1,       # Max depth to follow links
    timeout=30,        # Request timeout in seconds
    retries=3,         # Number of retry attempts
    user_agent="Mozilla/5.0 (compatible; ScrapeGen/1.0)",
    headers=None       # Additional HTTP headers
)
```

### 🔄 Updating Configuration

```python
scraper = ScrapeGen(api_key="your-api-key", model="gemini-1.5-pro", config=config)

# Dynamically update configuration
scraper.update_config(max_pages=30, timeout=45)
```

## 📌 Custom Data Models

Define Pydantic models to structure extracted data:

```python
from pydantic import BaseModel
from typing import Optional, List

class CustomDataModel(BaseModel):
    title: str
    description: Optional[str]
    date: str
    tags: List[str]

class CustomDataCollection(BaseModel):
    items: List[CustomDataModel]

# Scrape using the custom model
data = scraper.scrape(url, CustomDataCollection)
```

## 🤖 Supported Gemini Models

- gemini-1.5-flash-8b
- gemini-1.5-pro
- gemini-2.0-flash-exp
- gemini-1.5-flash

## ⚠️ Error Handling

ScrapeGen provides specific exception classes for detailed error handling:

- **❗ ScrapeGenError**: Base exception class.
- **⚙️ ConfigurationError**: Errors related to scraper configuration.
- **🕷️ ScrapingError**: Issues encountered during web scraping.
- **🔍 ExtractionError**: Problems with AI-driven data extraction.

Example usage:

```python
try:
    data = scraper.scrape(url, CustomDataCollection)
except ConfigurationError as e:
    print(f"⚙️ Configuration error: {e}")
except ScrapingError as e:
    print(f"🕷️ Scraping error: {e}")
except ExtractionError as e:
    print(f"🔍 Extraction error: {e}")
```

## 🏗️ Architecture

ScrapeGen follows a modular design for scalability and maintainability:

1. **🕷️ WebsiteScraper**: Handles core web scraping logic.
2. **📑 InfoExtractorAi**: Performs AI-driven content extraction.
3. **🤖 LlmManager**: Manages interactions with language models.
4. **🔗 UrlParser**: Parses and normalizes URLs.
5. **📥 ContentExtractor**: Extracts structured data from HTML elements.

## ✅ Best Practices

### 1️⃣ Rate Limiting

- ⏳ Use delays between requests.
- 📜 Respect robots.txt guidelines.
- ⚖️ Configure max_pages and max_depth responsibly.

### 2️⃣ Error Handling

- 🔄 Wrap scraping operations in try-except blocks.
- 📋 Implement proper logging for debugging.
- 🔁 Handle network timeouts and retries effectively.

### 3️⃣ Resource Management

- 🖥️ Monitor memory usage for large-scale operations.
- 📚 Implement pagination for large datasets.
- ⏱️ Adjust timeout settings based on expected response times.

## 🤝 Contributing

Contributions are welcome! 🎉 Feel free to submit a Pull Request to improve ScrapeGen.
