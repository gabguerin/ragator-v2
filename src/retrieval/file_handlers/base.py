import hashlib
from pathlib import Path
from typing import List
from abc import ABC, abstractmethod
from uuid import uuid5, NAMESPACE_DNS

import aiofiles

from src.retrieval.chunk import Chunk


class BaseFileHandler(ABC):
    def __init__(self, filepath: str | Path):
        self.filepath = filepath

    @abstractmethod
    async def preprocess(self, file_content: str) -> str:
        """Async method to load file content."""
        ...

    @abstractmethod
    async def split_text(self, content: str) -> List[str]:
        """Async method to split text into chunks."""
        ...

    async def load(self) -> str:
        """Async method to load file content."""
        async with aiofiles.open(self.filepath, mode="r", encoding="utf-8") as f:
            file_content: str = await f.read()

        return file_content

    async def to_chunks(self) -> List[Chunk]:
        """Async method to convert file content to a list of Chunk objects."""
        content = await self.load()

        preprocessed_content = await self.preprocess(content)

        chunks = [
            Chunk(
                content=chunk_content,
                source=str(self.filepath.name),
                uuid=str(
                    uuid5(
                        NAMESPACE_DNS,
                        hashlib.sha256(chunk_content.encode()).hexdigest(),
                    )
                ),
            )
            for chunk_content in await self.split_text(preprocessed_content)
        ]

        return chunks
