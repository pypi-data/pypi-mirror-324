# Scrapeready Client

A Python client for making requests to [scrapeready.com](https://api.scrapeready.com/v1/) endpoints.

## Features

- **website_to_text(url: str)**  
  Scrapes text from a website.

- **serp(q: str)**  
  Retrieves SERP (Search Engine Results Page) information.

- **ai_search(q: Optional[str], prompt: Optional[str], max_websites: int = 5)**  
  Generates or uses a query to scrape top search results.

## Installation

```bash
pip install scrapeready