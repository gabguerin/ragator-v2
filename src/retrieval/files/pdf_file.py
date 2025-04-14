import asyncio

from PyPDF2 import PdfReader
from retrieval.files.base_file import BaseFile


class PdfDocument(BaseFile):
    """
    PDF document loader.
    """

    async def load(self) -> str:
        def read_pdf():
            reader = PdfReader(self.filepath)
            return "\n".join(page.extract_text() or "" for page in reader.pages)

        return await asyncio.to_thread(read_pdf)
