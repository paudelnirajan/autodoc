import abc
import os
from groq import Groq

# ---- Interface (Contract) ----

class ILLMService(abc.ABC):
    """
    An interface for a service that can make requests to an LLM.
    This defines our internal, application-specific contract, supporting both generation and evaluation tasks.
    """
    @abc.abstractmethod
    def create_completion(self, prompt: str) -> str:
        """
        Generates a text completion based on the input prompt.
        """
        pass

    @abc.abstractmethod
    def evaluate_docstring(self, code: str, docstring: str) -> bool:
        """
        Asks the LLM to evaluate if a docstring is high quality for the given code.
        Returns True if the docstring is deemed good, False otherwise.
        """
        pass

# --- Implementation (Adapter) ---

class GroqAdapter(ILLMService):
    """
    An adapter for the Groq API. It "adapts" the `groq` library to fit the simple `ILLMService` interface our applciation uses.
    """

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        if not api_key:
            raise ValueError("Groq API key is required.")
        self.client = Groq(api_key=api_key)
        self.model = model

        # TODO: make the model selection like the API_KEY

    def create_completion(self, prompt: str) -> str:
        """
        Handles the specific logic for calling the Groq Chat Completions endpoint.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return ""

    def evaluate_docstring(self, code: str, docstring: str) -> bool:
        """
        Implements the LLM-powered evaluation logic using a specific prompt.
        """
        prompt = f"""
        Analyze the following Python code and its docstring.
        Is the docstring a high-quality, descriptive, and helpful documentation for the code?
        A good docstring explains what the code does, its arguments (if any), what it returns. A bad docstring is either too generic or completely irrevalent.

        Code:
        ```python
        {code}
        ```

        Docstring:
        ```
        {docstring}
        ```

        Answer with a single word: YES or NO.
        """
        try:
            response = self.create_completion(prompt)
            return "yes" in response.lower().strip()
            
        except Exception as e:
            print(f"Error during docstring evaluation: {e}")
            return True