from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class NicheBase(BaseModel):
    name: str
    description: Optional[str] = None
    keywords: List[str] = []
    hashtags: List[str] = []
    target_platforms: List[str] = []
    posting_frequency: int = 3
    content_tone: str = 'engaging'
    target_audience: Optional[str] = None
    brand_voice: Optional[str] = None


class NicheResponse(NicheBase):
    id: str
    active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ContentResponse(BaseModel):
    id: str
    niche_id: str
    topic: str
    platform: str
    content_type: str
    status: str
    hook: Optional[str] = None
    caption: Optional[str] = None
    hashtags: List[str] = []
    cta: Optional[str] = None
    media_type: Optional[str] = None
    media_paths: List[str] = []
    thumbnail_path: Optional[str] = None
    media_source: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    posted_at: Optional[datetime] = None
    post_id: Optional[str] = None
    post_url: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    trend_score: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScheduleBase(BaseModel):
    niche_id: str
    platform: str
    day_of_week: Optional[int] = None
    hour: int
    minute: int = 0
    active: bool = True
    timezone: str = "UTC"


class BotRunResponse(BaseModel):
    id: str
    bot_name: str
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    items_processed: int = 0
    items_succeeded: int = 0
    items_failed: int = 0
    error_message: Optional[str] = None
