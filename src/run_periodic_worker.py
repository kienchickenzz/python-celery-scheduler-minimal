"""
Worker Entry Point

Khởi chạy Celery worker để xử lý periodic tasks

Usage:
    python -m src.run_periodic_worker
"""
from os import environ
from pathlib import Path

from dotenv import load_dotenv

from src.config import Config
from src.logger.LoggerConfig import LoggerConfig
from src.logger.LoggerFactory import LoggerFactory

from src.infrastructure.CeleryConfig import CeleryConfig
from src.worker.CeleryAppFactory import CeleryAppFactory
from src.worker.PeriodicTaskRegistry import PeriodicTaskRegistry

# Import periodic tasks
from src.worker.periodic_task.CleanupTask import CleanupTask
from src.worker.periodic_task.DailyReportTask import DailyReportTask
from src.worker.periodic_task.SyncDataTask import SyncDataTask


def main():
    # 0. Load env và config
    load_dotenv('.env')
    config = Config(environ)

    # 0.1 Khởi tạo logger
    logger_config = LoggerConfig(project_root=Path(__file__).parent.parent)
    logger = LoggerFactory(logger_config).get_instance()

    logger.info("=" * 60)
    logger.info("STARTING PERIODIC TASKS WORKER")
    logger.info("=" * 60)

    # 1. Tạo Celery config
    celery_config = CeleryConfig.from_config(
        config=config,
        app_name='periodic_worker',
        worker_concurrency=4
    )

    # 2. Tạo Celery app
    celery_app = CeleryAppFactory.create(celery_config)

    # 3. Tạo periodic tasks
    cleanup_task = CleanupTask()
    daily_report_task = DailyReportTask()
    sync_data_task = SyncDataTask()

    # 4. Đăng ký periodic tasks để worker biết cách xử lý
    periodic_tasks = {
        'cleanup': cleanup_task,
        'daily_report': daily_report_task,
        'sync_data': sync_data_task,
    }

    registry = PeriodicTaskRegistry(
        celery_app=celery_app,
        periodic_tasks=periodic_tasks
    )
    registry.register_all()

    # 5. Hiển thị config
    redis_host = config.get_config('REDIS_HOST', 'localhost')
    redis_port = config.get_int('REDIS_PORT', 6379)

    logger.info("=" * 60)
    logger.info("WORKER CONFIGURATION")
    logger.info("=" * 60)
    logger.info(f"Redis: {redis_host}:{redis_port}")
    logger.info(f"Registered Tasks: {len(periodic_tasks)}")
    for name, task in periodic_tasks.items():
        logger.debug(f"  - {task.get_task_name()}")
    logger.info("=" * 60)

    logger.info("Worker is starting...")

    # 6. Khởi động worker
    celery_app.worker_main(argv=[
        'worker',
        '--hostname=periodic_worker@%h',
        '--loglevel=INFO',
        '--concurrency=4',
        '--pool=prefork',
    ])


if __name__ == '__main__':
    main()