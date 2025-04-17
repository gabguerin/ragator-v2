from pathlib import Path
from typing import Annotated

import typer

from utils.httpx import download_web_page


async def main(
    all_urls_to_download_file_path: Annotated[Path, typer.Option(...)],
    downloaded_html_pages_folder: Annotated[Path, typer.Option(...)],
) -> None:
    with open(all_urls_to_download_file_path, "r") as f:
        all_urls_to_download = [line.strip() for line in f.readlines()]

    for url in all_urls_to_download:
        try:
            await download_web_page(url, folder=downloaded_html_pages_folder)
        except Exception as e:
            print(f"Failed to download {url}: {e}")


if __name__ == "__main__":
    typer.run(main)
