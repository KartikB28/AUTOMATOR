import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from database import SessionLocal
from models import BotRun, SystemSetting
from utils.logger import setup_logger

logger = setup_logger(__name__)

BOT_DEFAULTS = {
    'scout':     {'interval_hours': 2,  'enabled': True},
    'builder':   {'interval_hours': 1,  'enabled': True},
    'creator':   {'interval_hours': 1,  'enabled': True},
    'publisher': {'interval_minutes': 15, 'enabled': True},
    'analyst':   {'interval_hours': 6,  'enabled': True},
}


class Orchestrator:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone='UTC')
        self.bot_states = {
            name: {'status': 'idle', 'last_run': None, 'next_run': None, 'enabled': True}
            for name in BOT_DEFAULTS
        }
        self._import_bots()

    def _import_bots(self):
        from bots.scout_bot import ScoutBot
        from bots.builder_bot import BuilderBot
        from bots.creator_bot import CreatorBot
        from bots.publisher_bot import PublisherBot
        from bots.analyst_bot import AnalystBot

        self.bots = {
            'scout': ScoutBot(),
            'builder': BuilderBot(),
            'creator': CreatorBot(),
            'publisher': PublisherBot(),
            'analyst': AnalystBot(),
        }

    async def start(self):
        self.scheduler.add_job(
            self._run_bot, 'interval', hours=2,
            args=['scout'], id='scout', replace_existing=True,
            next_run_time=datetime.utcnow()
        )
        self.scheduler.add_job(
            self._run_bot, 'interval', hours=1,
            args=['builder'], id='builder', replace_existing=True
        )
        self.scheduler.add_job(
            self._run_bot, 'interval', hours=1, minutes=15,
            args=['creator'], id='creator', replace_existing=True
        )
        self.scheduler.add_job(
            self._run_bot, 'interval', minutes=15,
            args=['publisher'], id='publisher', replace_existing=True
        )
        self.scheduler.add_job(
            self._run_bot, 'interval', hours=6,
            args=['analyst'], id='analyst', replace_existing=True
        )
        self.scheduler.start()
        logger.info("Orchestrator scheduler started with all 5 bot jobs")

    async def stop(self):
        self.scheduler.shutdown(wait=False)

    async def _run_bot(self, bot_name: str):
        if not self.bot_states[bot_name]['enabled']:
            logger.info(f"Bot {bot_name} is disabled, skipping run")
            return

        if self.bot_states[bot_name]['status'] == 'running':
            logger.warning(f"Bot {bot_name} is already running, skipping")
            return

        self.bot_states[bot_name]['status'] = 'running'
        self.bot_states[bot_name]['last_run'] = datetime.utcnow().isoformat()

        db = SessionLocal()
        run = BotRun(
            bot_name=bot_name,
            status='running',
            started_at=datetime.utcnow()
        )
        db.add(run)
        db.commit()
        run_id = run.id
        db.close()

        try:
            bot = self.bots[bot_name]
            result = await bot.run()

            db = SessionLocal()
            run = db.query(BotRun).filter(BotRun.id == run_id).first()
            if run:
                run.status = 'completed'
                run.completed_at = datetime.utcnow()
                run.items_processed = result.get('processed', 0)
                run.items_succeeded = result.get('succeeded', 0)
                run.items_failed = result.get('failed', 0)
                db.commit()
            db.close()

            self.bot_states[bot_name]['status'] = 'idle'
            logger.info(f"Bot {bot_name} completed: {result}")

        except Exception as e:
            logger.error(f"Bot {bot_name} failed: {e}", exc_info=True)
            db = SessionLocal()
            run = db.query(BotRun).filter(BotRun.id == run_id).first()
            if run:
                run.status = 'failed'
                run.completed_at = datetime.utcnow()
                run.error_message = str(e)
                db.commit()
            db.close()
            self.bot_states[bot_name]['status'] = 'error'

    async def trigger_bot(self, bot_name: str) -> dict:
        if bot_name not in self.bots:
            raise ValueError(f"Unknown bot: {bot_name}")
        asyncio.create_task(self._run_bot(bot_name))
        return {'triggered': True, 'bot': bot_name}

    def pause_bot(self, bot_name: str):
        self.bot_states[bot_name]['enabled'] = False
        try:
            self.scheduler.pause_job(bot_name)
        except Exception:
            pass

    def resume_bot(self, bot_name: str):
        self.bot_states[bot_name]['enabled'] = True
        try:
            self.scheduler.resume_job(bot_name)
        except Exception:
            pass

    def pause_all(self):
        for name in self.bots:
            self.pause_bot(name)

    def resume_all(self):
        for name in self.bots:
            self.resume_bot(name)

    def get_status(self) -> dict:
        status = {}
        for name, state in self.bot_states.items():
            job = self.scheduler.get_job(name)
            status[name] = {
                **state,
                'next_run': job.next_run_time.isoformat() if job and job.next_run_time else None
            }
        return status
