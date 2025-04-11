"""Split documents into chunks.

This is necessary to be able to retrieve only the relevant
parts of a document, to avoid giving too much context to the bot.
"""

from collections.abc import Generator
from pathlib import Path
from typing import Any

import pandas as pd
from loguru import logger

from src.constants import CHUNK_CONTENT_COLUMN, DOCUMENT_PATH_COLUMN
from src.document_ingestion.load_csv import extract_content, extract_metadata


def write_chunks_to_parquet(df: pd.DataFrame, output_path: str) -> None:
    """Write chunks to parquet.

    now using pandas, but we could use polars in the future
    """
    df.to_parquet(output_path)


def split_single_document_into_chunks(
    document: Path,
) -> Generator[dict[str, Any], None, None]:
    """Split a single document into chunks."""
    match document.suffix:
        case ".pdf":
            chunks_from_document = process_pdf_document(document)
        case ".csv":
            chunks_from_document = process_csv_document(document)
        case ".docx":
            logger.exception("docx format is not supported yet")
            raise NotImplementedError
        case _:
            logger.exception(f"Unsupported document format: {document.suffix}")
            raise NotImplementedError
    for chunk in chunks_from_document:
        if check_for_mandatory_fields(chunk):
            yield chunk
        else:
            logger.error(f"Missing mandatory fields in chunk: {chunk}")


def process_pdf_document(document: Path) -> Generator[dict[str, Any], None, None]:
    """Process a PDF document.

    The import is inside the function to avoid importing PyPDFLoader if the document
    is not a PDF and so minimize the dependencies of package.
    """
    from langchain_community.document_loaders import PyPDFLoader

    loader = PyPDFLoader(str(document))
    pages = loader.load_and_split()
    yield from [
        {
            CHUNK_CONTENT_COLUMN: chunk.page_content,
            DOCUMENT_PATH_COLUMN: document.name,
            "page": chunk.metadata["page"],
        }
        for chunk in pages
    ]


def process_csv_document(document: Path) -> Generator[dict[str, Any], None, None]:
    """Process a csv document."""
    data = pd.read_csv(document)

    content = data.apply(extract_content, axis=1)
    metadata = data.apply(extract_metadata, axis=1)

    yield from [
        {
            CHUNK_CONTENT_COLUMN: chunk_content,
            **metadata[index],
            DOCUMENT_PATH_COLUMN: document.name,
            "row": index,
        }
        for index, chunk_content in enumerate(content)
    ]


def check_for_mandatory_fields(chunk: dict[str, Any]) -> bool:
    """Check for mandatory fields in a chunk.

    Those fields are required by the chatbot to generate an answer and list its sources.
    """
    mandatory_fields = [CHUNK_CONTENT_COLUMN, DOCUMENT_PATH_COLUMN]
    are_all_mandatory_fields_present = all(field in chunk for field in mandatory_fields)
    if not are_all_mandatory_fields_present:
        logger.error(f"Missing mandatory fields in chunk: {chunk}")
    return are_all_mandatory_fields_present
