"""
Module: OpenAI LLM Implementation
Implements the OpenAI Large Language Model with specific configurations.
"""

import json
import os
from typing import List

import openai
from dotenv import load_dotenv

from generation.llms.base_llm import BaseLLM

# Load environment variables
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAILLM(BaseLLM):
    """
    A concrete implementation of the BaseLLM interface for OpenAI's LLM.

    Attributes:
        prompt (dict[str]): The prompt template for the LLM.
        prompt_inputs (List[str]): List of required input keys for the prompt.
        instructions (str): Additional instructions for the system role.
        format_json (bool): Flag to indicate if the output should be JSON.
        language (str): The language for the prompt, defaults to 'fra'.
    """

    def __init__(
        self,
        prompt: dict[str, str],
        prompt_inputs: List[str],
        instructions: str | None,
        format_json: bool,
        language: str = "fra",
    ):
        self.prompt: str = prompt[language]
        self.prompt_inputs: List[str] = prompt_inputs
        self.instructions: str = instructions or ""
        self.format_json: bool = format_json
        self.model: str = "gpt-3.5-turbo"

    def invoke(self, inputs: dict[str, str]) -> str:
        """
        Generates a response from OpenAI's LLM based on the given inputs.

        Parameters:
            inputs (dict[str, str]): A dictionary containing input key-value pairs.

        Returns:
            str: The generated response from the LLM.
        """
        missing_keys: set = set(self.prompt_inputs) - set(inputs.keys())
        if missing_keys:
            raise ValueError(f"Input dict should contain {self.prompt_inputs} keys")

        formatted_prompt: str = self.prompt.format(**inputs)

        messages: list[dict[str, str]] = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": formatted_prompt},
        ]

        kwargs: dict = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
        }

        if self.format_json:
            kwargs["response_format"] = "json"

        response: openai.ChatCompletion = openai.ChatCompletion.create(**kwargs)

        result: str = response.choices[0].message.content

        if self.format_json:
            return json.loads(result)
        return result
