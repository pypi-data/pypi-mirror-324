import requests
from typing import Optional, Dict, Any

class ScrapeReady:
    """
    A client for calling the Scrapeready.com v1 API endpoints.

    Usage example:
        from scrapeready import ScrapeReady

        client = ScrapeReady(api_key="YOUR_API_KEY_HERE")

        # 1. Website to text
        result_1 = client.website_to_text("https://www.example.com")
        print(result_1)

        # 2. SERP
        result_2 = client.serp("openai chatgpt")
        print(result_2)

        # 3. AI Search
        result_3 = client.ai_search(prompt="Who is the current President of the US?")
        print(result_3)
    """

    def __init__(self, api_key: str, base_url: str = "https://api.scrapeready.com/v1"):
        """
        :param api_key: Your Scrapeready API key.
        :param base_url: Base URL for the Scrapeready API (override for testing if needed).
        """
        self.api_key = api_key
        self.base_url = base_url

    def _headers(self) -> Dict[str, str]:
        """
        Returns the headers required for all requests, including the API key.
        """
        return {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
        }

    def website_to_text(self, url: str) -> Dict[str, Any]:
        """
        Call the `/website-to-text` endpoint to scrape a website's content.

        :param url: A URL to scrape (e.g. 'https://www.example.com').
        :return: A dictionary containing the response data, for example:
        {
            "message": "Page scraped successfully",
            "remaining_credits": ...,
            "page": {
                "url": ...,
                "raw_html": ...,
                "cleaned_html": ...,
                "relevant_html": ...,
                "markdown": ...
            }
        }

        :raises requests.exceptions.RequestException: If network issues occur.
        :raises Exception: If the server response indicates an error.
        """
        endpoint = f"{self.base_url}/website-to-text"
        payload = {"url": url}

        resp = requests.post(endpoint, headers=self._headers(), json=payload)
        resp.raise_for_status()  # Raises HTTPError if status is 4xx or 5xx
        return resp.json()

    def serp(self, q: str) -> Dict[str, Any]:
        """
        Call the `/serp` endpoint to fetch a Google SERP result.

        :param q: Search query (e.g. 'latest AI news').
        :return: A dictionary containing the response data, for example:
        {
            "message": "SERP scraped successfully",
            "remaining_credits": ...,
            "serp": {
                "url": ...,
                "serp": {
                    "organicResults": [...],
                    "url": ...,
                    "pageNumber": ...,
                    "metadata": ...
                },
                "httpResponseBody": ...
            }
        }

        :raises requests.exceptions.RequestException: If network issues occur.
        :raises Exception: If the server response indicates an error.
        """
        endpoint = f"{self.base_url}/serp"
        # We pass the query as a query parameter
        params = {"q": q}

        resp = requests.get(endpoint, headers=self._headers(), params=params)
        resp.raise_for_status()
        return resp.json()

    def ai_search(
        self,
        q: Optional[str] = None,
        prompt: Optional[str] = None,
        max_websites: int = 5
    ) -> Dict[str, Any]:
        """
        Call the `/ai-search` endpoint. This can use either:
          - an explicit query `q`, or
          - a `prompt` from which the endpoint can generate a query using AI.

        :param q: A raw search query (e.g. 'best pizza in NYC').
        :param prompt: If `q` is not provided, the server can generate a search query from your prompt.
        :param max_websites: The number of top SERP results to scrape (default=5).
        :return: A dictionary containing the AI search result, for example:
        {
            "message": "AI search completed successfully",
            "remaining_credits": ...,
            "ready-message": "...(markdown of scraped results)...",
            "pages": [
                {
                    "url": ...,
                    "raw_html": ...,
                    "cleaned_html": ...,
                    "relevant_html": ...,
                    "markdown": ...
                },
                ...
            ]
        }

        :raises requests.exceptions.RequestException: If network issues occur.
        :raises Exception: If the server response indicates an error.
        """
        endpoint = f"{self.base_url}/ai-search"
        payload = {
            "q": q,
            "prompt": prompt,
            "max_websites": max_websites
        }

        resp = requests.post(endpoint, headers=self._headers(), json=payload)
        resp.raise_for_status()
        return resp.json()