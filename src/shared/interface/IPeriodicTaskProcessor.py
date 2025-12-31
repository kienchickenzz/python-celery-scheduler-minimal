"""
Interface cho Periodic Task
Các periodic task cần implement interface này
"""
from abc import ABC, abstractmethod


class IPeriodicTaskProcessor(ABC):
    """
    Interface cho periodic tasks

    Mỗi periodic task cần:
    - Có tên task duy nhất
    - Có method execute() để chạy logic
    """

    @staticmethod
    def get_task_name() -> str:
        """
        Trả về tên unique của periodic task

        Returns:
            str: Task name (vd: 'cleanup_old_data')
        """
        return '' # Override trong class con

    # TODO: Trả về dto JobResult cụ thể
    @abstractmethod
    def execute(self) -> dict:
        """
        Thực thi logic của periodic task

        Returns:
            Dict[str, Any]: Kết quả thực thi
        """
        pass