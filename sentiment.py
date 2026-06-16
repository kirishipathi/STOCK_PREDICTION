from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

# Initialize
newsapi = NewsApiClient(api_key=API_KEY)
analyzer = SentimentIntensityAnalyzer()

# Search stock news
company = "Reliance Industries"

articles = newsapi.get_everything(
    q=company,
    language="en",
    sort_by="publishedAt",
    domains="economictimes.indiatimes.com,moneycontrol.com,business-standard.com",
    page_size=5
)

print("\nLatest News Sentiment\n")

for article in articles["articles"]:

    title = article["title"]

    score = analyzer.polarity_scores(title)

    compound = score["compound"]

    if compound >= 0.05:
        sentiment = "POSITIVE 😊"

    elif compound <= -0.05:
        sentiment = "NEGATIVE 😡"

    else:
        sentiment = "NEUTRAL 😐"

    print("News:", title)
    print("Sentiment:", sentiment)
    print("Score:", compound)
    print("-" * 50)