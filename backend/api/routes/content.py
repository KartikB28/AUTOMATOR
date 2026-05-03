from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List

router = APIRouter()


@router.get("/")
async def get_content(
    niche_id: Optional[str] = None,
    platform: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(50, le=200),
    offset: int = 0
):
    from database import SessionLocal
    from models import Content
    db = SessionLocal()
    try:
        q = db.query(Content).order_by(Content.created_at.desc())
        if niche_id:
            q = q.filter(Content.niche_id == niche_id)
        if platform:
            q = q.filter(Content.platform == platform)
        if status:
            q = q.filter(Content.status == status)
        items = q.offset(offset).limit(limit).all()
        return [_content_to_dict(c) for c in items]
    finally:
        db.close()


@router.get("/{content_id}")
async def get_content_item(content_id: str):
    from database import SessionLocal
    from models import Content
    db = SessionLocal()
    try:
        item = db.query(Content).filter(Content.id == content_id).first()
        if not item:
            raise HTTPException(404, "Content not found")
        return _content_to_dict(item)
    finally:
        db.close()


@router.delete("/{content_id}")
async def delete_content(content_id: str):
    from database import SessionLocal
    from models import Content
    db = SessionLocal()
    try:
        item = db.query(Content).filter(Content.id == content_id).first()
        if not item:
            raise HTTPException(404, "Content not found")
        db.delete(item)
        db.commit()
        return {"deleted": True}
    finally:
        db.close()


@router.patch("/{content_id}")
async def update_content(content_id: str, updates: dict):
    from database import SessionLocal
    from models import Content
    db = SessionLocal()
    try:
        item = db.query(Content).filter(Content.id == content_id).first()
        if not item:
            raise HTTPException(404, "Content not found")
        allowed = ['caption', 'hook', 'script', 'hashtags', 'status', 'scheduled_at']
        for key, val in updates.items():
            if key in allowed:
                setattr(item, key, val)
        db.commit()
        return _content_to_dict(item)
    finally:
        db.close()


@router.get("/stats/summary")
async def get_content_stats():
    from database import SessionLocal
    from models import Content
    from sqlalchemy import func
    db = SessionLocal()
    try:
        by_status = db.query(Content.status, func.count(Content.id)).group_by(Content.status).all()
        by_platform = db.query(Content.platform, func.count(Content.id)).group_by(Content.platform).all()
        return {
            "by_status": {s: c for s, c in by_status},
            "by_platform": {p: c for p, c in by_platform},
            "total": db.query(Content).count()
        }
    finally:
        db.close()


def _content_to_dict(c) -> dict:
    return {
        "id": c.id,
        "niche_id": c.niche_id,
        "topic": c.topic,
        "platform": c.platform,
        "content_type": c.content_type,
        "status": c.status,
        "hook": c.hook,
        "caption": c.caption,
        "hashtags": c.hashtags or [],
        "cta": c.cta,
        "media_type": c.media_type,
        "media_paths": c.media_paths or [],
        "thumbnail_path": c.thumbnail_path,
        "media_source": c.media_source,
        "scheduled_at": c.scheduled_at.isoformat() if c.scheduled_at else None,
        "posted_at": c.posted_at.isoformat() if c.posted_at else None,
        "post_id": c.post_id,
        "post_url": c.post_url,
        "error_message": c.error_message,
        "retry_count": c.retry_count,
        "trend_score": c.trend_score,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }
