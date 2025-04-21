import os
from typing import List, Optional, Any

from langchain_core.messages import AnyMessage
from openai import AsyncOpenAI

from .base import BaseChatModel

from dotenv import load_dotenv

load_dotenv()


class OpenAIChatModel(BaseChatModel):
    """OpenAI Chat Model using OpenAI API."""

    def initialize_client(self):
        """Initialize the OpenAI client."""
        return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def invoke(
        self,
        messages: List[AnyMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        """Generate a completion from a list of messages."""
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=self.format_messages(messages),
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        return self.get_content_from_response(response)

    def format_messages(self, messages: List[AnyMessage]) -> List[dict]:
        """Format messages for OpenAI API."""
        return [
            {
                "role": self.get_openai_role_from_langchain_type(msg.type),
                "content": msg.content,
            }
            for msg in messages
        ]

    @staticmethod
    def get_openai_role_from_langchain_type(
        message_type: str,
    ) -> str:
        """Map Langchain message type to OpenAI API role."""
        if message_type == "system":
            return "developer"
        elif message_type == "human":
            return "user"
        elif message_type == "ai":
            return "assistant"
        else:
            raise ValueError(f"Unknown message type: {message_type}")

    @staticmethod
    def get_content_from_response(response: Any) -> str:
        """Extract content from OpenAI API response."""
        return response.choices[0].message.content
