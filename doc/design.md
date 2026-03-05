Cấu trúc Codebase

```md
src/
├── __main__.py              # Entry point với argparse (--worker | --beat)
├── config.py                # Config class đọc env vars
├── run_periodic_worker.py   # Khởi động Celery Worker
├── run_beat.py              # Khởi động Celery Beat Scheduler
├── infrastructure/
│   ├── CeleryConfig.py      # Dataclass config cho Celery
│   └── schedules.py         # Định nghĩa PERIODIC_SCHEDULES (crontab, interval)
├── shared/
│   ├── interface/
│   │   └── IPeriodicTaskProcessor.py  # Interface cho periodic tasks
│   ├── model/
│   │   └── JobResult.py     # Dataclass kết quả job
│   └── enum/
│       └── JobStatus.py     # Enum: SUCCESS, FAILED, RETRY
└── worker/
    ├── CeleryAppFactory.py      # Factory tạo Celery app
    ├── PeriodicTaskRegistry.py  # Registry đăng ký tasks với Celery
    └── periodic_task/
        ├── CleanupTask.py
        ├── DailyReportTask.py
        └── SyncDataTask.py
```