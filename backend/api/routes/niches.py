import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class NicheCreate(BaseModel):
    name: str
    description: Optional[str] = None
    keywords: List[str] = []
    hashtags: List[str] = []
    target_platforms: List[str] = ['instagram', 'tiktok', 'youtube', 'twitter', 'linkedin', 'facebook']
    posting_frequency: int = 3
    content_tone: str = 'engaging'
    target_audience: Optional[str] = None
    brand_voice: Optional[str] = None


class NicheUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    target_platforms: Optional[List[str]] = None
    posting_frequency: Optional[int] = None
    content_tone: Optional[str] = None
    target_audience: Optional[str] = None
    brand_voice: Optional[str] = None
    active: Optional[bool] = None


@router.get("/")
async def list_niches():
    from database import SessionLocal
    from models import Niche
    db = SessionLocal()
    try:
        niches = db.query(Niche).order_by(Niche.created_at.desc()).all()
        return [_niche_to_dict(n) for n in niches]
    finally:
        db.close()


@router.post("/")
async def create_niche(data: NicheCreate):
    from database import SessionLocal
    from models import Niche
    db = SessionLocal()
    try:
        niche = Niche(
            id=str(uuid.uuid4()),
            name=data.name,
            description=data.description,
            keywords=data.keywords,
            hashtags=data.hashtags,
            target_platforms=data.target_platforms,
            posting_frequency=data.posting_frequency,
            content_tone=data.content_tone,
            target_audience=data.target_audience,
            brand_voice=data.brand_voice,
            active=True,
            created_at=datetime.utcnow()
        )
        db.add(niche)
        db.commit()
        db.refresh(niche)
        return _niche_to_dict(niche)
    finally:
        db.close()


@router.get("/{niche_id}")
async def get_niche(niche_id: str):
    from database import SessionLocal
    from models import Niche
    db = SessionLocal()
    try:
        niche = db.query(Niche).filter(Niche.id == niche_id).first()
        if not niche:
            raise HTTPException(404, "Niche not found")
        return _niche_to_dict(niche)
    finally:
        db.close()


@router.patch("/{niche_id}")
async def update_niche(niche_id: str, data: NicheUpdate):
    from database import SessionLocal
    from models import Niche
    db = SessionLocal()
    try:
        niche = db.query(Niche).filter(Niche.id == niche_id).first()
        if not niche:
            raise HTTPException(404, "Niche not found")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(niche, field, value)
        niche.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(niche)
        return _niche_to_dict(niche)
    finally:
        db.close()


@router.delete("/{niche_id}")
async def delete_niche(niche_id: str):
    from database import SessionLocal
    from models import Niche
    db = SessionLocal()
    try:
        niche = db.query(Niche).filter(Niche.id == niche_id).first()
        if not niche:
            raise HTTPException(404, "Niche not found")
        db.delete(niche)
        db.commit()
        return {"deleted": True}
    finally:
        db.close()


def _niche_to_dict(n) -> dict:
    return {
        "id": n.id,
        "name": n.name,
        "description": n.description,
        "keywords": n.keywords or [],
        "hashtags": n.hashtags or [],
        "target_platforms": n.target_platforms or [],
        "posting_frequency": n.posting_frequency,
        "content_tone": n.content_tone,
        "target_audience": n.target_audience,
        "brand_voice": n.brand_voice,
        "active": n.active,
        "created_at": n.created_at.isoformat() if n.created_at else None,
    }
