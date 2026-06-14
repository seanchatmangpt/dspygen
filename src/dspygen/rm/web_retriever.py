"""Web retriever that combines DuckDuckGo search with HTTP scraping."""

from __future__ import annotations

import asyncio
from typing import Any, List, Optional

import dspy
from loguru import logger

from dspygen.web_scraper import scrape_website


def _ddg_search(query: str, max_results: int) -> List[str]:
    """Return up to *max_results* URLs from a DuckDuckGo text search.

    Uses the ``duckduckgo_search`` package (``ddg5``/``DDGS`` API).
    Falls back gracefully to an empty list on import or network errors.
    """
    try:
        from duckduckgo_search import DDGS  # type: ignore[import]

        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
        return [r["href"] for r in results if "href" in r]
    except Exception as exc:
        logger.warning(f"DuckDuckGo search failed: {exc}")
        return []


async def _scrape_urls(urls: List[str], timeout: float = 10.0) -> List[str]:
    """Scrape *urls* concurrently, ignoring individual failures."""

    async def _safe_scrape(url: str) -> Optional[str]:
        try:
            text = await asyncio.wait_for(scrape_website(url), timeout=timeout)
            return text.strip() if text else None
        except Exception as exc:
            logger.debug(f"Scrape failed for {url}: {exc}")
            return None

    results = await asyncio.gather(*(_safe_scrape(u) for u in urls))
    return [r for r in results if r]


class WebRetriever(dspy.Retrieve):
    """Retrieve passages from the live web for a given query.

    Workflow:
    1. Use DuckDuckGo to find the top *k* URLs for *query*.
    2. Scrape each URL concurrently with :func:`~dspygen.web_scraper.scrape_website`.
    3. Return the scraped texts wrapped in a :class:`dspy.Prediction`.

    Args:
        k: Maximum number of web pages to retrieve (default: 3).
        scrape_timeout: Per-page network timeout in seconds (default: 10.0).
    """

    def __init__(self, k: int = 3, scrape_timeout: float = 10.0, **kwargs: Any) -> None:
        super().__init__(k=k)
        self.k: int = k
        self.scrape_timeout: float = scrape_timeout

    def forward(self, query: str, **kwargs: Any) -> dspy.Prediction:
        """Search the web and return scraped content as a :class:`dspy.Prediction`.

        Args:
            query: Natural-language search query.
            **kwargs: Additional keyword arguments (ignored, for API compatibility).

        Returns:
            A :class:`dspy.Prediction` whose ``passages`` field is a list of
            strings, each containing the scraped text of one result page.
            Returns an empty list if no results could be retrieved.
        """
        logger.info(f"WebRetriever.forward called with query={query!r}, k={self.k}")

        urls = _ddg_search(query, max_results=self.k)
        logger.debug(f"DuckDuckGo returned {len(urls)} URLs: {urls}")

        if not urls:
            logger.warning("No URLs returned from search; returning empty passages.")
            return dspy.Prediction(passages=[])

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Inside an already-running event loop (e.g. Jupyter / async test)
                import concurrent.futures

                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    passages = pool.submit(
                        asyncio.run, _scrape_urls(urls, timeout=self.scrape_timeout)
                    ).result()
            else:
                passages = loop.run_until_complete(_scrape_urls(urls, timeout=self.scrape_timeout))
        except Exception as exc:
            logger.error(f"Scraping failed: {exc}")
            passages = []

        logger.info(f"WebRetriever retrieved {len(passages)} passage(s) for query={query!r}")
        return dspy.Prediction(passages=passages)


def main() -> None:
    rm = WebRetriever(k=2)
    result = rm.forward(query="What is the CSS selector for a submit button?")
    for i, passage in enumerate(result.passages, 1):
        print(f"--- Passage {i} ---")
        print(passage[:400])
        print()


if __name__ == "__main__":
    main()
