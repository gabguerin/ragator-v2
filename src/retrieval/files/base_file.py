import os
from pathlib import Path
from typing import List
from abc import ABC, abstractmethod

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class BaseFile(ABC):
    def __init__(
        self, filepath: str | Path, chunk_size: int = 500, chunk_overlap: int = 50
    ):
        self.filepath = filepath
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @abstractmethod
    async def load(self) -> str:
        """Async method to load file content."""
        pass

    async def to_documents(self) -> List[Document]:
        content = await self.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        chunks = splitter.split_text(content)

        documents = [
            Document(
                page_content=chunk,
                metadata={
                    "source": os.path.basename(self.filepath),
                    "chunk_index": idx,
                },
            )
            for idx, chunk in enumerate(chunks)
        ]

        return documents
