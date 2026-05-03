from typing import List, Dict


class TrendScorer:
    """
    Scores a trend on three dimensions:
    - Velocity: how fast the topic is rising (raw_score is proxy)
    - Volume: how many sources mention it (normalized count)
    - Relevance: how closely it matches the niche keywords/hashtags

    Final score = 0.4 * velocity + 0.3 * volume + 0.3 * relevance
    """

    def score(self, trend_data: Dict, keywords: List[str], hashtags: List[str]) -> Dict:
        velocity = self._calc_velocity(trend_data)
        volume = self._calc_volume(trend_data)
        relevance = self._calc_relevance(trend_data, keywords, hashtags)

        final = round(0.4 * velocity + 0.3 * volume + 0.3 * relevance, 3)

        return {
            'velocity': round(velocity, 3),
            'volume': round(volume, 3),
            'relevance': round(relevance, 3),
            'final': final
        }

    def _calc_velocity(self, trend: Dict) -> float:
        """Use raw_score as velocity proxy (0-10 scale)."""
        raw = trend.get('raw_score', 0)
        return min(float(raw), 10.0)

    def _calc_volume(self, trend: Dict) -> float:
        """Score based on source credibility and how many keywords matched."""
        source_weights = {
            'google_trends': 9.0,
            'tiktok': 8.5,
            'twitter': 8.0,
            'youtube': 7.5,
            'reddit': 7.0,
            'rss': 6.0,
            'unknown': 5.0
        }
        base = source_weights.get(trend.get('source', 'unknown'), 5.0)
        keyword_bonus = min(len(trend.get('keywords', [])) * 0.5, 2.0)
        return min(base + keyword_bonus, 10.0)

    def _calc_relevance(self, trend: Dict, keywords: List[str], hashtags: List[str]) -> float:
        """Score based on keyword overlap between trend topic and niche keywords."""
        topic = trend.get('topic', '').lower()
        if not topic:
            return 0.0

        all_terms = [k.lower() for k in keywords] + [h.lower().lstrip('#') for h in hashtags]
        if not all_terms:
            return 5.0

        matches = sum(1 for term in all_terms if term in topic)
        score = (matches / len(all_terms)) * 10.0

        if any(k.lower() in topic for k in keywords):
            score = min(score + 2.0, 10.0)

        return score
