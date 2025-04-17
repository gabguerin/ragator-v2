from pathlib import Path
from typing import Annotated

import pandas as pd
import typer
import yaml

from retrieval.files.html_file import HtmlFile


def main(
    downloaded_html_pages_folder: Annotated[Path, typer.Option(...)],
    chunks_parquet_path: Annotated[str, typer.Option(...)],
) -> None:
    with open("scripts/populate_qdrant_collection/params.yaml") as f:
        params = yaml.safe_load(f)["train"]

    all_chunks = []
    for path in downloaded_html_pages_folder.glob("*.html"):
        try:
            file = HtmlFile(
                path,
                chunk_size=params["chunk_size"],
                chunk_overlap=params["chunk_overlap"],
            )
            chunks = await file.to_documents()
            for c in chunks:
                all_chunks.append({"content": c.page_content, "metadata": c.metadata})
        except Exception:
            continue

    df = pd.DataFrame(all_chunks)
    df.to_parquet(chunks_parquet_path, index=False)


if __name__ == "__main__":
    typer.run(main)
