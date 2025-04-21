from abc import ABC, abstractmethod
from typing import List, Optional, Any

from langchain_core.messages import AnyMessage


class BaseChatModel(ABC):
    """Abstract base class for all chat models."""

    def __init__(self, model_name: str):
        """Initialize the chat model with a model name."""
        self.model_name = model_name

        self.client = self.initialize_client()

    @abstractmethod
    def initialize_client(self):
        """Initialize the client for the chat model."""
        ...

    @abstractmethod
    async def invoke(
        self,
        messages: List[AnyMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        """Generate a completion from a list of messages."""
        ...
