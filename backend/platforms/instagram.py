import httpx
from typing import Optional
from pathlib import Path
from config import settings
from platforms.base_platform import BasePlatform

GRAPH_API_BASE = "https://graph.facebook.com/v18.0"


class InstagramPlatform(BasePlatform):
    def __init__(self):
        super().__init__()
        self.account_id = settings.instagram_business_account_id
        self.token = settings.instagram_access_token

    async def post(self, content) -> dict:
        if not self.account_id or not self.token:
            raise ValueError("Instagram credentials not configured")

        caption = self._build_caption(content)
        image_url = await self._upload_to_accessible_url(
            content.media_paths[0] if content.media_paths else None
        )

        async with httpx.AsyncClient() as client:
            container_resp = await client.post(
                f"{GRAPH_API_BASE}/{self.account_id}/media",
                params={
                    "image_url": image_url,
                    "caption": caption,
                    "access_token": self.token
                },
                timeout=30.0
            )
            container_resp.raise_for_status()
            container_id = container_resp.json()["id"]

            publish_resp = await client.post(
                f"{GRAPH_API_BASE}/{self.account_id}/media_publish",
                params={
                    "creation_id": container_id,
                    "access_token": self.token
                },
                timeout=30.0
            )
            publish_resp.raise_for_status()
            post_id = publish_resp.json()["id"]

            return {
                "post_id": post_id,
                "url": f"https://www.instagram.com/p/{post_id}/"
            }

    async def get_metrics(self, post_id: str, platform: str) -> Optional[dict]:
        if not self.token:
            return None
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{GRAPH_API_BASE}/{post_id}/insights",
                    params={
                        "metric": "impressions,reach,likes,comments,shares,saved",
                        "access_token": self.token
                    },
                    timeout=15.0
                )
                resp.raise_for_status()
                data = resp.json().get("data", [])
                result = {}
                for item in data:
                    name = item["name"]
                    value = item["values"][0]["value"] if item.get("values") else 0
                    result[name] = value
                return {
                    "impressions": result.get("impressions", 0),
                    "reach": result.get("reach", 0),
                    "likes": result.get("likes", 0),
                    "comments": result.get("comments", 0),
                    "shares": result.get("shares", 0),
                    "saves": result.get("saved", 0),
                    "views": result.get("impressions", 0)
                }
        except Exception as e:
            self.logger.warning(f"Failed to get Instagram metrics for {post_id}: {e}")
            return None

    def _build_caption(self, content) -> str:
        parts = [content.caption or '']
        if content.hashtags:
            parts.append('\n\n' + ' '.join(f"#{h.lstrip('#')}" for h in content.hashtags))
        return '\n'.join(parts)[:2200]

    async def _upload_to_accessible_url(self, local_path: Optional[str]) -> str:
        if not local_path:
            raise ValueError("No media path provided")
        media_base = Path(settings.media_path)
        file_path = Path(local_path)
        try:
            relative = file_path.relative_to(media_base)
            return f"http://localhost:{settings.port}/media/{relative}"
        except ValueError:
            return f"file://{local_path}"
