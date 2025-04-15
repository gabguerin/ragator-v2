import aiofiles

from retrieval.files.base_file import BaseFile


class PythonFile(BaseFile):
    async def load(self) -> str:
        async with aiofiles.open(self.filepath, mode="r", encoding="utf-8") as f:
            return await f.read()
