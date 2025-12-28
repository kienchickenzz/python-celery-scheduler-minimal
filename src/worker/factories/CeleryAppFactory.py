"""
Trách nhiệm: Tạo và config Celery app
DI Dependencies: CeleryConfig
"""
from celery import Celery

from src.infrastructure.CeleryConfig import CeleryConfig


class CeleryAppFactory:
    """
    Factory để tạo Celery application instance

    Sử dụng:
    - Client side: Tạo app để send tasks
    - Worker side: Tạo app để register và execute tasks
    """

    @staticmethod
    def create(config: CeleryConfig) -> Celery:
        """
        Tạo Celery app với configuration

        Args:
            config: CeleryConfig instance

        Returns:
            Celery: Configured Celery app instance
        """
        # Tạo Celery app
        app = Celery(
            config.app_name,
            broker=config.broker_url,
            backend=config.backend_url
        )

        # Apply configuration
        app.conf.update(**config.to_dict())

        print(f"[CeleryAppFactory] Created Celery app: {config.app_name}")
        print(f"[CeleryAppFactory] Broker: {config.broker_url}")
        print(f"[CeleryAppFactory] Backend: {config.backend_url}")

        return app
