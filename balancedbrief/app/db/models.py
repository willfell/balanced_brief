# balancedbrief/app/db/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, ARRAY, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    interests = Column(ARRAY(Text), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False)
    verified_at = Column(TIMESTAMP, nullable=True)
    unsubscribed = Column(Boolean, default=False)
    unsubscribed_at = Column(TIMESTAMP, nullable=True)

class Subreddit(Base):
    __tablename__ = 'subreddits'

    id = Column(Integer, primary_key=True)
    subreddit_name = Column(Text, unique=True, nullable=False)
    category = Column(Text, nullable=False)
    parent_category = Column(Text, nullable=False)

class ParentCategoryHierarchy(Base):
    __tablename__ = 'parent_category_hierarchy'

    id = Column(Integer, primary_key=True)
    parent_category = Column(Text, nullable=False)
    category_order = Column(Integer, unique=True, nullable=False)

class RedditPost(Base):
    __tablename__ = 'reddit_posts'

    id = Column(Integer, primary_key=True)
    post_id = Column(Text, unique=True, nullable=False)
    time = Column(TIMESTAMP, nullable=False)
    subreddit = Column(Text, nullable=False)
    post_title = Column(Text, nullable=False)
    post_score = Column(Integer, nullable=False)
    post_url = Column(Text, nullable=False)
    post_type = Column(Text, nullable=False)
    post_category = Column(Text, nullable=False)
    post_parent_category = Column(Text, nullable=False)

class UnsuccessfulPost(Base):
    __tablename__ = 'unsuccessful_posts'

    id = Column(Integer, primary_key=True)
    time = Column(TIMESTAMP, nullable=False)
    subreddit = Column(Text, nullable=False)
    post_title = Column(Text, nullable=False)
    post_score = Column(Integer, nullable=False)
    post_url = Column(Text, nullable=False)
    post_type = Column(Text, nullable=False)
    post_scrape_fail_reason = Column(Text, nullable=True)
    reddit_posts_id = Column(Integer, ForeignKey('reddit_posts.id'), nullable=False)
    post_id = Column(Text, ForeignKey('reddit_posts.post_id'), unique=True, nullable=False)
    post_category = Column(Text, nullable=False)
    post_parent_category = Column(Text, nullable=True)
    article_title = Column(Text, nullable=True)
    article_authors = Column(ARRAY(Text), nullable=True)
    article_publish_date = Column(Text, nullable=True)
    article_source_url = Column(Text, nullable=True)

class SuccessfulPost(Base):
    __tablename__ = 'successful_posts'

    id = Column(Integer, primary_key=True)
    time = Column(TIMESTAMP, nullable=False)
    subreddit = Column(Text, nullable=False)
    post_title = Column(Text, nullable=False)
    post_score = Column(Integer, nullable=False)
    post_url = Column(Text, nullable=False)
    post_type = Column(Text, nullable=False)
    post_content = Column(Text, nullable=True)
    post_summary = Column(Text, nullable=True)
    post_title_summary = Column(Text, nullable=True)
    post_image_url = Column(Text, nullable=True)
    reddit_posts_id = Column(Integer, ForeignKey('reddit_posts.id'), nullable=False)
    post_id = Column(Text, ForeignKey('reddit_posts.post_id'), unique=True, nullable=False)
    post_category = Column(Text, nullable=False)
    post_parent_category = Column(Text, nullable=False)
    article_title = Column(Text, nullable=True)
    article_authors = Column(ARRAY(Text), nullable=True)
    article_publish_date = Column(Text, nullable=True)
    article_source_url = Column(Text, nullable=True)

class SuccessfulEmailSend(Base):
    __tablename__ = 'successful_email_sends'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    success = Column(Boolean, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())

class UnsuccessfulEmailSend(Base):
    __tablename__ = 'unsuccessful_email_sends'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    success = Column(Boolean, nullable=False)
    failure_reason = Column(Text)
    timestamp = Column(TIMESTAMP, server_default=func.now())