from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class SettingUpdate(BaseModel):
    value: str


@router.get("/")
async def get_settings():
    """Return non-sensitive settings and connection status for each API."""
    from config import settings as s
    return {
        "has_anthropic": bool(s.anthropic_api_key),
        "has_openai": bool(s.openai_api_key),
        "has_stability": bool(s.stability_api_key),
        "has_pexels": bool(s.pexels_api_key),
        "has_unsplash": bool(s.unsplash_access_key),
        "has_instagram": bool(s.instagram_access_token and s.instagram_business_account_id),
        "has_tiktok": bool(s.tiktok_access_token),
        "has_youtube": bool(s.youtube_client_id),
        "has_twitter": bool(s.twitter_api_key),
        "has_linkedin": bool(s.linkedin_access_token),
        "has_facebook": bool(s.facebook_page_access_token),
        "has_supabase": bool(s.supabase_url and s.supabase_key),
        "media_path": s.media_path,
        "app_data_path": s.app_data_path,
    }


@router.get("/env-path")
async def get_env_path():
    from pathlib import Path
    env_path = Path(__file__).parent.parent.parent.parent / 'config' / '.env'
    return {"path": str(env_path.resolve()), "exists": env_path.exists()}
