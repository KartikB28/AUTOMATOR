import httpx
import base64
from typing import Optional
from config import settings
from platforms.base_platform import BasePlatform


class LinkedInPlatform(BasePlatform):
    def __init__(self):
        super().__init__()

    async def post(self, content) -> dict:
        if not settings.linkedin_access_token or not settings.linkedin_person_id:
            raise ValueError("LinkedIn credentials not configured")

        caption = content.caption or content.topic
        headers = {
            "Authorization": f"Bearer {settings.linkedin_access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        body = {
            "author": settings.linkedin_person_id,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": caption[:3000]
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers=headers,
                json=body,
                timeout=30.0
            )
            resp.raise_for_status()
            post_id = resp.json().get('id', '')
            return {
                "post_id": post_id,
                "url": f"https://www.linkedin.com/feed/update/{post_id}/"
            }

    async def get_metrics(self, post_id: str, platform: str) -> Optional[dict]:
        if not settings.linkedin_access_token:
            return None
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"https://api.linkedin.com/v2/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity={settings.linkedin_person_id}",
                    headers={"Authorization": f"Bearer {settings.linkedin_access_token}"},
                    timeout=15.0
                )
                return {'likes': 0, 'comments': 0, 'shares': 0, 'views': 0, 'reach': 0, 'saves': 0, 'impressions': 0}
        except Exception as e:
            self.logger.warning(f"LinkedIn metrics failed: {e}")
        return None
