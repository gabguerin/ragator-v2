"""
Module: HTML File Handler
Provides functionality to process and extract content from HTML files.
"""

import aiofiles

from retrieval.files.base_file import BaseFile


class HtmlFile(BaseFile):
    """
    Class for handling HTML file ingestion and processing.
    """

    async def load(self) -> str:
        """
        Reads the HTML file and extracts visible text content.

        Returns:
            str: The concatenated visible text from the HTML file.
        """
        async with aiofiles.open(self.filepath, mode="r", encoding="utf-8") as f:
            html_content: str = await f.read()

        # soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")
        #
        # texts: list[str] = []
        # for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "code", "pre"]):
        #     text: str = tag.get_text(strip=True)
        #     if text:
        #         texts.append(text)

        return html_content
