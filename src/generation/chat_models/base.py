from abc import ABC, abstractmethod
from typing import List, Optional, Any
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class BaseChatModel(ABC):
    """Abstract base class for all chat models."""

    @abstractmethod
    async def invoke(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Generate a completion from a list of messages."""
        pass
