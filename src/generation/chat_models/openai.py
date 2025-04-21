import os

from openai import AsyncOpenAI
from typing import List, Optional, Any
from .base import BaseChatModel, ChatMessage


class OpenAIChatModel(BaseChatModel):
    def __init__(self, model_name: str):
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model_name = model_name

    async def invoke(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[msg.dict() for msg in messages],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message["content"]
