from abc import ABC, abstractmethod
from database import SessionLocal
from utils.logger import setup_logger


class BaseBot(ABC):
    def __init__(self):
        self.logger = setup_logger(self.__class__.__name__)

    def get_db(self):
        return SessionLocal()

    @abstractmethod
    async def run(self) -> dict:
        """Execute the bot's main work. Returns dict with keys:
        processed (int), succeeded (int), failed (int)
        """
        pass
