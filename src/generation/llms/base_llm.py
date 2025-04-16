"""
Module: Base LLM Interface
Defines an abstract base class for Large Language Models (LLMs).
"""

from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class representing an interface for LLM models.
    """

    @abstractmethod
    async def invoke(self, inputs: dict[str, str]) -> str:
        """
        Abstract method to generate a response based on input.

        Parameters:
            inputs (dict[str, str]): A dictionary containing input key-value pairs.

        Returns:
            str: The generated response from the LLM.
        """
        ...
