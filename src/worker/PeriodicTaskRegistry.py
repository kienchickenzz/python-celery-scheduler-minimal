"""
Trách nhiệm:
- Đăng ký periodic tasks với Celery
- Quản lý lịch chạy (schedule)

DI Dependencies:
- celery_app: Celery
- periodic_tasks: Dict[str, IPeriodicTask]
"""
import logging

from celery import Celery

from src.shared.interface.IPeriodicTaskProcessor import IPeriodicTaskProcessor


logger = logging.getLogger("app")


class PeriodicTaskRegistry:
    """
    Registry để đăng ký periodic tasks với Celery Beat

    Chịu trách nhiệm:
    - Wrap IPeriodicTask.execute() thành Celery task
    - Quản lý schedule configuration
    - Error handling cho periodic tasks
    """

    def __init__(
        self,
        celery_app: Celery,
        periodic_tasks: dict[str, IPeriodicTaskProcessor],
    ):
        self._app = celery_app
        self._periodic_tasks = periodic_tasks

    def register_all(self):
        """Đăng ký tất cả periodic tasks với Celery"""
        logger.info(f"Registering {len(self._periodic_tasks)} periodic tasks...")

        for name, task in self._periodic_tasks.items():
            self._register_task(name, task)

        logger.info("All periodic tasks registered")

    def _register_task(self, name: str, task: IPeriodicTaskProcessor):
        """
        Wrap periodic task execute() thành Celery task

        Args:
            name: Tên task (vd: 'cleanup')
            task: Instance của IPeriodicTask
        """
        task_name = task.get_task_name()

        # Tạo Celery task function
        # TODO: Mỗi task có thể cần 1 cấu hình retry khác nhau???
        @self._app.task(
            name=task_name,
            bind=True,
            autoretry_for=(Exception,),
            retry_kwargs={'max_retries': 3, 'countdown': 10},
        )
        def celery_periodic_task(self):
            """
            Celery task wrapper cho periodic task

            Returns:
                dict: Kết quả thực thi (serialized từ JobResult)
            """
            try:
                logger.info("=" * 60)
                logger.info(f"Executing periodic task: {task_name}")
                logger.info("=" * 60)

                # Gọi task để thực thi, nhận về JobResult
                job_result = task.execute()

                logger.info(f"Periodic task completed: {task_name}")

                # Convert JobResult thành dict để Celery serialize
                return job_result.to_dict()

            except Exception as e:
                logger.error(f"Periodic task error: {str(e)}")
                logger.warning(f"Retry count: {self.request.retries}/{self.max_retries}")
                raise

        logger.debug(f"Registered periodic task '{name}' with task name '{task_name}'")
