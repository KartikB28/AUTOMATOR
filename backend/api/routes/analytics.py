from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/overview")
async def get_analytics_overview(days: int = Query(30, le=365)):
    from database import SessionLocal
    from models import Metrics, Content
    from sqlalchemy import func
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=days)
        metrics = db.query(Metrics).filter(Metrics.recorded_at >= cutoff).all()

        if not metrics:
            return {"total_posts": 0, "total_likes": 0, "total_views": 0,
                    "total_reach": 0, "avg_engagement_rate": 0,
                    "by_platform": {}, "top_content": []}

        total_likes = sum(m.likes for m in metrics)
        total_views = sum(m.views for m in metrics)
        total_reach = sum(m.reach for m in metrics)
        avg_engagement = round(sum(m.engagement_rate for m in metrics) / len(metrics), 2)

        by_platform = {}
        for m in metrics:
            if m.platform not in by_platform:
                by_platform[m.platform] = {
                    'posts': 0, 'likes': 0, 'views': 0,
                    'reach': 0, 'avg_engagement': []
                }
            by_platform[m.platform]['posts'] += 1
            by_platform[m.platform]['likes'] += m.likes
            by_platform[m.platform]['views'] += m.views
            by_platform[m.platform]['reach'] += m.reach
            by_platform[m.platform]['avg_engagement'].append(m.engagement_rate)

        for p in by_platform:
            eng = by_platform[p]['avg_engagement']
            by_platform[p]['avg_engagement'] = round(sum(eng) / len(eng), 2) if eng else 0

        top = sorted(metrics, key=lambda m: m.engagement_rate, reverse=True)[:5]
        top_content = []
        for m in top:
            c = db.query(Content).filter(Content.id == m.content_id).first()
            if c:
                top_content.append({
                    "content_id": c.id,
                    "topic": c.topic,
                    "platform": c.platform,
                    "engagement_rate": m.engagement_rate,
                    "likes": m.likes,
                    "views": m.views,
                    "thumbnail_path": c.thumbnail_path
                })

        return {
            "total_posts": len(set(m.content_id for m in metrics)),
            "total_likes": total_likes,
            "total_views": total_views,
            "total_reach": total_reach,
            "avg_engagement_rate": avg_engagement,
            "by_platform": by_platform,
            "top_content": top_content
        }
    finally:
        db.close()


@router.get("/digest")
async def get_digest():
    from database import SessionLocal
    from models import SystemSetting
    db = SessionLocal()
    try:
        setting = db.query(SystemSetting).filter(SystemSetting.key == 'latest_digest').first()
        if setting:
            return {"digest": setting.value, "updated_at": setting.updated_at.isoformat() if setting.updated_at else None}
        return {"digest": None, "updated_at": None}
    finally:
        db.close()


@router.get("/timeseries")
async def get_timeseries(metric: str = "views", days: int = 30, platform: Optional[str] = None):
    from database import SessionLocal
    from models import Metrics
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=days)
        q = db.query(Metrics).filter(Metrics.recorded_at >= cutoff)
        if platform:
            q = q.filter(Metrics.platform == platform)
        metrics = q.all()

        by_date = {}
        for m in metrics:
            date_key = m.recorded_at.strftime('%Y-%m-%d')
            if date_key not in by_date:
                by_date[date_key] = 0
            val = getattr(m, metric, 0) or 0
            by_date[date_key] += val

        result = [{"date": k, "value": v} for k, v in sorted(by_date.items())]
        return result
    finally:
        db.close()
