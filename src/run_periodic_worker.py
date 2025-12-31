"""
Worker Entry Point

Khởi chạy Celery worker để xử lý periodic tasks

Usage:
    python -m src.run_periodic_worker
"""
from src.config import config
from src.infrastructure.CeleryConfig import CeleryConfig
from src.worker.factories.CeleryAppFactory import CeleryAppFactory
from src.worker.registry.PeriodicTaskRegistry import PeriodicTaskRegistry

# Import periodic tasks
from src.worker.periodic.CleanupTask import CleanupTask
from src.worker.periodic.DailyReportTask import DailyReportTask
from src.worker.periodic.SyncDataTask import SyncDataTask


def main():
    print("\n" + "="*60)
    print("🔧 STARTING PERIODIC TASKS WORKER")
    print("="*60 + "\n")

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

    print("\n" + "="*60)
    print("⚙️   WORKER CONFIGURATION")
    print("="*60)
    print(f"  Redis: {redis_host}:{redis_port}")
    print(f"  Registered Tasks: {len(periodic_tasks)}")
    for name, task in periodic_tasks.items():
        print(f"    - {task.get_task_name()}")
    print("="*60 + "\n")

    print("⏳ Worker is starting...\n")

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