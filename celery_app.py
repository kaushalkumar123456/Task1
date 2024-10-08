# celery_app.py
from celery import Celery
from models import Session, Article
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
import spacy
import logging

# Configure Celery
celery_app = Celery('news_aggregator', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Define categories
categories = {
    "terrorism": ["terrorism", "riot", "protest", "unrest"],
    "positive": ["uplifting", "positive", "good news"],
    "natural_disaster": ["earthquake", "flood", "storm", "disaster"],
    "others": []
}

@celery_app.task
def categorize_article(article_id):
    session = Session()
    article = session.query(Article).get(article_id)

    if article:
        # Classify the content
        doc = nlp(article.content)
        category = "others"
        for cat, keywords in categories.items():
            if any(keyword in doc.text.lower() for keyword in keywords):
                category = cat
                break
        article.category = category
        session.commit()
        logging.info(f"Categorized article {article_id} as {category}")
    session.close()
