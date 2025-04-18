from typing import Annotated
import typer
import asyncio

import yaml

from src.utils.urllib import crawl_website


async def _main(
    max_pages_per_sources: int,
    all_urls_to_download_file_path: str
) -> None:


def main(
    chunks_parquet_path: Annotated[str, typer.Option(...)],
    embedding_size: Annotated[str, typer.Option(...)],
) -> None:
    asyncio.run(
        _main(
        )
    )


if __name__ == "__main__":
    typer.run(main)
