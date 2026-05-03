import asyncio
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

from database import SessionLocal
from models import Niche, Trend
from bots.base_bot import BaseBot
from utils.scraper import Scraper
from utils.trend_scorer import TrendScorer


class ScoutBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.scraper = Scraper()
        self.scorer = TrendScorer()

    async def run(self) -> dict:
        self.logger.info("ScoutBot starting run")
        processed = 0
        succeeded = 0
        failed = 0

        db = self.get_db()
        try:
            niches = db.query(Niche).filter(Niche.active == True).all()
            self.logger.info(f"ScoutBot found {len(niches)} active niches")

            for niche in niches:
                try:
                    await self._process_niche(niche)
                    processed += 1
                    succeeded += 1
                except Exception as e:
                    self.logger.error(f"ScoutBot failed for niche {niche.name}: {e}")
                    processed += 1
                    failed += 1
        finally:
            db.close()

        return {'processed': processed, 'succeeded': succeeded, 'failed': failed}

    async def _process_niche(self, niche: Niche):
        self.logger.info(f"Scouting trends for niche: {niche.name}")
        keywords = niche.keywords or []
        hashtags = [h.lstrip('#') for h in (niche.hashtags or [])]
        search_terms = keywords + hashtags

        all_trends = []

        tasks = [
            self._scrape_google_trends(search_terms),
            self._scrape_reddit(search_terms),
            self._scrape_twitter_trending(search_terms),
            self._scrape_tiktok_trending(search_terms),
            self._scrape_youtube_trending(search_terms),
            self._scrape_rss_feeds(niche),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                self.logger.warning(f"Scraping source failed: {result}")
            elif isinstance(result, list):
                all_trends.extend(result)

        all_trends = self._deduplicate(all_trends)

        scored_trends = []
        for trend_data in all_trends:
            score = self.scorer.score(trend_data, keywords, hashtags)
            trend_data['final_score'] = score['final']
            trend_data['velocity_score'] = score['velocity']
            trend_data['volume_score'] = score['volume']
            trend_data['relevance_score'] = score['relevance']
            scored_trends.append(trend_data)

        scored_trends.sort(key=lambda x: x['final_score'], reverse=True)
        top_trends = scored_trends[:20]

        db = self.get_db()
        try:
            cutoff = datetime.utcnow() - timedelta(hours=48)
            db.query(Trend).filter(
                Trend.niche_id == niche.id,
                Trend.used == False,
                Trend.scraped_at < cutoff
            ).delete()

            for td in top_trends:
                trend = Trend(
                    id=str(uuid.uuid4()),
                    niche_id=niche.id,
                    topic=td['topic'],
                    source=td.get('source', 'unknown'),
                    raw_score=td.get('raw_score', 0.0),
                    velocity_score=td['velocity_score'],
                    volume_score=td['volume_score'],
                    relevance_score=td['relevance_score'],
                    final_score=td['final_score'],
                    keywords=td.get('keywords', []),
                    hashtags=td.get('hashtags', []),
                    source_url=td.get('url', None),
                    used=False,
                    scraped_at=datetime.utcnow()
                )
                db.add(trend)
            db.commit()
            self.logger.info(f"Saved {len(top_trends)} trends for niche: {niche.name}")
        finally:
            db.close()

    async def _scrape_google_trends(self, search_terms: List[str]) -> List[Dict]:
        results = []
        try:
            for term in search_terms[:3]:
                url = f"https://trends.google.com/trends/explore?q={term}&date=now+1-d"
                data = await self.scraper.scrape_page(url)
                if data:
                    parsed = self.scraper.parse_google_trends(data, term)
                    results.extend(parsed)
        except Exception as e:
            self.logger.warning(f"Google Trends scraping failed: {e}")
        return results

    async def _scrape_reddit(self, search_terms: List[str]) -> List[Dict]:
        results = []
        try:
            from config import settings
            if settings.reddit_client_id:
                data = await self.scraper.scrape_reddit(search_terms)
                results.extend(data)
            else:
                for term in search_terms[:2]:
                    url = f"https://www.reddit.com/search.json?q={term}&sort=hot&limit=10"
                    data = await self.scraper.fetch_json(url)
                    if data and 'data' in data:
                        for post in data['data'].get('children', []):
                            pd = post.get('data', {})
                            results.append({
                                'topic': pd.get('title', ''),
                                'source': 'reddit',
                                'raw_score': min(pd.get('score', 0) / 1000, 10.0),
                                'url': f"https://reddit.com{pd.get('permalink', '')}",
                                'keywords': term.split(),
                                'hashtags': []
                            })
        except Exception as e:
            self.logger.warning(f"Reddit scraping failed: {e}")
        return results

    async def _scrape_twitter_trending(self, search_terms: List[str]) -> List[Dict]:
        results = []
        try:
            data = await self.scraper.scrape_page("https://nitter.net/explore/tabs/trending")
            if data:
                parsed = self.scraper.parse_nitter_trending(data, search_terms)
                results.extend(parsed)
        except Exception as e:
            self.logger.warning(f"Twitter trending scraping failed: {e}")
        return results

    async def _scrape_tiktok_trending(self, search_terms: List[str]) -> List[Dict]:
        results = []
        try:
            for term in search_terms[:2]:
                url = f"https://www.tiktok.com/search?q={term}"
                data = await self.scraper.scrape_page_playwright(url)
                if data:
                    parsed = self.scraper.parse_tiktok_trends(data, term)
                    results.extend(parsed)
        except Exception as e:
            self.logger.warning(f"TikTok trending scraping failed: {e}")
        return results

    async def _scrape_youtube_trending(self, search_terms: List[str]) -> List[Dict]:
        results = []
        try:
            from config import settings
            if settings.youtube_client_id:
                import googleapiclient.discovery
                youtube = googleapiclient.discovery.build('youtube', 'v3',
                    developerKey=settings.youtube_client_id)
                request = youtube.videos().list(
                    part='snippet,statistics',
                    chart='mostPopular',
                    maxResults=20,
                    regionCode='US'
                )
                response = request.execute()
                for item in response.get('items', []):
                    snippet = item.get('snippet', {})
                    stats = item.get('statistics', {})
                    topic = snippet.get('title', '')
                    topic_lower = topic.lower()
                    if any(term.lower() in topic_lower for term in search_terms):
                        results.append({
                            'topic': topic,
                            'source': 'youtube',
                            'raw_score': min(int(stats.get('viewCount', 0)) / 1000000, 10.0),
                            'url': f"https://youtube.com/watch?v={item['id']}",
                            'keywords': [t for t in search_terms if t.lower() in topic_lower],
                            'hashtags': []
                        })
        except Exception as e:
            self.logger.warning(f"YouTube trending failed: {e}")
        return results

    async def _scrape_rss_feeds(self, niche: Niche) -> List[Dict]:
        results = []
        keywords_str = '+'.join((niche.keywords or [])[:3])
        rss_feeds = [
            f"https://news.google.com/rss/search?q={keywords_str}",
            f"https://www.reddit.com/search.rss?q={'+'.join((niche.keywords or [])[:2])}&sort=hot",
        ]
        try:
            import feedparser
            for feed_url in rss_feeds:
                parsed = feedparser.parse(feed_url)
                for entry in parsed.entries[:10]:
                    results.append({
                        'topic': entry.get('title', ''),
                        'source': 'rss',
                        'raw_score': 5.0,
                        'url': entry.get('link', ''),
                        'keywords': niche.keywords or [],
                        'hashtags': []
                    })
        except Exception as e:
            self.logger.warning(f"RSS scraping failed: {e}")
        return results

    def _deduplicate(self, trends: List[Dict]) -> List[Dict]:
        """Remove duplicate topics using simple string similarity."""
        seen = []
        unique = []
        for trend in trends:
            topic = trend['topic'].lower().strip()
            if not topic or len(topic) < 5:
                continue
            is_dup = False
            for s in seen:
                words_a = set(topic.split())
                words_b = set(s.split())
                if len(words_a) > 0 and len(words_a & words_b) / len(words_a) > 0.6:
                    is_dup = True
                    break
            if not is_dup:
                seen.append(topic)
                unique.append(trend)
        return unique
