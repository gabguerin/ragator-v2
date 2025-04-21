from typing import Annotated, Any

import pandas as pd
import typer
import asyncio

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings

from src.retrieval.chunk import Chunk
from src.retrieval.vector_stores.base import BaseVectorStore
from src.utils.importlib import import_module_from_path


load_dotenv()


async def _main(
    chunks_parquet_path: str,
    embedding_module: str,
    embedding_class_name: str,
    embedding_model_name: str,
    embedding_dimension: int,
    vector_store_module: str,
    vector_store_class_name: str,
    vector_store_collection_name: str,
) -> None:
    chunks_data_df = pd.read_parquet(chunks_parquet_path, engine="pyarrow")
    chunks = [
        Chunk(**chunk_data) for chunk_data in chunks_data_df.to_dict(orient="records")
    ]

    # Load embedding model
    embedding_model_class: Any = import_module_from_path(
        module_path=embedding_module, object_name=embedding_class_name
    )
    embedding_model: Embeddings = embedding_model_class(
        model=embedding_model_name,
        dimensions=embedding_dimension,
    )

    # Create vector store
    vector_store_class: Any = import_module_from_path(
        module_path=vector_store_module, object_name=vector_store_class_name
    )
    vector_store: BaseVectorStore = vector_store_class(embedding_model=embedding_model)
    await vector_store.create_or_overwrite_collection_if_exists(
        collection_name=vector_store_collection_name, vector_size=embedding_dimension
    )

    # Insert chunks into the vector store
    await vector_store.upsert_chunks(
        collection_name=vector_store_collection_name,
        chunks=chunks,
    )


def main(
    chunks_parquet_path: Annotated[str, typer.Option(...)],
    embedding_module: Annotated[str, typer.Option(...)],
    embedding_class_name: Annotated[str, typer.Option(...)],
    embedding_model_name: Annotated[str, typer.Option(...)],
    embedding_dimension: Annotated[int, typer.Option(...)],
    vector_store_module: Annotated[str, typer.Option(...)],
    vector_store_class_name: Annotated[str, typer.Option(...)],
    vector_store_collection_name: Annotated[str, typer.Option(...)],
) -> None:
    asyncio.run(
        _main(
            chunks_parquet_path=chunks_parquet_path,
            embedding_module=embedding_module,
            embedding_class_name=embedding_class_name,
            embedding_model_name=embedding_model_name,
            embedding_dimension=embedding_dimension,
            vector_store_module=vector_store_module,
            vector_store_class_name=vector_store_class_name,
            vector_store_collection_name=vector_store_collection_name,
        )
    )


if __name__ == "__main__":
    typer.run(main)
