import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urldefrag, urljoin, urlparse
from typing import Set, List


async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None


async def fetch_with_parse(url, session, to_visit, base_netloc, semaphore):
    async with semaphore:
        html = await fetch(session, url)
        if not html:
            return

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            abs_url = urldefrag(urljoin(url, href))[0]
            if urlparse(abs_url).netloc == base_netloc:
                to_visit.add(abs_url)


async def crawl_website(start_url: str, max_pages: int = 100) -> List[str]:
    visited: Set[str] = set()
    to_visit: Set[str] = {start_url}
    discovered: List[str] = []
    base_url = urlparse(start_url)
    semaphore = asyncio.Semaphore(10)  # control concurrency

    async with aiohttp.ClientSession() as session:
        while to_visit and len(discovered) < max_pages:
            tasks = []
            current_batch = list(to_visit)[: max_pages - len(discovered)]
            to_visit.clear()

            for url in current_batch:
                if urlparse(url).netloc == base_url.netloc:
                    if url not in visited:
                        visited.add(url)
                        tasks.append(
                            fetch_with_parse(
                                url, session, to_visit, base_url.netloc, semaphore
                            )
                        )

            _ = await asyncio.gather(*tasks)
            for url in current_batch:
                if url not in discovered:
                    discovered.append(url)

    return discovered
