import tweepy
from typing import Optional
from config import settings
from platforms.base_platform import BasePlatform


class TwitterPlatform(BasePlatform):
    def __init__(self):
        super().__init__()
        if (settings.twitter_api_key and settings.twitter_api_secret and
                settings.twitter_access_token and settings.twitter_access_token_secret):
            self.client = tweepy.Client(
                bearer_token=settings.twitter_bearer_token,
                consumer_key=settings.twitter_api_key,
                consumer_secret=settings.twitter_api_secret,
                access_token=settings.twitter_access_token,
                access_token_secret=settings.twitter_access_token_secret
            )
            self.auth = tweepy.OAuth1UserHandler(
                settings.twitter_api_key,
                settings.twitter_api_secret,
                settings.twitter_access_token,
                settings.twitter_access_token_secret
            )
            self.api_v1 = tweepy.API(self.auth)
        else:
            self.client = None
            self.api_v1 = None

    async def post(self, content) -> dict:
        if not self.client:
            raise ValueError("Twitter credentials not configured")

        tweet_text = (content.caption or content.topic)[:280]

        media_ids = []
        if content.thumbnail_path and self.api_v1:
            try:
                media = self.api_v1.media_upload(content.thumbnail_path)
                media_ids.append(media.media_id)
            except Exception as e:
                self.logger.warning(f"Twitter media upload failed: {e}")

        response = self.client.create_tweet(
            text=tweet_text,
            media_ids=media_ids if media_ids else None
        )
        post_id = str(response.data['id'])
        return {
            "post_id": post_id,
            "url": f"https://twitter.com/i/web/status/{post_id}"
        }

    async def get_metrics(self, post_id: str, platform: str) -> Optional[dict]:
        if not self.client:
            return None
        try:
            response = self.client.get_tweet(
                id=post_id,
                tweet_fields=["public_metrics"]
            )
            if response.data:
                m = response.data.public_metrics
                return {
                    "likes": m.get('like_count', 0),
                    "comments": m.get('reply_count', 0),
                    "shares": m.get('retweet_count', 0),
                    "views": m.get('impression_count', 0),
                    "reach": m.get('impression_count', 0),
                    "saves": 0,
                    "impressions": m.get('impression_count', 0)
                }
        except Exception as e:
            self.logger.warning(f"Twitter metrics fetch failed for {post_id}: {e}")
        return None
