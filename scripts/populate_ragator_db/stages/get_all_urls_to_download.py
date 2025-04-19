from typing import Annotated
import typer
import asyncio

import yaml

from src.utils.urllib import crawl_website


async def _main(
    max_pages_per_sources: int,
    all_urls_to_download_file_path: str,
    params_file_path: str,
) -> None:
    with open(params_file_path) as f:
        starting_urls = yaml.safe_load(f)["starting_urls"]

    all_urls = []
    for url in starting_urls:
        print(f"Crawling {url}")
        try:
            urls = await crawl_website(url, max_pages=max_pages_per_sources)
            all_urls.extend(urls)
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    with open(all_urls_to_download_file_path, "w") as f:
        f.write("\n".join(all_urls))


def main(
    max_pages_per_sources: Annotated[int, typer.Option(...)],
    all_urls_to_download_file_path: Annotated[str, typer.Option(...)],
    params_file_path: Annotated[str, typer.Option(...)],
) -> None:
    asyncio.run(
        _main(
            max_pages_per_sources=max_pages_per_sources,
            all_urls_to_download_file_path=all_urls_to_download_file_path,
            params_file_path=params_file_path,
        ),
    )


if __name__ == "__main__":
    typer.run(main)
