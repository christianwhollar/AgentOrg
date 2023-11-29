import os
import json
import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)

class LLM(ABC):
    """
    Abstract base class for language model interactions. 
    This class defines the structure and required methods for derived classes 
    which implement specific language model functionalities.
    """
    
    @property
    @abstractmethod
    def token_file_name(self) -> str:
        """
        Abstract property that should return the filename for storing token usage information.
        """
        pass

    @property
    def token_file_path(self) -> str:
        """
        Returns the full path of the token file, based on the token file name.
        """
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), self.token_file_name)

    @property
    @abstractmethod
    def cost_per_token(self) -> float:
        """
        Abstract property for the cost per token.
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Abstract method to count the number of tokens in a given text.

        Args:
        text (str): The text to be tokenized and counted.

        Returns:
        int: The number of tokens in the text.
        """
        pass

    def update_token_usage(self, prompt: str) -> None:
        """
        Update the token count and total cost in the token file based on the new prompt.

        Args:
        prompt (str): The prompt text for which tokens are to be counted and added.
        """
        try:
            if os.path.exists(self.token_file_path):
                with open(self.token_file_path, "r") as file:
                    data = json.load(file)
            else:
                data = {"total_tokens": 0, "total_cost": 0.0}

            token_count = self.count_tokens(prompt)
            data["total_tokens"] += token_count
            data["total_cost"] = data["total_tokens"] * self.cost_per_token

            with open(self.token_file_path, "w") as file:
                json.dump(data, file, indent=4)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error updating token usage: {e}")

    @abstractmethod
    def get_response(self, user_input: str) -> str:
        """
        Abstract method to get a response from the model based on user input.

        Args:
        user_input (str): The input string from the user.

        Returns:
        str: The response from the model.
        """
        pass