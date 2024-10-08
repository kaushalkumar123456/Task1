# models.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from config import DATABASE_URI

# Define the base model class
Base = declarative_base()

# Define the Article model
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    publication_date = Column(DateTime, default=datetime.datetime.utcnow)
    source_url = Column(String, unique=True, nullable=False)
    category = Column(String)
    feed_source = Column(String)

# Create a new database engine
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Create the articles table
Base.metadata.create_all(engine)
