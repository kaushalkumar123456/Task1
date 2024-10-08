# config.py

# PostgreSQL settings
DATABASE_URI = 'postgresql://user:password@localhost:5432/news_db'

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
