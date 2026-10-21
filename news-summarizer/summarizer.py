
from news_api import fetch_articles
from llm_providers import LLMProviders
from collections import Counter
import re


STOP_WORDS = {
    "the", "and", "for", "that", "with", "this", "from", "are",
    "was", "were", "has", "have", "had", "will", "its", "into",
    "about", "after", "before", "over", "under", "their", "they",
    "you", "your", "not", "but", "said", "says", "than", "then",
    "new", "more", "also", "could", "would", "been", "being",
    "his", "her", "our", "out", "who", "what", "when", "where",
    "how", "all", "can", "may", "one", "two", "per", "via"
}


def trending_topics(articles, top_n=10):
    """Identify frequently mentioned keywords across news articles."""
    counts = Counter()

    for article in articles:
        text = (
            f"{article.get('title', '')} "
            f"{article.get('description', '')} "
            f"{article.get('summary', '')}"
        )
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        counts.update(word for word in words if word not in STOP_WORDS)

    return counts.most_common(top_n)


class NewsSummarizer:
    def __init__(self):
        self.providers = LLMProviders()

    def run(self):
        articles = fetch_articles(limit=10)

        if not articles:
            print("No news articles were returned.")
            return

        processed_articles = []

        for article in articles:
            title = article.get("title") or "Untitled"
            description = article.get("description") or title

            print(f"\nTitle: {title}")

            try:
                summary = self.providers.summarize(description)
                sentiment = self.providers.analyze_sentiment(summary)

                article["summary"] = summary
                processed_articles.append(article)

                print(f"Summary: {summary}")
                print(f"Sentiment: {sentiment}")

            except Exception as error:
                print(f"Processing failed: {error}")

        print("\n=== Trending Topics ===")
        topics = trending_topics(processed_articles)

        if topics:
            for topic, count in topics:
                print(f"{topic}: mentioned {count} times")
        else:
            print("No trending topics identified.")

        try:
            cost = f"${float(self.providers.total_cost):.6f}"
        except (TypeError, ValueError):
            cost = "unavailable"

        print(f"\nEstimated OpenAI cost: {cost}")


if __name__ == "__main__":
    NewsSummarizer().run()
