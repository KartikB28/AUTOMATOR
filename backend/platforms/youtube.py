import os
import httpx
import subprocess
from typing import Optional
from config import settings
from platforms.base_platform import BasePlatform


class YouTubePlatform(BasePlatform):
    def __init__(self):
        super().__init__()

    def _get_credentials(self):
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        creds = Credentials(
            token=None,
            refresh_token=settings.youtube_refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=settings.youtube_client_id,
            client_secret=settings.youtube_client_secret,
            scopes=['https://www.googleapis.com/auth/youtube.upload',
                    'https://www.googleapis.com/auth/youtube.readonly']
        )
        creds.refresh(Request())
        return creds

    async def post(self, content) -> dict:
        if not settings.youtube_client_id:
            raise ValueError("YouTube credentials not configured")

        import googleapiclient.discovery
        from googleapiclient.http import MediaFileUpload

        creds = self._get_credentials()
        youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)

        description = content.caption or content.topic
        hashtag_str = ' '.join(f"#{h.lstrip('#')}" for h in (content.hashtags or []))
        full_description = f"{description}\n\n{hashtag_str}"

        media_path = None
        if content.media_paths:
            for p in content.media_paths:
                if p.endswith(('.mp4', '.mov', '.avi')):
                    media_path = p
                    break

        if not media_path:
            media_path = await self._create_video_from_image(
                content.media_paths[0] if content.media_paths else None,
                content.hook or content.topic
            )

        media = MediaFileUpload(media_path, chunksize=-1, resumable=True,
                                mimetype='video/mp4')

        request = youtube.videos().insert(
            part='snippet,status',
            body={
                'snippet': {
                    'title': (content.hook or content.topic)[:100],
                    'description': full_description[:5000],
                    'tags': [h.lstrip('#') for h in (content.hashtags or [])],
                    'categoryId': '22',
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False,
                }
            },
            media_body=media
        )

        response = request.execute()
        video_id = response['id']
        return {
            "post_id": video_id,
            "url": f"https://youtube.com/shorts/{video_id}"
        }

    async def get_metrics(self, post_id: str, platform: str) -> Optional[dict]:
        if not settings.youtube_client_id:
            return None
        try:
            import googleapiclient.discovery
            creds = self._get_credentials()
            youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)
            response = youtube.videos().list(
                part='statistics',
                id=post_id
            ).execute()
            items = response.get('items', [])
            if items:
                stats = items[0]['statistics']
                return {
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                    'shares': 0,
                    'saves': 0,
                    'reach': int(stats.get('viewCount', 0)),
                    'impressions': int(stats.get('viewCount', 0))
                }
        except Exception as e:
            self.logger.warning(f"YouTube metrics failed for {post_id}: {e}")
        return None

    async def _create_video_from_image(self, image_path: Optional[str], text: str) -> str:
        """Use ffmpeg to create a 30-second video from a still image."""
        if not image_path:
            raise ValueError("No image provided for video creation")

        output_path = image_path.replace('.jpg', '_video.mp4').replace('.png', '_video.mp4')
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', image_path,
            '-c:v', 'libx264',
            '-t', '30',
            '-pix_fmt', 'yuv420p',
            '-vf', 'scale=1080:1920',
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {result.stderr}")
        return output_path
