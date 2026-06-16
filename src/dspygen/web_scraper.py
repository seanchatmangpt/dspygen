import asyncio

import httpx


async def scrape_website(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; dspygen-scraper/1.0; +https://github.com/seanchatmangpt/dspygen)"
    }
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        html = response.text
        start = html.find('<title>') + len('<title>')
        end = html.find('</title>')
        return html[start:end]
