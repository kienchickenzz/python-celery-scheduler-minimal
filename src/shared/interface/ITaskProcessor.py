"""
Trách nhiệm: Định nghĩa contract cho việc xử lý task
Dùng cho: Worker cần xử lý job từ queue
DI: Worker inject implementation này
"""
from abc import ABC, abstractmethod
from typing import Any

from src.shared.model.JobResult import JobResult

class ITaskProcessor(ABC):
    @abstractmethod
    def process(self, job_data: dict[str, Any]) -> JobResult:
        """Xử lý job và trả về kết quả"""
        pass

    @abstractmethod
    def get_task_name(self) -> str:
        """Tên task để đăng ký với Celery"""
        pass
