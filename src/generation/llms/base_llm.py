"""Vector store utilities."""

from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """LLM model interface."""

    @abstractmethod
    async def invoke(self, inputs: dict[str, str]) -> str:
        """Generate."""
        ...
