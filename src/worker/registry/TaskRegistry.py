"""
Trách nhiệm:
- Đăng ký processors với Celery
- Bridge giữa Celery và processors
- Error handling, retry logic

DI Dependencies:
- celery_app: Celery
- processors: Dict[str, ITaskProcessor]
- error_handler: IErrorHandler (Optional)
"""
from celery import Celery

from src.shared.interface.ITaskProcessor import ITaskProcessor
from src.shared.enum.JobStatus import JobStatus


class TaskRegistry:
    """
    Registry để đăng ký processors với Celery

    Chịu trách nhiệm:
    - Wrap processor.process() thành Celery task
    - Error handling
    - Retry logic
    """

    def __init__(
        self,
        celery_app: Celery,
        processors: dict[str, ITaskProcessor],
    ):
        self._app = celery_app
        self._processors = processors

    def register_all(self):
        """Đăng ký tất cả processors với Celery"""
        print(f"[TaskRegistry] Registering {len(self._processors)} processors...")

        for name, processor in self._processors.items():
            self._register_processor(name, processor)

        print(f"[TaskRegistry] All processors registered")

    def _register_processor(self, name: str, processor: ITaskProcessor):
        """
        Wrap processor.process() thành Celery task
        Handle errors, logging, metrics

        Args:
            name: Tên processor (vd: 'prediction')
            processor: Instance của ITaskProcessor
        """
        task_name = processor.get_task_name()

        # Tạo Celery task function
        @self._app.task(
            name=task_name,
            bind=True,
            autoretry_for=(Exception,),
            retry_kwargs={'max_retries': 3, 'countdown': 5},
            acks_late=True
        )
        def celery_task(self, job_data):
            """
            Celery task wrapper cho processor

            Args:
                self: Celery task instance (bind=True)
                job_data: Job data dictionary

            Returns:
                dict: Job result dictionary
            """
            try:
                print(f"\n{'='*60}")
                print(f"[TaskRegistry] Executing task: {task_name}")
                print(f"[TaskRegistry] Job ID: {job_data.get('id', 'unknown')}")
                print(f"{'='*60}")

                # Gọi processor để xử lý
                result = processor.process(job_data)

                # Check kết quả
                if result.status == JobStatus.FAILED:
                    print(f"[TaskRegistry] Task failed: {result.error}")

                print(f"[TaskRegistry] Task completed with status: {result.status.value}")

                # Return result dạng dict
                return result.to_dict()

            except Exception as e:
                # Log error
                print(f"[TaskRegistry] Task error: {str(e)}")
                print(f"[TaskRegistry] Retry count: {self.request.retries}/{self.max_retries}")

                # Re-raise để Celery xử lý retry
                raise

        print(f"[TaskRegistry] Registered processor '{name}' with task name '{task_name}'")
