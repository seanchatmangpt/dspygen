import httpx
import asyncio


async def scrape_website(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        html = response.text
        start = html.find('<title>') + len('<title>')
        end = html.find('</title>')
        return html[start:end]
