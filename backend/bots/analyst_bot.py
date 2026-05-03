import asyncio
import uuid
from datetime import datetime, timedelta

import anthropic

from config import settings
from database import SessionLocal
from models import Content, Metrics, Niche, SystemSetting
from bots.base_bot import BaseBot
from platforms.instagram import InstagramPlatform
from platforms.tiktok import TikTokPlatform
from platforms.youtube import YouTubePlatform
from platforms.twitter import TwitterPlatform
from platforms.linkedin import LinkedInPlatform
from platforms.facebook import FacebookPlatform


class AnalystBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.handlers = {
            'instagram': InstagramPlatform(),
            'tiktok': TikTokPlatform(),
            'youtube': YouTubePlatform(),
            'twitter': TwitterPlatform(),
            'linkedin': LinkedInPlatform(),
            'facebook': FacebookPlatform(),
        }
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key) if settings.anthropic_api_key else None

    async def run(self) -> dict:
        self.logger.info("AnalystBot starting run")
        processed = 0
        succeeded = 0
        failed = 0

        db = self.get_db()
        try:
            cutoff = datetime.utcnow() - timedelta(days=30)
            posted_content = (db.query(Content)
                              .filter(
                                  Content.status == 'posted',
                                  Content.posted_at >= cutoff,
                                  Content.post_id != None
                              ).all())

            for item in posted_content:
                try:
                    handler = self.handlers.get(item.platform)
                    if not handler:
                        continue

                    metrics_data = await handler.get_metrics(item.post_id, item.platform)
                    if not metrics_data:
                        continue

                    reach = metrics_data.get('reach', 0) or 1
                    engagement = (
                        metrics_data.get('likes', 0) +
                        metrics_data.get('comments', 0) +
                        metrics_data.get('shares', 0) +
                        metrics_data.get('saves', 0)
                    )
                    engagement_rate = round((engagement / reach) * 100, 2)

                    existing = (db.query(Metrics)
                                .filter(
                                    Metrics.content_id == item.id,
                                    Metrics.platform == item.platform
                                ).first())

                    if existing:
                        existing.likes = metrics_data.get('likes', 0)
                        existing.comments = metrics_data.get('comments', 0)
                        existing.shares = metrics_data.get('shares', 0)
                        existing.saves = metrics_data.get('saves', 0)
                        existing.views = metrics_data.get('views', 0)
                        existing.reach = metrics_data.get('reach', 0)
                        existing.impressions = metrics_data.get('impressions', 0)
                        existing.clicks = metrics_data.get('clicks', 0)
                        existing.engagement_rate = engagement_rate
                        existing.recorded_at = datetime.utcnow()
                    else:
                        metric = Metrics(
                            id=str(uuid.uuid4()),
                            content_id=item.id,
                            platform=item.platform,
                            post_id=item.post_id,
                            likes=metrics_data.get('likes', 0),
                            comments=metrics_data.get('comments', 0),
                            shares=metrics_data.get('shares', 0),
                            saves=metrics_data.get('saves', 0),
                            views=metrics_data.get('views', 0),
                            reach=metrics_data.get('reach', 0),
                            impressions=metrics_data.get('impressions', 0),
                            clicks=metrics_data.get('clicks', 0),
                            engagement_rate=engagement_rate
                        )
                        db.add(metric)

                    db.commit()
                    processed += 1
                    succeeded += 1

                except Exception as e:
                    self.logger.warning(f"AnalystBot metrics failed for {item.id}: {e}")
                    processed += 1
                    failed += 1

            now = datetime.utcnow()
            if now.weekday() == 0 and 8 <= now.hour <= 10:
                await self._generate_weekly_digest(db)

        finally:
            db.close()

        return {'processed': processed, 'succeeded': succeeded, 'failed': failed}

    async def _generate_weekly_digest(self, db):
        """Generate an AI-powered weekly performance digest."""
        if not self.client:
            return

        cutoff = datetime.utcnow() - timedelta(days=7)
        metrics = (db.query(Metrics)
                   .filter(Metrics.recorded_at >= cutoff)
                   .all())

        if not metrics:
            return

        total_posts = len(set(m.content_id for m in metrics))
        total_likes = sum(m.likes for m in metrics)
        total_views = sum(m.views for m in metrics)
        total_reach = sum(m.reach for m in metrics)
        avg_engagement = round(sum(m.engagement_rate for m in metrics) / len(metrics), 2)

        by_platform = {}
        for m in metrics:
            if m.platform not in by_platform:
                by_platform[m.platform] = {'posts': 0, 'likes': 0, 'views': 0, 'engagement': []}
            by_platform[m.platform]['posts'] += 1
            by_platform[m.platform]['likes'] += m.likes
            by_platform[m.platform]['views'] += m.views
            by_platform[m.platform]['engagement'].append(m.engagement_rate)

        platform_summary = "\n".join([
            f"- {p.upper()}: {d['posts']} posts, {d['likes']} likes, {d['views']} views, "
            f"avg {round(sum(d['engagement'])/max(1,len(d['engagement'])), 2)}% engagement"
            for p, d in by_platform.items()
        ])

        prompt = f"""You are analyzing the weekly social media performance for The Automator content automation system.

LAST 7 DAYS SUMMARY:
- Total posts published: {total_posts}
- Total likes: {total_likes:,}
- Total views: {total_views:,}
- Total reach: {total_reach:,}
- Average engagement rate: {avg_engagement}%

BY PLATFORM:
{platform_summary}

Write a concise weekly digest (maximum 500 words) that:
1. Highlights what worked well this week
2. Identifies which platform is performing best and worst
3. Gives 3 specific, actionable recommendations to improve next week
4. Mentions any red flags (low engagement, declining views)
5. Ends with a performance score out of 10

Be direct and specific. No fluff."""

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )

        digest_text = response.content[0].text

        setting = db.query(SystemSetting).filter(SystemSetting.key == 'latest_digest').first()
        if setting:
            setting.value = digest_text
            setting.updated_at = datetime.utcnow()
        else:
            db.add(SystemSetting(key='latest_digest', value=digest_text))
        db.commit()

        self.logger.info("AnalystBot generated weekly digest")
