import asyncio
from typing import Optional
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def sync_to_supabase():
    """Sync local SQLite data to Supabase in the background."""
    if not settings.supabase_url or not settings.supabase_key:
        return

    try:
        from supabase import create_client
        from database import SessionLocal
        from models import Content, Metrics, Niche, Trend, BotRun

        supabase = create_client(settings.supabase_url, settings.supabase_key)
        db = SessionLocal()

        try:
            from datetime import datetime, timedelta
            cutoff = datetime.utcnow() - timedelta(hours=1)

            recent_content = db.query(Content).filter(Content.updated_at >= cutoff).all()
            if recent_content:
                rows = [
                    {
                        "id": c.id,
                        "niche_id": c.niche_id,
                        "topic": c.topic,
                        "platform": c.platform,
                        "status": c.status,
                        "posted_at": c.posted_at.isoformat() if c.posted_at else None,
                        "post_id": c.post_id,
                        "hook": c.hook,
                        "caption": c.caption,
                        "hashtags": c.hashtags,
                        "engagement_rate": 0
                    }
                    for c in recent_content
                ]
                supabase.table("content").upsert(rows).execute()
                logger.info(f"Synced {len(rows)} content items to Supabase")

            recent_metrics = db.query(Metrics).filter(Metrics.recorded_at >= cutoff).all()
            if recent_metrics:
                rows = [
                    {
                        "id": m.id,
                        "content_id": m.content_id,
                        "platform": m.platform,
                        "likes": m.likes,
                        "views": m.views,
                        "reach": m.reach,
                        "engagement_rate": m.engagement_rate,
                        "recorded_at": m.recorded_at.isoformat()
                    }
                    for m in recent_metrics
                ]
                supabase.table("metrics").upsert(rows).execute()

        finally:
            db.close()

    except Exception as e:
        logger.warning(f"Supabase sync failed: {e}")
