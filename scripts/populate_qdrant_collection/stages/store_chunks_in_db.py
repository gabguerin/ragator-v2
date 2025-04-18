from typing import Annotated, Any

import pandas as pd
import typer
import asyncio

from langchain_core.embeddings import Embeddings

from utils.importlib import import_module_from_path


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
    chunks_data = pd.read_parquet(chunks_parquet_path, engine="pyarrow")

    # Load embedding model
    embedding_model_class: Any = import_module_from_path(
        module_path=embedding_module, object_name=embedding_class_name
    )
    embedding_model: Embeddings = embedding_model_class(
        model=embedding_model_name, dimensions=embedding_dimension
    )

    # Create vector store
    vector_store_class: Any = import_module_from_path(
        module_path=vector_store_module, object_name=vector_store_class_name
    )
    vector_store = vector_store_class(embedding_model=embedding_model)
    await vector_store.create_collection_if_not_exists(
        collection_name=vector_store_collection_name, vector_size=embedding_dimension
    )

    await vector_store.insert_documents(
        collection_name=vector_store_collection_name,
        texts=chunks_data["content"].tolist(),
        metadata=chunks_data.drop(columns=["text"]).to_dict(orient="records"),
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
