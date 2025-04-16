"""
Module: Utilities
This module provides utility functions for httpx functionalities.
"""
from pathlib import Path

import httpx
import os


def convert_url_to_filename(url):
    return url.replace("https://", "").replace("http://", "").replace("/", "_") + ".html"


async def download_web_page(url: str, folder: Path) -> str | None:
    """
    Downloads the contents of the specified URL and saves it as an HTML file
    in the given folder. The filename is derived from the URL.
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, convert_url_to_filename(url))
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(response.text)

    return filepath
