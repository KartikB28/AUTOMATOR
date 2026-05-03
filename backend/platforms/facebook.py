import httpx
from typing import Optional
from config import settings
from platforms.base_platform import BasePlatform

GRAPH_API_BASE = "https://graph.facebook.com/v18.0"


class FacebookPlatform(BasePlatform):
    def __init__(self):
        super().__init__()

    async def post(self, content) -> dict:
        if not settings.facebook_page_access_token or not settings.facebook_page_id:
            raise ValueError("Facebook credentials not configured")

        caption = content.caption or content.topic
        hashtags = ' '.join(f"#{h.lstrip('#')}" for h in (content.hashtags or []))
        full_message = f"{caption}\n\n{hashtags}".strip()

        async with httpx.AsyncClient() as client:
            if content.thumbnail_path:
                with open(content.thumbnail_path, 'rb') as f:
                    resp = await client.post(
                        f"{GRAPH_API_BASE}/{settings.facebook_page_id}/photos",
                        params={"access_token": settings.facebook_page_access_token},
                        data={"message": full_message[:63206]},
                        files={"source": f},
                        timeout=60.0
                    )
            else:
                resp = await client.post(
                    f"{GRAPH_API_BASE}/{settings.facebook_page_id}/feed",
                    params={"access_token": settings.facebook_page_access_token},
                    json={"message": full_message[:63206]},
                    timeout=30.0
                )
            resp.raise_for_status()
            post_id = resp.json().get('id', resp.json().get('post_id', ''))
            return {
                "post_id": post_id,
                "url": f"https://facebook.com/{post_id}"
            }

    async def get_metrics(self, post_id: str, platform: str) -> Optional[dict]:
        if not settings.facebook_page_access_token:
            return None
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{GRAPH_API_BASE}/{post_id}/insights",
                    params={
                        "metric": "post_impressions,post_reach,post_reactions_by_type_total,post_clicks",
                        "access_token": settings.facebook_page_access_token
                    },
                    timeout=15.0
                )
                resp.raise_for_status()
                data = {d['name']: d['values'][0]['value'] for d in resp.json().get('data', [])}
                reactions = data.get('post_reactions_by_type_total', {})
                total_reactions = sum(reactions.values()) if isinstance(reactions, dict) else 0
                return {
                    'likes': total_reactions,
                    'comments': 0,
                    'shares': 0,
                    'views': data.get('post_impressions', 0),
                    'reach': data.get('post_reach', 0),
                    'saves': 0,
                    'impressions': data.get('post_impressions', 0),
                    'clicks': data.get('post_clicks', 0)
                }
        except Exception as e:
            self.logger.warning(f"Facebook metrics failed for {post_id}: {e}")
        return None
