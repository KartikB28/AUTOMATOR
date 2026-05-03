import asyncio
import uuid
from datetime import datetime, timedelta
from typing import List

from database import SessionLocal
from models import Content, Schedule, Niche
from bots.base_bot import BaseBot
from platforms.instagram import InstagramPlatform
from platforms.tiktok import TikTokPlatform
from platforms.youtube import YouTubePlatform
from platforms.twitter import TwitterPlatform
from platforms.linkedin import LinkedInPlatform
from platforms.facebook import FacebookPlatform
from utils.notifications import send_notification

PLATFORM_HANDLERS = {
    'instagram': InstagramPlatform,
    'tiktok': TikTokPlatform,
    'youtube': YouTubePlatform,
    'twitter': TwitterPlatform,
    'linkedin': LinkedInPlatform,
    'facebook': FacebookPlatform,
}


class PublisherBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.handlers = {name: cls() for name, cls in PLATFORM_HANDLERS.items()}

    async def run(self) -> dict:
        self.logger.info("PublisherBot starting run")
        processed = 0
        succeeded = 0
        failed = 0

        db = self.get_db()
        try:
            now = datetime.utcnow()
            items = (db.query(Content)
                     .filter(
                         Content.status == 'media_ready',
                         Content.retry_count < Content.max_retries
                     )
                     .order_by(Content.created_at.asc())
                     .limit(10).all())

            for item in items:
                if not self._is_posting_time(db, item.niche_id, item.platform, now):
                    continue

                if self._daily_limit_reached(db, item.niche_id, item.platform, now):
                    continue

                try:
                    item.status = 'posting'
                    db.commit()

                    handler = self.handlers.get(item.platform)
                    if not handler:
                        raise ValueError(f"No handler for platform: {item.platform}")

                    post_result = await handler.post(item)

                    item.status = 'posted'
                    item.posted_at = datetime.utcnow()
                    item.post_id = post_result.get('post_id')
                    item.post_url = post_result.get('url')
                    db.commit()

                    send_notification(
                        f"Posted to {item.platform.title()}",
                        f"{item.topic[:60]}..."
                    )

                    processed += 1
                    succeeded += 1
                    self.logger.info(f"Successfully posted to {item.platform}: {item.id}")

                except Exception as e:
                    self.logger.error(f"PublisherBot failed to post {item.id} to {item.platform}: {e}")
                    item.retry_count = (item.retry_count or 0) + 1
                    if item.retry_count >= item.max_retries:
                        item.status = 'failed'
                        item.error_message = str(e)
                        send_notification(
                            f"Failed to post to {item.platform.title()}",
                            f"After {item.max_retries} retries: {str(e)[:60]}"
                        )
                    else:
                        item.status = 'media_ready'
                        item.error_message = str(e)
                    db.commit()
                    processed += 1
                    failed += 1

                await asyncio.sleep(2)
        finally:
            db.close()

        return {'processed': processed, 'succeeded': succeeded, 'failed': failed}

    def _is_posting_time(self, db, niche_id: str, platform: str, now: datetime) -> bool:
        """Check if the current time falls within a scheduled posting window for this niche+platform."""
        schedules = (db.query(Schedule)
                     .filter(
                         Schedule.niche_id == niche_id,
                         Schedule.platform == platform,
                         Schedule.active == True
                     ).all())

        if not schedules:
            return True

        current_dow = now.weekday()
        current_hour = now.hour
        current_minute = now.minute

        for sched in schedules:
            if sched.day_of_week is not None and sched.day_of_week != current_dow:
                continue
            sched_minutes = sched.hour * 60 + sched.minute
            current_minutes = current_hour * 60 + current_minute
            if abs(current_minutes - sched_minutes) <= 15:
                return True
        return False

    def _daily_limit_reached(self, db, niche_id: str, platform: str, now: datetime) -> bool:
        """Prevent posting more than the niche's posting_frequency per day."""
        niche = db.query(Niche).filter(Niche.id == niche_id).first()
        if not niche:
            return False

        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        posted_today = (db.query(Content)
                        .filter(
                            Content.niche_id == niche_id,
                            Content.platform == platform,
                            Content.status == 'posted',
                            Content.posted_at >= day_start
                        ).count())

        num_platforms = len(niche.target_platforms or [platform])
        per_platform_limit = max(1, niche.posting_frequency // max(1, num_platforms))
        return posted_today >= per_platform_limit
