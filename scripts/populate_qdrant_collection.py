from pathlib import Path
from typing import List

import aiofiles
import asyncio
import pandas as pd
from prefect import flow, task

from paths import INPUT_FILES
from retrieval.files.html_file import HtmlFile
# from retrieval.vectorstores.qdrant_store import QdrantVectorStore
from utils.httpx import download_web_page
from utils.io_manager import hash_value
from utils.urllib import crawl_website

DOC_SOURCES = {
    "langgraph": "https://langchain-ai.github.io/langgraph/",
}

FAILED_WEBPAGE_INGESTION_PATH = Path("data/documents/rag_about_ragator/failed_download_html_pages.txt")
CHUNKS_PARQUET_PATH = Path("data/chunks/chunks.parquet")


@task(
    persist_result=True,
    cache_key_fn=lambda context, inputs: hash_value(list(DOC_SOURCES.values()))
)
async def get_all_urls_to_download() -> List[str]:
    all_urls = []
    for url in DOC_SOURCES.values():
        print(f"Crawling {url}")
        try:
            urls = await crawl_website(url, max_pages=50)
            all_urls.extend(urls)
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")
    return list(set(all_urls))


@task(
    persist_result=True,
    cache_key_fn=lambda context, inputs: hash_value(inputs["urls"])
)
async def download_html_pages(urls: List[str]) -> List[str]:
    download_paths = []
    failed_urls = []

    for url in urls:
        try:
            path = await download_web_page(url, folder=INPUT_FILES)
            download_paths.append(str(path))
        except Exception:
            failed_urls.append(url)

    async with aiofiles.open(FAILED_WEBPAGE_INGESTION_PATH, mode="w") as f:
        await f.write("\n".join(failed_urls))

    return download_paths


@task(
    persist_result=True,
    cache_key_fn=lambda context, inputs: hash_value((inputs["paths"], inputs.get("splitter_cfg")))
)
async def get_chunks_from_html_pages(paths: List[str], splitter_cfg: dict = None) -> str:
    all_chunks = []

    for path in paths:
        try:
            file = HtmlFile(path, chunk_size=splitter_cfg["chunk_size"])
            chunks = await file.to_documents()
            for c in chunks:
                all_chunks.append({"content": c.page_content, "metadata": c.metadata})
        except Exception:
            continue

    df = pd.DataFrame(all_chunks)
    CHUNKS_PARQUET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CHUNKS_PARQUET_PATH, index=False)

    return str(CHUNKS_PARQUET_PATH)


# @task
# async def store_chunks_in_qdrant(parquet_path: str):
#     df = pd.read_parquet(parquet_path)
#     docs = [Document(page_content=row["content"], metadata=row["metadata"]) for _, row in df.iterrows()]
#     qdrant_client = QdrantVectorStore(collection_name="test")
#     qdrant_client.initialize_client()
#     await qdrant_client.add_documents(docs)
#     print(f"Stored {len(docs)} chunks in Qdrant.")


@flow
async def ingest_docs_flow(splitter_cfg: dict = None, store_to_qdrant: bool = True):
    urls = await get_all_urls_to_download()
    html_paths = await download_html_pages(urls)
    parquet_path = await get_chunks_from_html_pages(html_paths, splitter_cfg)
    # if store_to_qdrant:
    #     await store_chunks_in_qdrant(parquet_path)


if __name__ == "__main__":
    asyncio.run(ingest_docs_flow(splitter_cfg={"chunk_size": 512}))
