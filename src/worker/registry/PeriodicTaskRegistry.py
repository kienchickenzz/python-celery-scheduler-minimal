"""
Trách nhiệm:
- Đăng ký periodic tasks với Celery
- Quản lý lịch chạy (schedule)

DI Dependencies:
- celery_app: Celery
- periodic_tasks: Dict[str, IPeriodicTask]
"""
from celery import Celery

from src.shared.interface.IPeriodicTaskProcessor import IPeriodicTaskProcessor


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
        print(f"[PeriodicTaskRegistry] Registering {len(self._periodic_tasks)} periodic tasks...")

        for name, task in self._periodic_tasks.items():
            self._register_task(name, task)

        print(f"[PeriodicTaskRegistry] All periodic tasks registered")

    def _register_task(self, name: str, task: IPeriodicTaskProcessor):
        """
        Wrap periodic task execute() thành Celery task

        Args:
            name: Tên task (vd: 'cleanup')
            task: Instance của IPeriodicTask
        """
        task_name = task.get_task_name()

        # Tạo Celery task function
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
                dict: Kết quả thực thi
            """
            try:
                print(f"\n{'='*60}")
                print(f"[PeriodicTaskRegistry] Executing periodic task: {task_name}")
                print(f"{'='*60}")

                # Gọi task để thực thi
                result = task.execute()

                print(f"[PeriodicTaskRegistry] Periodic task completed: {task_name}")

                return result

            except Exception as e:
                print(f"[PeriodicTaskRegistry] Periodic task error: {str(e)}")
                print(f"[PeriodicTaskRegistry] Retry count: {self.request.retries}/{self.max_retries}")
                raise

        print(f"[PeriodicTaskRegistry] Registered periodic task '{name}' with task name '{task_name}'")
