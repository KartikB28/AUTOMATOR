import os
import httpx
from typing import Optional
from config import settings
from platforms.base_platform import BasePlatform

TIKTOK_API_BASE = "https://open.tiktokapis.com/v2"


class TikTokPlatform(BasePlatform):
    def __init__(self):
        super().__init__()

    async def post(self, content) -> dict:
        if not settings.tiktok_access_token:
            raise ValueError("TikTok credentials not configured")

        media_path = None
        for p in (content.media_paths or []):
            if p.endswith(('.mp4', '.mov')):
                media_path = p
                break

        if not media_path:
            from platforms.youtube import YouTubePlatform
            yt = YouTubePlatform()
            media_path = await yt._create_video_from_image(
                content.media_paths[0] if content.media_paths else None,
                content.hook or content.topic
            )

        caption = (content.caption or content.topic)[:2200]
        hashtags = ' '.join(f"#{h.lstrip('#')}" for h in (content.hashtags or []))
        full_caption = f"{caption} {hashtags}".strip()

        async with httpx.AsyncClient() as client:
            init_resp = await client.post(
                f"{TIKTOK_API_BASE}/post/publish/video/init/",
                headers={
                    "Authorization": f"Bearer {settings.tiktok_access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "post_info": {
                        "title": full_caption[:150],
                        "privacy_level": "SELF_ONLY",
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False
                    },
                    "source_info": {
                        "source": "FILE_UPLOAD",
                        "video_size": os.path.getsize(media_path),
                        "chunk_size": os.path.getsize(media_path),
                        "total_chunk_count": 1
                    }
                },
                timeout=30.0
            )
            init_resp.raise_for_status()
            init_data = init_resp.json().get('data', {})
            upload_url = init_data.get('upload_url')
            publish_id = init_data.get('publish_id')

            if not upload_url:
                raise ValueError("TikTok did not return upload URL")

            with open(media_path, 'rb') as f:
                video_bytes = f.read()

            upload_resp = await client.put(
                upload_url,
                content=video_bytes,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Range": f"bytes 0-{len(video_bytes)-1}/{len(video_bytes)}"
                },
                timeout=120.0
            )
            upload_resp.raise_for_status()

            return {
                "post_id": publish_id,
                "url": f"https://www.tiktok.com/@user/video/{publish_id}"
            }

    async def get_metrics(self, post_id: str, platform: str) -> Optional[dict]:
        if not settings.tiktok_access_token:
            return None
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{TIKTOK_API_BASE}/video/query/",
                    headers={
                        "Authorization": f"Bearer {settings.tiktok_access_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "filters": {"video_ids": [post_id]},
                        "fields": ["id", "like_count", "comment_count", "share_count", "view_count", "reach"]
                    },
                    timeout=15.0
                )
                resp.raise_for_status()
                data = resp.json().get('data', {}).get('videos', [])
                if data:
                    v = data[0]
                    return {
                        'likes': v.get('like_count', 0),
                        'comments': v.get('comment_count', 0),
                        'shares': v.get('share_count', 0),
                        'views': v.get('view_count', 0),
                        'reach': v.get('reach', v.get('view_count', 0)),
                        'saves': 0,
                        'impressions': v.get('view_count', 0)
                    }
        except Exception as e:
            self.logger.warning(f"TikTok metrics failed for {post_id}: {e}")
        return None
