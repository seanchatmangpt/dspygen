import requests
# from html2text import html2text
import requests
# from duckduckgo_search import DDGS


def execute_duckduckgo_queries(queries: dict, max_results=5):
    """
    Execute search queries using DuckDuckGo API and return search results formatted to include
    only URL, title, and description for each result.

    :param queries: Dictionary of objectives to search query strings
    :param max_results: Maximum number of results to return per query
    :return: Dictionary of objectives to lists of {'url': url, 'title': title, 'description': description}
    """
    print(f"Executing DuckDuckGo queries: {queries}")
    search_results = {}

    for objective, query in queries.items():
        print(f"Executing query for {objective}: {query}")
        results = {}  # DDGS().text(query, max_results=max_results)

        print(f"Results for {objective}: {results}")

        formatted_results = [
            {
                'url': result.get('href'),
                'title': result.get('title'),
                'description': result.get('body')
            }
            for result in results if result.get('href') and result.get('title')
        ]
        search_results[objective] = formatted_results

    print(f"Search results: {search_results}")

    return search_results



def execute_brave_search_queries(queries: dict, api_key):
    """
    Execute search queries using Brave Search API and return search results formatted to include
    only URL, title, and description for each result.

    :param queries: Dictionary of objectives to search query strings
    :param api_key: Your API key for the Brave Search API
    :return: Dictionary of objectives to lists of {'url': url, 'title': title, 'description': description}
    """
    search_results = {}
    base_url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }

    for objective, query in queries.items():
        params = {
            "q": query,  # The user's search query term
            "country": "us",  # Optional: the search query country
            "search_lang": "en",  # Optional: the search language preference
            "ui_lang": "en-US",  # Optional: User interface language
            "count": 20,  # Optional: the number of search results to return
            "offset": 0,  # Optional: the zero-based offset for pagination
            "safesearch": "moderate",  # Optional: filter search results for adult content
        }

        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('web', {}).get('results', [])
            formatted_results = [{
                'url': result.get('url'),
                'title': result.get('title'),
                'description': result.get('description')
            } for result in results if result.get('url') and result.get('title')]
            search_results[objective] = formatted_results
        else:
            search_results[objective] = []
            print(f"Failed to fetch results for {objective}: {response.status_code}")

    return search_results



def scrape_urls(urls):
    """
    Scrape content from a list of URLs and convert HTML to text.

    :param urls: List of URLs to scrape
    :return: List of textual contents from these URLs
    """
    contents = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            text = ""  # html2text(response.text)
            contents.append(text)
        else:
            contents.append("")
    return contents
