import pytest
import httpx
from dspygen.web_scraper import scrape_website

@pytest.mark.asyncio
async def test_scrape_website(httpx_mock):
    url = "http://example.com"
    httpx_mock.add_response(method="GET", url=url, text='<html><head><title>Test Page</title></head><body></html>')

    title = await scrape_website(url)
    assert title == "Test Page"
