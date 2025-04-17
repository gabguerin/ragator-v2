from typing import List, Annotated

import typer
import yaml

from utils.urllib import crawl_website


async def main(
    all_urls_to_download_file_path: Annotated[str, typer.Option(...)],
) -> None:
    with open("scripts/populate_qdrant_collection/params.yaml") as f:
        params = yaml.safe_load(f)["train"]

    all_urls = []
    for url in params["sources"]:
        print(f"Crawling {url}")
        try:
            urls = await crawl_website(url, max_pages=params["max_pages_per_sources"])
            all_urls.extend(urls)
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    async with open(all_urls_to_download_file_path, "w") as f:
        f.write("\n".join(all_urls))


if __name__ == "__main__":
    typer.run(main)
