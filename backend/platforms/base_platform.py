from abc import ABC, abstractmethod
from typing import Optional
from utils.logger import setup_logger


class BasePlatform(ABC):
    def __init__(self):
        self.logger = setup_logger(self.__class__.__name__)

    @abstractmethod
    async def post(self, content) -> dict:
        """Post content to the platform. Returns dict with post_id and url."""
        pass

    @abstractmethod
    async def get_metrics(self, post_id: str, platform: str) -> Optional[dict]:
        """Fetch metrics for a post by its platform-assigned ID."""
        pass
