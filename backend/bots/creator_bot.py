import uuid
import asyncio
from datetime import datetime
from pathlib import Path

from config import settings
from database import SessionLocal
from models import Content
from bots.base_bot import BaseBot
from utils.media_handler import MediaHandler


class CreatorBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.media_handler = MediaHandler()

    async def run(self) -> dict:
        self.logger.info("CreatorBot starting run")
        processed = 0
        succeeded = 0
        failed = 0

        db = self.get_db()
        try:
            items = (db.query(Content)
                     .filter(Content.status == 'pending')
                     .order_by(Content.created_at.asc())
                     .limit(20).all())

            self.logger.info(f"CreatorBot found {len(items)} pending content items")

            for item in items:
                try:
                    item.status = 'media_pending'
                    db.commit()

                    media_result = await self.media_handler.get_media_for_content(item)

                    item.media_type = media_result['type']
                    item.media_paths = media_result['paths']
                    item.thumbnail_path = media_result['thumbnail']
                    item.media_source = media_result['source']
                    item.status = 'media_ready'
                    db.commit()

                    processed += 1
                    succeeded += 1
                    self.logger.info(f"CreatorBot processed content {item.id} from {media_result['source']}")

                except Exception as e:
                    self.logger.error(f"CreatorBot failed for content {item.id}: {e}")
                    item.status = 'pending'
                    item.error_message = str(e)
                    db.commit()
                    processed += 1
                    failed += 1
        finally:
            db.close()

        return {'processed': processed, 'succeeded': succeeded, 'failed': failed}
