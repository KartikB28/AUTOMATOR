import os
import uuid
import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
import io

from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MediaHandler:
    def __init__(self):
        self.media_base = Path(settings.media_path)

    def _get_output_dir(self, niche_id: str) -> Path:
        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        out_dir = self.media_base / niche_id / date_str
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / 'images').mkdir(exist_ok=True)
        (out_dir / 'thumbnails').mkdir(exist_ok=True)
        (out_dir / 'videos').mkdir(exist_ok=True)
        return out_dir

    async def get_media_for_content(self, content) -> dict:
        """Try each media source in order until one succeeds."""
        niche_id = content.niche_id
        detailed_prompt = (
            f"Professional, high-quality image for social media about: {content.topic}. "
            f"Modern aesthetic, vibrant, eye-catching. No text in the image."
        )

        image_path = None
        source = 'none'

        if settings.openai_api_key:
            image_path = await self._generate_dalle3(detailed_prompt, niche_id)
            if image_path:
                source = 'dalle3'

        if not image_path and settings.stability_api_key:
            image_path = await self._generate_stability(detailed_prompt, niche_id)
            if image_path:
                source = 'stability'

        if not image_path and settings.pexels_api_key:
            image_path = await self._search_pexels(content.topic, niche_id)
            if image_path:
                source = 'pexels'

        if not image_path and settings.unsplash_access_key:
            image_path = await self._search_unsplash(content.topic, niche_id)
            if image_path:
                source = 'unsplash'

        if not image_path:
            image_path = self._generate_placeholder(content.topic, niche_id)
            source = 'generated'

        thumbnail_path = self._create_thumbnail(image_path, content.hook or content.topic, niche_id)

        return {
            'type': 'image',
            'paths': [str(image_path)],
            'thumbnail': str(thumbnail_path),
            'source': source
        }

    async def _generate_dalle3(self, prompt: str, niche_id: str) -> Optional[Path]:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            return await self._download_image(image_url, niche_id, 'dalle3')
        except Exception as e:
            logger.warning(f"DALL-E 3 generation failed: {e}")
            return None

    async def _generate_stability(self, prompt: str, niche_id: str) -> Optional[Path]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                    headers={
                        "Authorization": f"Bearer {settings.stability_api_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    json={
                        "text_prompts": [{"text": prompt, "weight": 1.0}],
                        "cfg_scale": 7,
                        "height": 1024,
                        "width": 1024,
                        "steps": 30,
                        "samples": 1
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                if data.get('artifacts'):
                    import base64
                    img_bytes = base64.b64decode(data['artifacts'][0]['base64'])
                    out_dir = self._get_output_dir(niche_id)
                    file_path = out_dir / 'images' / f"stability_{uuid.uuid4().hex[:8]}.png"
                    with open(file_path, 'wb') as f:
                        f.write(img_bytes)
                    return file_path
        except Exception as e:
            logger.warning(f"Stability AI generation failed: {e}")
            return None

    async def _search_pexels(self, query: str, niche_id: str) -> Optional[Path]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.pexels.com/v1/search",
                    headers={"Authorization": settings.pexels_api_key},
                    params={"query": query, "per_page": 5, "orientation": "square"},
                    timeout=15.0
                )
                response.raise_for_status()
                data = response.json()
                photos = data.get('photos', [])
                if photos:
                    photo_url = photos[0]['src']['large']
                    return await self._download_image(photo_url, niche_id, 'pexels')
        except Exception as e:
            logger.warning(f"Pexels search failed: {e}")
            return None

    async def _search_unsplash(self, query: str, niche_id: str) -> Optional[Path]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.unsplash.com/search/photos",
                    headers={"Authorization": f"Client-ID {settings.unsplash_access_key}"},
                    params={"query": query, "per_page": 5, "orientation": "squarish"},
                    timeout=15.0
                )
                response.raise_for_status()
                data = response.json()
                results = data.get('results', [])
                if results:
                    photo_url = results[0]['urls']['regular']
                    return await self._download_image(photo_url, niche_id, 'unsplash')
        except Exception as e:
            logger.warning(f"Unsplash search failed: {e}")
            return None

    async def _download_image(self, url: str, niche_id: str, source: str) -> Optional[Path]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0, follow_redirects=True)
                response.raise_for_status()
                out_dir = self._get_output_dir(niche_id)
                ext = 'jpg' if 'jpeg' in response.headers.get('content-type', '') else 'png'
                file_path = out_dir / 'images' / f"{source}_{uuid.uuid4().hex[:8]}.{ext}"
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return file_path
        except Exception as e:
            logger.warning(f"Image download failed from {url}: {e}")
            return None

    def _generate_placeholder(self, topic: str, niche_id: str) -> Path:
        """Generate a simple gradient image with topic text as fallback."""
        img = Image.new('RGB', (1024, 1024), color=(20, 20, 30))
        draw = ImageDraw.Draw(img)
        for i in range(1024):
            color = (int(20 + i * 0.04), int(20 + i * 0.02), int(30 + i * 0.06))
            draw.line([(0, i), (1024, i)], fill=color)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        except Exception:
            font = ImageFont.load_default()
        lines = self._wrap_text(topic, max_chars=20)
        y = 1024 // 2 - len(lines) * 30
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            draw.text(((1024 - w) // 2, y), line, fill=(255, 255, 255), font=font)
            y += 60

        out_dir = self._get_output_dir(niche_id)
        file_path = out_dir / 'images' / f"placeholder_{uuid.uuid4().hex[:8]}.png"
        img.save(file_path, 'PNG')
        return file_path

    def _create_thumbnail(self, image_path: Path, hook_text: str, niche_id: str) -> Path:
        """Overlay hook text on image to create a thumbnail."""
        try:
            img = Image.open(image_path).convert('RGB')
            img = img.resize((1080, 1080), Image.LANCZOS)

            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle([(0, 750), (1080, 1080)], fill=(0, 0, 0, 160))
            img = img.convert('RGBA')
            img = Image.alpha_composite(img, overlay)
            img = img.convert('RGB')
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            except Exception:
                font = ImageFont.load_default()

            hook_short = hook_text[:80] + '...' if len(hook_text) > 80 else hook_text
            lines = self._wrap_text(hook_short, max_chars=28)
            y = 780
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                w = bbox[2] - bbox[0]
                x = (1080 - w) // 2
                draw.text((x + 2, y + 2), line, fill=(0, 0, 0), font=font)
                draw.text((x, y), line, fill=(255, 255, 255), font=font)
                y += 50

            out_dir = self._get_output_dir(niche_id)
            thumb_path = out_dir / 'thumbnails' / f"thumb_{uuid.uuid4().hex[:8]}.jpg"
            img.save(str(thumb_path), 'JPEG', quality=85)
            return thumb_path
        except Exception as e:
            logger.warning(f"Thumbnail creation failed: {e}")
            return image_path

    def _wrap_text(self, text: str, max_chars: int) -> list:
        words = text.split()
        lines = []
        current = ''
        for word in words:
            if len(current) + len(word) + 1 <= max_chars:
                current += (' ' if current else '') + word
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines[:4]
