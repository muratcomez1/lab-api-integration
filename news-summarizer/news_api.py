
"""NewsAPI client helpers."""

import requests

from config import Config


URL = "https://newsapi.org/v2/top-headlines"


def fetch_articles(limit=3):
    """Return up to ``limit`` technology headlines from NewsAPI."""
    if not Config.NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is not configured")

    response = requests.get(
        URL,
        params={
            "category": "technology",
            "language": "en",
            "pageSize": limit,
            "apiKey": Config.NEWS_API_KEY,
        },
        timeout=Config.REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    data = response.json()
    return data.get("articles", [])[:limit]


if __name__ == "__main__":
    for article in fetch_articles():
        print(f"Title: {article.get('title')}")
        print(f"URL: {article.get('url')}")
        print("-" * 50)
