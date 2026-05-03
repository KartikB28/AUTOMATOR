from fastapi import APIRouter, Request, HTTPException
from typing import Optional

router = APIRouter()


def get_orchestrator(request: Request):
    if not hasattr(request.app.state, 'orchestrator'):
        raise HTTPException(503, "Orchestrator not initialized")
    return request.app.state.orchestrator


@router.get("/status")
async def get_bot_status(request: Request):
    orch = get_orchestrator(request)
    return orch.get_status()


@router.post("/{bot_name}/trigger")
async def trigger_bot(bot_name: str, request: Request):
    orch = get_orchestrator(request)
    valid = ['scout', 'builder', 'creator', 'publisher', 'analyst']
    if bot_name not in valid:
        raise HTTPException(400, f"Invalid bot name. Must be one of: {valid}")
    result = await orch.trigger_bot(bot_name)
    return result


@router.post("/{bot_name}/pause")
async def pause_bot(bot_name: str, request: Request):
    orch = get_orchestrator(request)
    orch.pause_bot(bot_name)
    return {"paused": True, "bot": bot_name}


@router.post("/{bot_name}/resume")
async def resume_bot(bot_name: str, request: Request):
    orch = get_orchestrator(request)
    orch.resume_bot(bot_name)
    return {"resumed": True, "bot": bot_name}


@router.post("/pause-all")
async def pause_all(request: Request):
    orch = get_orchestrator(request)
    orch.pause_all()
    return {"paused": True}


@router.post("/resume-all")
async def resume_all(request: Request):
    orch = get_orchestrator(request)
    orch.resume_all()
    return {"resumed": True}


@router.get("/runs")
async def get_bot_runs(limit: int = 50, bot_name: Optional[str] = None):
    from database import SessionLocal
    from models import BotRun
    db = SessionLocal()
    try:
        q = db.query(BotRun).order_by(BotRun.started_at.desc())
        if bot_name:
            q = q.filter(BotRun.bot_name == bot_name)
        runs = q.limit(limit).all()
        return [
            {
                "id": r.id,
                "bot_name": r.bot_name,
                "status": r.status,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                "items_processed": r.items_processed,
                "items_succeeded": r.items_succeeded,
                "items_failed": r.items_failed,
                "error_message": r.error_message
            }
            for r in runs
        ]
    finally:
        db.close()
