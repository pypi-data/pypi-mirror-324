# Scrapeready Client

A Python client for making requests to [scrapeready.com](https://scrapeready.com/) endpoints.

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
```
## Example Usage

Here’s how you can use the ```ScrapeReady``` client to interact with the API's main functionalities.

### 1. Initialize the Client

First, import the ```ScrapeReady``` class and initialize it with your API key.

```python
from scrapeready import ScrapeReady

# Replace 'YOUR_API_KEY_HERE' with your actual API key
client = ScrapeReady(api_key="YOUR_API_KEY_HERE")
```

### 2. Scrape a Website to Text

Use the `website_to_text` method to scrape and extract text from a specified website.

```python
try:
    website_url = "https://www.example.com"
    website_result = client.website_to_text(website_url)
    print("Website to Text Result:")
    print(website_result)
except Exception as e:
    print(f"Error in website_to_text: {e}")
```

**Output Example:**

```json
{
    "message": "Page scraped successfully",
    "remaining_credits": 99,
    "page": {
        "url": "https://www.example.com",
        "raw_html": "<html>...</html>",
        "cleaned_html": "<div>Example Domain</div>",
        "relevant_html": "<div>Example Domain</div>",
        "markdown": "# Example Domain\n\nThis domain is for use in illustrative examples in documents."
    }
}
```

### 3. Retrieve SERP Information

Use the `serp` method to fetch Search Engine Results Page data based on a query.

```python
try:
    search_query = "openai chatgpt"
    serp_result = client.serp(search_query)
    print("\nSERP Result:")
    print(serp_result)
except Exception as e:
    print(f"Error in serp: {e}")
```

**Output Example:**

```json
{
    "message": "SERP scraped successfully",
    "remaining_credits": 98,
    "serp": {
        "url": "https://www.google.com/search?q=openai+chatgpt",
        "serp": {
            "organicResults": [
                {
                    "description": "ChatGPT is an AI developed by OpenAI...",
                    "name": "ChatGPT - OpenAI",
                    "url": "https://www.openai.com/chatgpt",
                    "rank": 1
                }
                // More results...
            ],
            "pageNumber": 1,
            "metadata": {
                "displayedQuery": "openai chatgpt",
                "searchedQuery": "openai chatgpt",
                "totalOrganicResults": 100,
                "dateDownloaded": "2025-01-30T12:34:56+00:00"
            }
        },
        "httpResponseBody": "<html>...</html>"
    }
}
```

### 4. Perform an AI-Powered Search

Use the `ai_search` method to generate or utilize a query to scrape top search results.

```py
try:
    prompt = "Who is the current President of the US?"
    ai_search_result = client.ai_search(prompt=prompt, max_websites=3)
    print("\nAI Search Result:")
    print(ai_search_result)
except Exception as e:
    print(f"Error in ai_search: {e}")
```

**Output Example:**

```json
{
    "message": "AI search completed successfully",
    "remaining_credits": 96,
    "ready-message": "https://www.whitehouse.gov/president-john-doe:\n# President John Doe\n\nJohn Doe is the 47th President of the United States.\n\nhttps://www.cnn.com/president-john-doe:\n# President John Doe\n\nJohn Doe was inaugurated on January 20, 2025.\n\nhttps://www.bbc.com/president-john-doe:\n# President John Doe\n\nJohn Doe has implemented several key policies...",
    "pages": [
        {
            "url": "https://www.whitehouse.gov/president-john-doe",
            "raw_html": "<html>...</html>",
            "cleaned_html": "<div>President John Doe</div>",
            "relevant_html": "<div>John Doe is the 47th President of the United States.</div>",
            "markdown": "# President John Doe\n\nJohn Doe is the 47th President of the United States."
        }
        // More pages...
    ]
}
```

## Handling Exceptions

All methods may raise exceptions in case of network issues, invalid API keys, or other errors. It's recommended to use <try-except> blocks to handle these gracefully, as shown in the example usage above.

## License

See the <LICENSE>(./LICENSE) file for details.