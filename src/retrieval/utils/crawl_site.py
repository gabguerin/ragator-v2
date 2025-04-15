from typing import List

from requests_html import HTMLSession
from urllib.parse import urldefrag, urlparse


def crawl_site(start_url: str, max_pages: int = 50) -> List[str]:
    visited = set()
    to_visit = {start_url}
    discovered = []

    session = HTMLSession()

    while to_visit and len(discovered) < max_pages:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        try:
            response = session.get(url)
            response.html.render(timeout=10)
        except Exception as e:
            print(f"Error loading {url}: {e}")
            continue

        discovered.append(url)
        for link in response.html.absolute_links:
            cleaned = urldefrag(link)[0]
            if urlparse(cleaned).netloc == urlparse(start_url).netloc:
                if cleaned not in visited:
                    to_visit.add(cleaned)

    return discovered
