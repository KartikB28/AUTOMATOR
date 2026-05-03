import asyncio
import httpx
from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup
from utils.logger import setup_logger

logger = setup_logger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
]


class Scraper:
    def __init__(self):
        self._ua_index = 0

    def _next_ua(self) -> str:
        ua = USER_AGENTS[self._ua_index % len(USER_AGENTS)]
        self._ua_index += 1
        return ua

    async def fetch_json(self, url: str) -> Optional[dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    url,
                    headers={"User-Agent": self._next_ua()},
                    timeout=15.0,
                    follow_redirects=True
                )
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.warning(f"fetch_json failed for {url}: {e}")
            return None

    async def scrape_page(self, url: str) -> Optional[str]:
        """Fetch a page with httpx (fast, for simple HTML)."""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    url,
                    headers={
                        "User-Agent": self._next_ua(),
                        "Accept": "text/html,application/xhtml+xml",
                        "Accept-Language": "en-US,en;q=0.9",
                    },
                    timeout=15.0,
                    follow_redirects=True
                )
                resp.raise_for_status()
                return resp.text
        except Exception as e:
            logger.warning(f"scrape_page failed for {url}: {e}")
            return None

    async def scrape_page_playwright(self, url: str, wait_selector: str = None) -> Optional[str]:
        """Fetch a JS-rendered page using Playwright headless browser."""
        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self._next_ua(),
                    viewport={"width": 1280, "height": 800}
                )
                page = await context.new_page()
                await page.goto(url, wait_until="networkidle", timeout=20000)
                if wait_selector:
                    await page.wait_for_selector(wait_selector, timeout=10000)
                content = await page.content()
                await browser.close()
                return content
        except Exception as e:
            logger.warning(f"Playwright scrape failed for {url}: {e}")
            return None

    def parse_google_trends(self, html: str, query: str) -> List[Dict]:
        """Parse trending queries from a Google Trends page."""
        results = []
        try:
            soup = BeautifulSoup(html, 'lxml')
            for elem in soup.select('.fe-atoms-generic-content-value, [data-ved] .title'):
                text = elem.get_text(strip=True)
                if text and len(text) > 5:
                    results.append({
                        'topic': text,
                        'source': 'google_trends',
                        'raw_score': 10.0,
                        'keywords': [query],
                        'hashtags': [],
                        'url': f"https://trends.google.com/trends/explore?q={text}"
                    })
        except Exception as e:
            logger.warning(f"parse_google_trends failed: {e}")
        return results[:10]

    def parse_nitter_trending(self, html: str, search_terms: List[str]) -> List[Dict]:
        """Parse trending topics from Nitter."""
        results = []
        try:
            soup = BeautifulSoup(html, 'lxml')
            for trend in soup.select('.trend-topic, .trending-hashtag'):
                text = trend.get_text(strip=True)
                if text:
                    results.append({
                        'topic': text.lstrip('#'),
                        'source': 'twitter',
                        'raw_score': 8.0,
                        'keywords': [t for t in search_terms if t.lower() in text.lower()],
                        'hashtags': [text.lstrip('#')] if text.startswith('#') else [],
                        'url': f"https://twitter.com/search?q={text}"
                    })
        except Exception as e:
            logger.warning(f"parse_nitter_trending failed: {e}")
        return results

    def parse_tiktok_trends(self, html: str, query: str) -> List[Dict]:
        """Parse trending content from TikTok search results."""
        results = []
        try:
            soup = BeautifulSoup(html, 'lxml')
            for item in soup.select('[data-e2e="search-common-video"] span, .tiktok-1ejylhp'):
                text = item.get_text(strip=True)
                if text and len(text) > 10:
                    results.append({
                        'topic': text[:200],
                        'source': 'tiktok',
                        'raw_score': 9.0,
                        'keywords': [query],
                        'hashtags': [],
                        'url': f"https://www.tiktok.com/search?q={query}"
                    })
        except Exception as e:
            logger.warning(f"parse_tiktok_trends failed: {e}")
        return results[:5]

    async def scrape_reddit(self, search_terms: List[str]) -> List[Dict]:
        """Scrape Reddit using the JSON API."""
        results = []
        for term in search_terms[:3]:
            data = await self.fetch_json(
                f"https://www.reddit.com/search.json?q={term}&sort=hot&limit=10&t=day"
            )
            if data:
                for post in data.get('data', {}).get('children', []):
                    pd = post.get('data', {})
                    score = pd.get('score', 0)
                    if score > 100:
                        results.append({
                            'topic': pd.get('title', ''),
                            'source': 'reddit',
                            'raw_score': min(score / 1000, 10.0),
                            'keywords': [term],
                            'hashtags': [],
                            'url': f"https://reddit.com{pd.get('permalink', '')}"
                        })
        return results
