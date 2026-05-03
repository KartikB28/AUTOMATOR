import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config import settings


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    log_dir = Path(settings.app_data_path) / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    fh = RotatingFileHandler(
        str(log_dir / 'automator.log'),
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
