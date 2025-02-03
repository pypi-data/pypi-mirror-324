from http.client import HTTPException
import json
from .base import Extractor
from ..manager.llm_manager import LlmManager
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Type

class InfoExtractorAi(Extractor):
    """
    Extracts structured information from given content using a language model.

    Attributes:
        basemodel (Type): The Pydantic model used for parsing extracted data.
        llm_manager (LlmManager): Manages the language model instance.
    """
    
    def __init__(self, basemodel: Type, llm_manager: LlmManager):
        super().__init__()
        self.basemodel = basemodel
        self.llm_manager = llm_manager

    def extract(self, content: str, prompt: str = None):
        """
        Extracts structured data from the provided content using a language model.

        Args:
            content (str): The raw content to process and extract.
            prompt (str, optional): Custom prompt template. Defaults to predefined prompt.

        Returns:
            An instance of the base model containing the structured data.

        Raises:
            HTTPException: If extraction fails.
        """
        default_prompt = """
        You have been given a list of company data. Your job is to extract and format the company's details
        based on the following fields:
        ('Artificial Intelligence'), ('Web Development'), ('Cybersecurity'), ('Blockchain'),
        ('Cloud Computing'), ('Data Science'), ('E-commerce'), ('FinTech'), ('Healthcare Technology'),
        ('EdTech'), ('IoT'), ('VR/AR'), ('Gaming'), ('Robotics'), ('Marketing Technology'),
        ('Social Media'), ('Green Energy'), ('Manufacturing Tech'), ('Automotive Tech'), ('Biotech').
        """
        
        try:
            parser = PydanticOutputParser(pydantic_object=self.basemodel)
            prompt_template = PromptTemplate(
                template=f"{prompt or default_prompt}\n{{format_instructions}}",
                input_variables=["info"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )
            
            llm = self.llm_manager.create_instance()
            response = llm.invoke(prompt_template.format(info=content))
            content_str = response.content.strip()

            print(f"Extracted content: {content_str}")

            # Extract JSON payload from formatted response
            if "```json" in content_str:
                content_str = content_str.split("```json")[1].split("```")[0].strip()
            
            output_data = json.loads(content_str)
            return self.basemodel(**output_data)
        
        except json.JSONDecodeError as json_err:
            raise HTTPException(status_code=500, detail=f"JSON parsing error: {str(json_err)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
