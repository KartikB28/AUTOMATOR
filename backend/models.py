import uuid
from datetime import datetime
from sqlalchemy import (Column, String, Integer, Float, Boolean,
                        DateTime, Text, ForeignKey, JSON)
from sqlalchemy.orm import relationship
from database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Niche(Base):
    __tablename__ = 'niches'
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    keywords = Column(JSON, default=list)
    hashtags = Column(JSON, default=list)
    target_platforms = Column(JSON, default=list)
    posting_frequency = Column(Integer, default=3)
    content_tone = Column(String(50), default='engaging')
    target_audience = Column(String(200), nullable=True)
    brand_voice = Column(Text, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    content = relationship('Content', back_populates='niche', cascade='all, delete-orphan')
    trends = relationship('Trend', back_populates='niche', cascade='all, delete-orphan')
    schedules = relationship('Schedule', back_populates='niche', cascade='all, delete-orphan')


class Content(Base):
    __tablename__ = 'content'
    id = Column(String, primary_key=True, default=generate_uuid)
    niche_id = Column(String, ForeignKey('niches.id'), nullable=False)
    trend_id = Column(String, ForeignKey('trends.id'), nullable=True)
    topic = Column(String(500), nullable=False)
    trend_score = Column(Float, nullable=True)
    platform = Column(String(50), nullable=False)
    content_type = Column(String(50), default='post')

    hook = Column(Text, nullable=True)
    caption = Column(Text, nullable=True)
    script = Column(Text, nullable=True)
    hashtags = Column(JSON, default=list)
    cta = Column(String(300), nullable=True)

    media_type = Column(String(20), nullable=True)
    media_paths = Column(JSON, default=list)
    thumbnail_path = Column(String(500), nullable=True)
    media_source = Column(String(50), nullable=True)

    status = Column(String(30), default='pending')
    scheduled_at = Column(DateTime, nullable=True)
    posted_at = Column(DateTime, nullable=True)
    post_id = Column(String(200), nullable=True)
    post_url = Column(String(500), nullable=True)

    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    niche = relationship('Niche', back_populates='content')
    trend = relationship('Trend', back_populates='content')
    metrics = relationship('Metrics', back_populates='content', cascade='all, delete-orphan')


class Trend(Base):
    __tablename__ = 'trends'
    id = Column(String, primary_key=True, default=generate_uuid)
    niche_id = Column(String, ForeignKey('niches.id'), nullable=False)
    topic = Column(String(500), nullable=False)
    source = Column(String(100), nullable=True)
    raw_score = Column(Float, default=0.0)
    velocity_score = Column(Float, default=0.0)
    volume_score = Column(Float, default=0.0)
    relevance_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    keywords = Column(JSON, default=list)
    hashtags = Column(JSON, default=list)
    source_url = Column(String(500), nullable=True)
    used = Column(Boolean, default=False)
    scraped_at = Column(DateTime, default=datetime.utcnow)

    niche = relationship('Niche', back_populates='trends')
    content = relationship('Content', back_populates='trend')


class Metrics(Base):
    __tablename__ = 'metrics'
    id = Column(String, primary_key=True, default=generate_uuid)
    content_id = Column(String, ForeignKey('content.id'), nullable=False)
    platform = Column(String(50), nullable=False)
    post_id = Column(String(200), nullable=True)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    views = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    content = relationship('Content', back_populates='metrics')


class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(String, primary_key=True, default=generate_uuid)
    niche_id = Column(String, ForeignKey('niches.id'), nullable=False)
    platform = Column(String(50), nullable=False)
    day_of_week = Column(Integer, nullable=True)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    timezone = Column(String(50), default='UTC')

    niche = relationship('Niche', back_populates='schedules')


class BotRun(Base):
    __tablename__ = 'bot_runs'
    id = Column(String, primary_key=True, default=generate_uuid)
    bot_name = Column(String(50), nullable=False)
    status = Column(String(20), default='running')
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    items_processed = Column(Integer, default=0)
    items_succeeded = Column(Integer, default=0)
    items_failed = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    niche_id = Column(String, nullable=True)


class SystemSetting(Base):
    __tablename__ = 'system_settings'
    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
