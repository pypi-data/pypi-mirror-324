from http.client import HTTPException
import json
from .base import Extractor
from ..manager.llm_manager  import LlmManager
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

class InfoExtractorAi(Extractor):
    """
Extracts information from the provided content using a language model and a base model.

Initializes with a base model and a language model manager. The `extract` method
formats the content using a prompt template and invokes the language model to
generate a response. The response is parsed and returned as an instance of the
base model. Raises an HTTPException if extraction fails.

Attributes:
    basemodel: The base model used for parsing the extracted data.
    llm_manager (LlmManager): Manages the language model instance.

Methods:
    extract(content: str): Extracts and returns structured data from the content.
"""
    def __init__(self, basemodel , llm_manager):
        super().__init__()
        self.basemodel = basemodel
        self.llm_manager : LlmManager = llm_manager

    def extract(self, content: str):
        """
        Extracts structured data from the provided content using a language model.

        This method formats the input content with a prompt template and invokes
        a language model to generate a structured response. The response is parsed
        into a JSON format and returned as an instance of the base model. Raises
        an HTTPException if the extraction process fails.

        Args:
            content (str): The raw content to be processed and extracted.

        Returns:
            An instance of the base model containing the structured data.

        Raises:
            HTTPException: If the extraction process encounters an error.
        """
        # extracts the content based on the given basemodel
        try:
            parser = PydanticOutputParser(pydantic_object=self.basemodel)
            prompt = PromptTemplate(
                template="""
                    You have given below the list of company data your job is to return the compaies data
                Format the response according to these instructions:
                {format_instructions}
                """,
                input_variables=["comapnyInfo"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )
        
            llm = self.llm_manager.create_instance()
            response = llm.invoke(
                prompt.format(
                    comapnyInfo=content,
            ))
        
            content = response.content
            print(f" content is {content}")
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            output = json.loads(content)
            return self.basemodel(**output)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate project tasks: {str(e)}"
            )
            