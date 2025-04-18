from pathlib import Path

import aiofiles
from markdownify import markdownify


async def convert_html_to_md(html_page_path: Path, output_folder: Path):
    async with aiofiles.open(html_page_path, mode="r", encoding="utf-8") as f:
        html_content = await f.read()

    markdown_page_path = output_folder / html_page_path.name.replace(".html", ".md")
    async with aiofiles.open(markdown_page_path, mode="w", encoding="utf-8") as f:
        await f.write(markdownify(html_content))
