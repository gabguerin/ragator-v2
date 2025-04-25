"""
Module: HTML File Handler
Provides functionality to process and extract content from HTML files.
"""
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from markdownify import markdownify

from .base import BaseFileHandler


class HtmlFileHandler(BaseFileHandler):
    """
    Class for handling HTML file ingestion and processing.
    """

    def __init__(self, filepath: Path, chunk_size: int = 500, chunk_overlap: int = 50):
        super().__init__(filepath)

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    async def preprocess(self, file_content: str) -> str:
        """
        Preprocess the HTML content by removing unnecessary tags and formatting.
        """
        return markdownify(file_content)

    async def split_text(self, content: str) -> list[str]:
        """
        Split the preprocessed text into smaller chunks for easier processing.

        Uses RecursiveCharacterTextSplitter for chunking.
        """

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        return splitter.split_text(content)
