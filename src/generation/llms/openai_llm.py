import json
import os
from typing import List

import openai
from dotenv import load_dotenv

from generation.llms.base_llm import BaseLLM

# Load env variables
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAILLM(BaseLLM):
    def __init__(
        self,
        prompt: dict[str],
        prompt_inputs: List[str],
        instructions: str | None,
        format_json: bool,
        language: str = "fra",
    ):
        self.prompt = prompt[language]
        self.prompt_inputs = prompt_inputs
        self.instructions = instructions or ""
        self.format_json = format_json
        self.model = "gpt-3.5-turbo"

    def invoke(self, inputs: dict[str, str]) -> str:
        missing_keys = set(self.prompt_inputs) - set(inputs.keys())
        if missing_keys:
            raise ValueError(f"Input dict should contain {self.prompt_inputs} keys")

        formatted_prompt = self.prompt.format(**inputs)

        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": formatted_prompt},
        ]

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
        }

        if self.format_json:
            kwargs["response_format"] = "json"

        response = openai.ChatCompletion.create(**kwargs)

        result = response.choices[0].message.content

        if self.format_json:
            return json.loads(result)
        return result
