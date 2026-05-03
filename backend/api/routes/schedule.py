import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class ScheduleCreate(BaseModel):
    niche_id: str
    platform: str
    day_of_week: Optional[int] = None
    hour: int
    minute: int = 0
    active: bool = True
    timezone: str = "UTC"


@router.get("/{niche_id}")
async def get_schedule(niche_id: str):
    from database import SessionLocal
    from models import Schedule
    db = SessionLocal()
    try:
        schedules = db.query(Schedule).filter(Schedule.niche_id == niche_id).all()
        return [_to_dict(s) for s in schedules]
    finally:
        db.close()


@router.post("/")
async def create_schedule(data: ScheduleCreate):
    from database import SessionLocal
    from models import Schedule
    db = SessionLocal()
    try:
        sched = Schedule(id=str(uuid.uuid4()), **data.model_dump())
        db.add(sched)
        db.commit()
        db.refresh(sched)
        return _to_dict(sched)
    finally:
        db.close()


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: str):
    from database import SessionLocal
    from models import Schedule
    db = SessionLocal()
    try:
        sched = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not sched:
            raise HTTPException(404, "Schedule not found")
        db.delete(sched)
        db.commit()
        return {"deleted": True}
    finally:
        db.close()


@router.patch("/{schedule_id}/toggle")
async def toggle_schedule(schedule_id: str):
    from database import SessionLocal
    from models import Schedule
    db = SessionLocal()
    try:
        sched = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not sched:
            raise HTTPException(404, "Schedule not found")
        sched.active = not sched.active
        db.commit()
        return _to_dict(sched)
    finally:
        db.close()


def _to_dict(s) -> dict:
    return {
        "id": s.id,
        "niche_id": s.niche_id,
        "platform": s.platform,
        "day_of_week": s.day_of_week,
        "hour": s.hour,
        "minute": s.minute,
        "active": s.active,
        "timezone": s.timezone
    }
