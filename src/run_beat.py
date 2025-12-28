"""
Celery Beat Entry Point

Khởi chạy Celery Beat scheduler để chạy periodic tasks

Usage:
    python -m src.run_beat
"""
from src.config import config
from src.infrastructure.CeleryConfig import CeleryConfig
from src.worker.factories.CeleryAppFactory import CeleryAppFactory
from src.infrastructure.schedules import get_beat_schedule


def main():
    """Main function để run beat scheduler"""

    print("\n" + "="*60)
    print("⏰ STARTING CELERY BEAT SCHEDULER")
    print("="*60 + "\n")

    # 1. Load schedule config
    beat_schedule = get_beat_schedule()

    # 2. Load config từ environment với beat_schedule
    celery_config = CeleryConfig.from_config(
        config=config,
        app_name='celery_beat',
        beat_schedule=beat_schedule
    )

    # 3. Tạo Celery app
    celery_app = CeleryAppFactory.create(celery_config)
    
    # 4. Hiển thị cấu hình
    redis_host = config.get_config('REDIS_HOST', 'localhost')
    redis_host = config.get_config('REDIS_HOST', 'localhost')
    redis_port = config.get_int('REDIS_PORT', 6379)

    print("\n" + "="*60)
    print("⚙️   BEAT SCHEDULER CONFIGURATION")
    print("="*60)
    print(f"  Redis: {redis_host}:{redis_port}")
    print(f"  Scheduled Tasks: {len(beat_schedule)}")
    print()
    for task_name, task_config in beat_schedule.items():
        print(f"  📅 {task_name}")
        print(f"      Task: {task_config['task']}")
        print(f"      Schedule: {task_config['schedule']}")
        print()
    print("="*60 + "\n")

    print("⏳ Beat scheduler running... Press Ctrl+C to stop\n")

    # 7. Khởi động beat scheduler
    celery_app.Beat(loglevel='INFO').run()


if __name__ == '__main__':
    main()