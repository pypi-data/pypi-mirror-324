
from pydantic import BaseModel


class LlmType(BaseModel):
    """
Represents the type of a language model (LLM) with a flag indicating if it is a Gemini model.

Attributes:
    is_gemini (bool): A flag that specifies whether the LLM is a Gemini model. Defaults to False.
"""
    is_gemini: bool = False