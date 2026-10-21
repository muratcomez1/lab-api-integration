
from openai import OpenAI
import cohere
from config import Config


class LLMProviders:
    def __init__(self):
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.cohere_client = cohere.ClientV2(
            api_key=Config.COHERE_API_KEY
        )
        self.total_cost = 0.0

    def summarize(self, text):
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this news in 2 sentences:\n{text}",
                }
            ],
        )

        if response.usage:
            self.total_cost += (
                response.usage.prompt_tokens * 0.00000015
                + response.usage.completion_tokens * 0.00000060
            )

        return response.choices[0].message.content

    def analyze_sentiment(self, text):
        response = self.cohere_client.chat(
            model="command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Classify the sentiment as positive, negative, "
                        "or neutral. Return only the classification.\n\n"
                        f"{text}"
                    ),
                }
            ],
        )
        return response.message.content[0].text.strip()
