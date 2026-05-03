from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "The Automator API"
    }


@router.get("/stats")
async def get_system_stats():
    from database import SessionLocal
    from models import Niche, Content, BotRun, Metrics
    db = SessionLocal()
    try:
        return {
            "niches": db.query(Niche).filter(Niche.active == True).count(),
            "total_content": db.query(Content).count(),
            "posted_content": db.query(Content).filter(Content.status == 'posted').count(),
            "pending_content": db.query(Content).filter(Content.status.in_(['pending', 'media_ready', 'media_pending'])).count(),
            "total_metrics": db.query(Metrics).count(),
        }
    finally:
        db.close()
