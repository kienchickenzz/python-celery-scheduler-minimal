"""
Celery Beat Entry Point

Khởi chạy Celery Beat scheduler để lập lịch periodic tasks

Usage:
    python -m src.run_beat
"""
from os import environ
from pathlib import Path

from dotenv import load_dotenv

from src.config import Config
from src.logger.LoggerConfig import LoggerConfig
from src.logger.LoggerFactory import LoggerFactory

from src.infrastructure.CeleryConfig import CeleryConfig
from src.worker.CeleryAppFactory import CeleryAppFactory
from src.infrastructure.schedules import get_beat_schedule


def main():
    """Main function để run beat scheduler"""

    # 0. Load env và config
    load_dotenv('.env')
    config = Config(environ)

    # 0.1 Khởi tạo logger
    logger_config = LoggerConfig(project_root=Path(__file__).parent.parent)
    logger = LoggerFactory(logger_config).get_instance()

    logger.info("=" * 60)
    logger.info("STARTING CELERY BEAT SCHEDULER")
    logger.info("=" * 60)

    # 1. Load schedule config
    beat_schedule = get_beat_schedule()

    # 2. Load config từ với schedule
    celery_config = CeleryConfig.from_config(
        config=config,
        app_name='celery_beat',
        beat_schedule=beat_schedule
    )

    # 3. Tạo Celery app
    celery_app = CeleryAppFactory.create(celery_config)

    # 4. Hiển thị cấu hình
    redis_host = config.get_config('REDIS_HOST', 'localhost')
    redis_port = config.get_int('REDIS_PORT', 6379)

    logger.info("=" * 60)
    logger.info("BEAT SCHEDULER CONFIGURATION")
    logger.info("=" * 60)
    logger.info(f"Redis: {redis_host}:{redis_port}")
    logger.info(f"Scheduled Tasks: {len(beat_schedule)}")
    for task_name, task_config in beat_schedule.items():
        logger.debug(f"  {task_name}")
        logger.debug(f"    Task: {task_config['task']}")
        logger.debug(f"    Schedule: {task_config['schedule']}")
    logger.info("=" * 60)

    logger.info("Beat scheduler running... Press Ctrl+C to stop")

    # 5. Khởi động beat scheduler
    celery_app.Beat(loglevel='INFO').run()


if __name__ == '__main__':
    main()