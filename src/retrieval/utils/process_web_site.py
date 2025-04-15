from typing import List

from langchain_core.documents import Document

from retrieval.files.html_file import HtmlFile
from retrieval.utils.crawl_site import crawl_site


async def main(start_url: str, max_pages: int = 50) -> List[Document]:
    urls = crawl_site(start_url, max_pages=max_pages)
    documents = []

    for url in urls:
        try:
            html_file = HtmlFile(url)
            docs = await html_file.to_documents()
            documents.extend(docs)
            print(f"Processed {url} -> {len(docs)} chunks")
        except Exception as e:
            print(f"Failed to process {url}: {e}")

    return documents
