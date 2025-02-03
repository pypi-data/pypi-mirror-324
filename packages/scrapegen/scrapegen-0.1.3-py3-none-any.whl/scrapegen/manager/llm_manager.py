from langchain_google_genai import ChatGoogleGenerativeAI

from ..models import LlmType



class SupportedModels:
    """
    Manages a list of supported language models and provides validation functionality.

    Attributes:
        models (set): A set of supported model names.
    """

    def __init__(self):
        # Initialize with supported models
        self.models = {
            "gemini-1.5-flash-8b",
            "gemini-1.5-pro",
            "gemini-2.0-flash-exp",
            "gemini-1.5-flash"
        }

    def is_model_supported(self, model: str) -> bool:
        """
        Check if a given model is supported.

        Args:
            model (str): The name of the model to check.

        Returns:
            bool: True if the model is supported, False otherwise.
        """
        return model in self.models

    def get_supported_models(self) -> set:
        """
        Get the list of supported models.

        Returns:
            set: A set of supported model names.
        """
        return self.models

class LlmManager:
    """
    Manages the creation and retrieval of a language model (LLM) instance.

    Attributes:
        llm (LlmType): The type of LLM to manage, indicating if it is a Gemini model.
        instance (Optional[ChatGoogleGenerativeAI]): The LLM instance, initialized if it is a Gemini model.
        api_key (str): The API key used for authentication with the LLM service.
        model (str): The name of the model to use.
        supported_models (SupportedModels): An instance of SupportedModels for validation.
    """

    def __init__(self, llm_type: LlmType, api_key: str, model: str):
        """
        Initialize the LlmManager.

        Args:
            llm_type (LlmType): The type of LLM to manage.
            api_key (str): The API key for the LLM service.
            model (str): The name of the model to use.

        Raises:
            ValueError: If the API key is invalid or the model is not supported.
        """
        if not api_key or not isinstance(api_key, str):
            raise ValueError("A valid API key is required.")

        self.llm = llm_type
        self.api_key = api_key
        self.model = model
        self.instance = None
        self.supported_models = SupportedModels()

        # Validate the model
        if not self.supported_models.is_model_supported(self.model):
            raise ValueError(
                f"Model '{self.model}' is not supported. Supported models: {self.supported_models.get_supported_models()}"
            )

    def create_instance(self):
        """
        Create and return an instance of the LLM.

        Returns:
            ChatGoogleGenerativeAI: An instance of the LLM.

        Raises:
            RuntimeError: If the LLM type is not supported or initialization fails.
        """
        if self.llm.is_gemini:
            if not self.instance:
                try:
                    self.instance = ChatGoogleGenerativeAI(
                        model=self.model,
                        google_api_key=self.api_key,
                        temperature=0.0,
                    )
                except Exception as e:
                    raise RuntimeError(f"Failed to initialize LLM: {str(e)}")
            return self.instance
        else:
            raise RuntimeError("Only Gemini models are currently supported.")
