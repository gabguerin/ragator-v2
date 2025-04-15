import aiofiles
from bs4 import BeautifulSoup

from retrieval.files.base_file import BaseFile


class HtmlFile(BaseFile):
    async def load(self) -> str:
        async with aiofiles.open(self.filepath, mode="r", encoding="utf-8") as f:
            html_content = await f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Extract visible text (you can customize this)
        texts = []

        for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "code", "pre"]):
            text = tag.get_text(strip=True)
            if text:
                texts.append(text)

        return "\n".join(texts)
