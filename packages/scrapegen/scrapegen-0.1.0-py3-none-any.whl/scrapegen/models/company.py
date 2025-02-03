
### This class is created as an example 
from typing import List, Optional

from pydantic import BaseModel


class CompanyInfo(BaseModel):
    """
Represents information about a company.

Attributes:
    company_name (Optional[str]): The name of the company.
    company_description (Optional[str]): A brief description of the company.
    funding_amount (Optional[str]): The amount of funding the company has received.
    ceo_name (Optional[str]): The name of the company's CEO.
    company_url (Optional[str]): The URL of the company's website.
"""
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    funding_amount: Optional[str] = None
    ceo_name: Optional[str] = None
    company_url: Optional[str] = None

### This class is created as an example 
class CompaniesInfo(BaseModel):
    """
Represents a collection of company information.

Attributes:
    companies (List[CompanyInfo]): A list of CompanyInfo objects containing details about various companies.
"""
    companies: List[CompanyInfo]
