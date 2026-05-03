import uuid
import asyncio
import json
from datetime import datetime
from typing import List, Optional

import anthropic

from config import settings
from database import SessionLocal
from models import Niche, Trend, Content
from bots.base_bot import BaseBot

PLATFORM_CONTENT_SPECS = {
    'instagram': {
        'caption_max': 2200,
        'hashtag_count': 30,
        'content_types': ['post', 'reel', 'story', 'carousel'],
        'default_type': 'reel',
        'format': 'Visual-first. Hook in the first line. Use line breaks. End with CTA.',
    },
    'tiktok': {
        'caption_max': 2200,
        'hashtag_count': 10,
        'content_types': ['short'],
        'default_type': 'short',
        'format': 'Script for a 30-60 second video. Hook in first 3 seconds. Fast-paced. Conversational.',
    },
    'youtube': {
        'caption_max': 5000,
        'hashtag_count': 15,
        'content_types': ['short', 'video'],
        'default_type': 'short',
        'format': 'YouTube Shorts script: 60 seconds max. Hook -> insight -> CTA to subscribe.',
    },
    'twitter': {
        'caption_max': 280,
        'hashtag_count': 3,
        'content_types': ['post'],
        'default_type': 'post',
        'format': 'Punchy tweet under 280 chars. Provoke thought or share an insight. Max 2 hashtags.',
    },
    'linkedin': {
        'caption_max': 3000,
        'hashtag_count': 5,
        'content_types': ['post'],
        'default_type': 'post',
        'format': 'Professional tone. Value-forward. Start with a hook. Use spacing. End with question.',
    },
    'facebook': {
        'caption_max': 63206,
        'hashtag_count': 5,
        'content_types': ['post'],
        'default_type': 'post',
        'format': 'Conversational and engaging. Can be longer-form. Ask a question. Encourage sharing.',
    }
}


class BuilderBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key) if settings.anthropic_api_key else None

    async def run(self) -> dict:
        if not self.client:
            self.logger.error("BuilderBot: No Anthropic API key configured")
            return {'processed': 0, 'succeeded': 0, 'failed': 0}

        self.logger.info("BuilderBot starting run")
        processed = 0
        succeeded = 0
        failed = 0

        db = self.get_db()
        try:
            niches = db.query(Niche).filter(Niche.active == True).all()

            for niche in niches:
                trends = (db.query(Trend)
                          .filter(Trend.niche_id == niche.id, Trend.used == False)
                          .order_by(Trend.final_score.desc())
                          .limit(5).all())

                for trend in trends:
                    platforms = niche.target_platforms or []
                    for platform in platforms:
                        if platform not in PLATFORM_CONTENT_SPECS:
                            continue
                        try:
                            content_data = await self._generate_content(niche, trend, platform)
                            content = Content(
                                id=str(uuid.uuid4()),
                                niche_id=niche.id,
                                trend_id=trend.id,
                                topic=trend.topic,
                                trend_score=trend.final_score,
                                platform=platform,
                                content_type=PLATFORM_CONTENT_SPECS[platform]['default_type'],
                                hook=content_data.get('hook'),
                                caption=content_data.get('caption'),
                                script=content_data.get('script'),
                                hashtags=content_data.get('hashtags', []),
                                cta=content_data.get('cta'),
                                status='pending',
                                created_at=datetime.utcnow()
                            )
                            db.add(content)
                            processed += 1
                            succeeded += 1
                        except Exception as e:
                            self.logger.error(f"BuilderBot failed for {trend.topic}/{platform}: {e}")
                            processed += 1
                            failed += 1

                    trend.used = True

                db.commit()
        finally:
            db.close()

        return {'processed': processed, 'succeeded': succeeded, 'failed': failed}

    async def _generate_content(self, niche: Niche, trend: Trend, platform: str) -> dict:
        spec = PLATFORM_CONTENT_SPECS[platform]
        brand_voice = niche.brand_voice or f"An authoritative but approachable voice in the {niche.name} niche."
        tone = niche.content_tone or 'engaging'
        audience = niche.target_audience or f"People interested in {niche.name}"

        prompt = f"""You are a world-class social media content creator specializing in the {niche.name} niche.

NICHE: {niche.name}
DESCRIPTION: {niche.description or niche.name}
TOPIC TO CREATE CONTENT ABOUT: {trend.topic}
TREND KEYWORDS: {', '.join(trend.keywords or [])}
TARGET PLATFORM: {platform.upper()}
TARGET AUDIENCE: {audience}
CONTENT TONE: {tone}
BRAND VOICE: {brand_voice}
PLATFORM CONTENT REQUIREMENTS: {spec['format']}
CAPTION CHARACTER LIMIT: {spec['caption_max']}
HASHTAG COUNT: Exactly {spec['hashtag_count']} hashtags

Generate a complete content package for this topic. Your response must be a valid JSON object with these exact keys:

{{
  "hook": "The first 1-2 sentences that grab attention immediately. For video, this is what they hear in the first 3 seconds.",
  "caption": "The complete post caption/description optimized for {platform}. Stay under {spec['caption_max']} characters. Include the hook at the start.",
  "script": "For TikTok/YouTube/Instagram Reels: a full word-for-word video script with [PAUSE], [CUT], [SHOW X] stage directions. For static platforms (twitter, linkedin, facebook), set this to null.",
  "hashtags": ["array", "of", "{spec['hashtag_count']}", "hashtags", "without", "the", "hash", "symbol"],
  "cta": "The specific call-to-action at the end (follow, share, comment, link in bio, etc.)",
  "image_prompt": "A detailed DALL-E 3 image generation prompt describing the perfect visual for this content. Be specific about style, composition, colors, and mood. Do NOT include text in the image."
}}

RULES:
- The hook must be irresistible and create immediate curiosity or emotion
- Captions must feel human-written, not AI-generated
- Hashtags must be a mix of: 5 high-volume (#fitness), 10 medium (#homeworkout), and niche-specific (#30minuteabs)
- The image_prompt must be highly detailed and produce a professional, shareable image
- For Twitter: caption is the tweet itself, max 280 chars, no script needed
- Do not add any text outside the JSON object"""

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text.strip()
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            text = text[start:end]
        result = json.loads(text)
        result['_image_prompt'] = result.get('image_prompt', f"Professional photo related to {trend.topic}")
        return result
