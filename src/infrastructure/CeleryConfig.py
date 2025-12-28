"""
Celery Configuration

Trách nhiệm:
- Chứa tất cả settings cho Celery app
- Expose methods để config Celery
- Load config từ Config class (env vars)
"""
from dataclasses import dataclass
from typing import Any

from src.config import Config


@dataclass(frozen=True)
class CeleryConfig:
    """Celery application configuration"""

    app_name: str
    broker_url: str
    backend_url: str
    task_serializer: str = 'json'
    accept_content: list[str] | None = None
    result_serializer: str = 'json'
    timezone: str = 'UTC'
    enable_utc: bool = True
    task_track_started: bool = True
    task_time_limit: int = 30 * 60  # 30 minutes
    task_soft_time_limit: int = 25 * 60  # 25 minutes
    worker_prefetch_multiplier: int = 1
    worker_concurrency: int = 10
    task_acks_late: bool = True
    task_reject_on_worker_lost: bool = True
    broker_connection_retry_on_startup: bool = True

    # Optional: Celery Beat schedule
    beat_schedule: dict[str, Any] | None = None

    def __post_init__(self):
        """Set default values for mutable fields"""
        if self.accept_content is None:
            object.__setattr__(self, 'accept_content', ['json'])
        if self.beat_schedule is None:
              object.__setattr__(self, 'beat_schedule', {})

    @classmethod
    def from_config(
        cls,
        config: Config,
        app_name: str = 'celery_app',
        worker_concurrency: int = 10,
        beat_schedule: dict[str, Any] | None = None,
    ) -> 'CeleryConfig':
        """
        Tạo CeleryConfig từ Config instance (env vars)

        Args:
            config: Config instance để load env vars
            app_name: Tên Celery application
            worker_concurrency: Số worker processes

        Returns:
            CeleryConfig: Instance với giá trị từ env vars
        """
        # Load Redis config từ env
        redis_host = config.get_config('REDIS_HOST', 'localhost')
        redis_port = config.get_int('REDIS_PORT', 6379)
        redis_password = config.get_config('REDIS_PASSWORD', 'Pa55w.rd')
        redis_db = config.get_int('REDIS_DB', 0)

        # Build Redis URL
        redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}"

        return cls(
            app_name=app_name,
            broker_url=redis_url,
            backend_url=redis_url,
            worker_concurrency=worker_concurrency,
            accept_content=['json'],
            beat_schedule=beat_schedule,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert config thành dict để pass vào Celery app.conf.update()

        Returns:
            dict: Celery configuration dictionary
        """
        return {
            'task_serializer': self.task_serializer,
            'accept_content': self.accept_content,
            'result_serializer': self.result_serializer,
            'timezone': self.timezone,
            'enable_utc': self.enable_utc,
            'task_track_started': self.task_track_started,
            'task_time_limit': self.task_time_limit,
            'task_soft_time_limit': self.task_soft_time_limit,
            'worker_prefetch_multiplier': self.worker_prefetch_multiplier,
            'worker_concurrency': self.worker_concurrency,
            'task_acks_late': self.task_acks_late,
            'task_reject_on_worker_lost': self.task_reject_on_worker_lost,
            'broker_connection_retry_on_startup': self.broker_connection_retry_on_startup,
            'beat_schedule': self.beat_schedule,
        }
