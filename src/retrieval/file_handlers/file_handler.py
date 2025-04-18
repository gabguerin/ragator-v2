import hashlib
from pathlib import Path
from typing import List
from abc import ABC, abstractmethod
from uuid import uuid5, NAMESPACE_DNS

import aiofiles
from langchain_text_splitters import RecursiveCharacterTextSplitter

from retrieval.chunks.base_chunk import Chunk


class FileHandler(ABC):
    def __init__(
        self, filepath: str | Path, chunk_size: int = 500, chunk_overlap: int = 50
    ):
        self.filepath = filepath
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @abstractmethod
    async def preprocess(self, file_content: str) -> str:
        """Async method to load file content."""
        ...

    async def load(self) -> str:
        """Async method to load file content."""
        async with aiofiles.open(self.filepath, mode="r", encoding="utf-8") as f:
            file_content: str = await f.read()

        return file_content

    async def to_chunks(self) -> List[Chunk]:
        content = await self.load()

        preprocessed_content = await self.preprocess(content)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        chunks = [
            Chunk(
                content=chunk_content,
                source=self.filepath.name,
                uuid=str(
                    uuid5(
                        NAMESPACE_DNS,
                        hashlib.sha256(chunk_content.encode()).hexdigest(),
                    )
                ),
            )
            for chunk_content in splitter.split_text(preprocessed_content)
        ]

        return chunks
