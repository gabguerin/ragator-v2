import asyncio
import os
from pathlib import Path
from typing import Annotated

import pandas as pd
import typer

from src.retrieval.file_handlers.html import HtmlFileHandler


async def _main(
    downloaded_html_pages_folder: Path,
    chunk_size: int,
    chunk_overlap: int,
    chunks_parquet_path: str,
) -> None:
    chunks_data = []
    for html_page_path in downloaded_html_pages_folder.glob("*"):
        file = HtmlFileHandler(
            html_page_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        chunks = await file.to_chunks()
        chunks_data.extend([chunk.model_dump() for chunk in chunks])

    os.makedirs(os.path.dirname(chunks_parquet_path), exist_ok=True)
    pd.DataFrame(chunks_data).to_parquet(
        chunks_parquet_path, engine="pyarrow", compression="gzip"
    )


def main(
    downloaded_html_pages_folder: Annotated[Path, typer.Option(...)],
    chunk_size: Annotated[int, typer.Option(...)],
    chunk_overlap: Annotated[int, typer.Option(...)],
    chunks_parquet_path: Annotated[str, typer.Option(...)],
) -> None:
    asyncio.run(
        _main(
            downloaded_html_pages_folder=downloaded_html_pages_folder,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            chunks_parquet_path=chunks_parquet_path,
        ),
    )


if __name__ == "__main__":
    typer.run(main)
