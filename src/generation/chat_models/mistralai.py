from mistralai import Mistral
from typing import List, Optional, Any
from .base import BaseChatModel, ChatMessage


class MistralAIChatModel(BaseChatModel):
    def __init__(self, model_name: str = "mistral-medium", api_key: str = ""):
        self.client = Mistral(api_key=api_key)
        self.model_name = model_name

    async def invoke(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        response = await self.client.chat.complete_async(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
