"""Load CSV file and extract content and metadata."""

from src.constants import DOCUMENTS_FOLDER
from src.models import CSVModel

CSV_MODEL = CSVModel(
    content_fields=["content_field_1", "content_field_2"],
    metadata_fields=["metadata_field_1", "metadata_field_2"],
    documents_folder=DOCUMENTS_FOLDER,
)


def extract_content(row: dict[str, str]) -> str:
    """Extract content from a row."""
    return "\n".join(
        f"{column}: {value if value is not None else value}"
        for column, value in row.items()
        if column in CSV_MODEL.content_fields
    )


def extract_metadata(row: dict[str, str]) -> dict[str, str]:
    """Extract metadata from a row."""
    return {
        column: value
        for column, value in row.items()
        if column in CSV_MODEL.metadata_fields
    }
