"""
Module: HTML File Handler
Provides functionality to process and extract content from HTML files.
"""

from markdownify import markdownify

from src.retrieval.file_handlers.file_handler import FileHandler


class HtmlHandler(FileHandler):
    """
    Class for handling HTML file ingestion and processing.
    """

    async def preprocess(self, file_content: str) -> str:
        """
        Preprocess the HTML content by removing unnecessary tags and formatting.
        """
        return markdownify(file_content)
