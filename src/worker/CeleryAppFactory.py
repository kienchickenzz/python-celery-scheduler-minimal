"""
Trách nhiệm: Tạo và config Celery app
DI Dependencies: CeleryConfig
"""
import logging

from celery import Celery

from src.infrastructure.CeleryConfig import CeleryConfig


logger = logging.getLogger("app")


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

        logger.info(f"Created Celery app: {config.app_name}")
        logger.debug(f"Broker: {config.broker_url}")
        logger.debug(f"Backend: {config.backend_url}")

        return app
