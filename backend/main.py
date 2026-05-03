import sys
import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from database import init_db
from orchestrator import Orchestrator
from utils.logger import setup_logger

logger = setup_logger(__name__)
orchestrator: Orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global orchestrator
    logger.info("Starting The Automator backend...")

    init_db()
    logger.info("Database initialized")

    Path(settings.media_path).mkdir(parents=True, exist_ok=True)

    orchestrator = Orchestrator()
    await orchestrator.start()
    app.state.orchestrator = orchestrator
    logger.info("Orchestrator started")

    yield

    if orchestrator:
        await orchestrator.stop()
    logger.info("Backend shutdown complete")


app = FastAPI(
    title="The Automator API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "app://.", "file://"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

media_path = Path(settings.media_path)
media_path.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(media_path)), name="media")

from api.routes import bots, content, niches, settings as settings_routes, analytics, schedule, system

app.include_router(bots.router, prefix="/api/bots", tags=["bots"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(niches.router, prefix="/api/niches", tags=["niches"])
app.include_router(settings_routes.router, prefix="/api/settings", tags=["settings"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(schedule.router, prefix="/api/schedule", tags=["schedule"])
app.include_router(system.router, prefix="/api/system", tags=["system"])
