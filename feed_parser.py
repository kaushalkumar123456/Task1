# feed_parser.py
import feedparser
from models import Article, Session
from config import DATABASE_URI
import logging

# List of RSS feeds
rss_feeds = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]

# Set up logging
logging.basicConfig(level=logging.INFO)

def parse_feed(url, feed_source):
    session = Session()
    feed = feedparser.parse(url)

    for entry in feed.entries:
        # Use entry.get to avoid KeyError, and set a default value if summary is missing
        title = entry.get("title", "No Title")
        content = entry.get("summary", entry.get("description", "No Content Available"))
        publication_date = entry.get("published", None)  # Some feeds might use 'updated'

        # Create an Article instance
        article = Article(
            title=title,
            content=content,
            publication_date=publication_date,
            source_url=entry.link,
            feed_source=feed_source
        )

        # Check for duplicates based on source_url
        if not session.query(Article).filter_by(source_url=entry.link).first():
            session.add(article)
            session.commit()
            logging.info(f"Stored article: {title}")
    session.close()

if __name__ == '__main__':
    for url in rss_feeds:
        parse_feed(url, url.split('/')[2])
