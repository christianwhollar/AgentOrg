from llms.llm import LLM
import openai
import os
import tiktoken
from typing import List, Dict
from rich.text import Text

class ChatGPT35Turbo(LLM):

    def __init__(self, system_prompt: str) -> None:

        self.api_key: str = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        openai.api_key = self.api_key

        self.messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

    def get_response(self, input_prompt: str) -> str:
        self.update_token_usage(input_prompt)

        self.messages.append(
            {
                "role": 'user',
                "content": input_prompt
            }
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )
        except Exception as e:
            return f"An error occurred: {e}"

        content = response["choices"][0]["message"]["content"]

        self.messages.append(
            {
                "role": 'assistant',
                "content": content
            }
        )

        return content

    @property
    def token_file_name(self) -> str:
        return "chatgpt35turbo/chatgpt35turbo.txt"

    @property
    def cost_per_token(self) -> float:
        return 0.002 / 1000

    def count_tokens(self, text: str) -> int:
        encoder = tiktoken.get_encoding("cl100k_base")
        tokenized_text = encoder.encode(text)
        return len(tokenized_text)

    def __rich__(self) -> Text:
        return Text(f"ChatGPT35Turbo: Token File Name = {self.token_file_name}, Cost Per Token = {self.cost_per_token}")
