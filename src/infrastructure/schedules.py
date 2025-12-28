"""
Định nghĩa lịch chạy cho periodic tasks

Sử dụng Celery schedule:
- crontab: Giống cron syntax
- schedule: Interval theo giây
"""
from celery.schedules import crontab, schedule

from src.worker.periodic.CleanupTask import CleanupTask
from src.worker.periodic.DailyReportTask import DailyReportTask
from src.worker.periodic.SyncDataTask import SyncDataTask

# Định nghĩa các schedule
PERIODIC_SCHEDULES = {

    # Chạy mỗi 10 giây
    'cleanup-old-data-every-10-seconds': {
        'task': CleanupTask.get_task_name(),
        'schedule': schedule(run_every=10),  # 10 giây
        'options': {
            'expires': 10,  # Task expire sau 10 giây nếu không được chạy
        }
    },

    # Chạy mỗi 1 phút
    'cleanup-old-data-every-1-minutes': {
        'task': CleanupTask.get_task_name(),
        'schedule': schedule(run_every=60),  # 60 giây = 1 phút
        'options': {
            'expires': 60,  # Task expire sau 60 giây nếu không được chạy
        }
    },

    # Chạy vào 2h sáng mỗi ngày
    'daily-report-at-2am': {
        'task': DailyReportTask.get_task_name(),
        'schedule': crontab(hour=2, minute=0),  # 02:00 AM
        'options': {
            'expires': 3600,
        }
    },

    # Chạy mỗi giờ
    'hourly-sync': {
        'task': SyncDataTask.get_task_name(),
        'schedule': crontab(minute=0),  # Mỗi giờ đúng xx:00
        'options': {
            'expires': 600,
        }
    },
    # Chạy mỗi thứ 2 lúc 9h sáng
    'weekly-cleanup-monday-9am': {
        'task': CleanupTask.get_task_name(),
        'schedule': crontab(hour=9, minute=0, day_of_week=1),  # Monday 9:00 AM
        'options': {
            'expires': 7200,
        }
    },
}

def get_beat_schedule():
    """
    Trả về schedule config cho Celery Beat

    Returns:
        dict: Schedule configuration
    """
    return PERIODIC_SCHEDULES
