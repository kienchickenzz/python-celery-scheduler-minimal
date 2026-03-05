"""
Example Periodic Task: Cleanup old data
"""
import logging
from datetime import datetime

from src.shared.interface.IPeriodicTaskProcessor import IPeriodicTaskProcessor
from src.shared.model.JobResult import JobResult
from src.shared.enum.JobStatus import JobStatus


logger = logging.getLogger("app")


class CleanupTask(IPeriodicTaskProcessor):
    """
    Periodic task để cleanup dữ liệu cũ
    Chạy định kỳ để xóa data quá hạn
    """

    @staticmethod
    def get_task_name() -> str:
        """Trả về tên task phải KHỚP với tên trong schedules.py"""
        return 'tasks.periodic.cleanup_old_data'

    def execute(self) -> JobResult:
        """
        Thực hiện cleanup logic

        Returns:
            JobResult: Kết quả cleanup
        """
        logger.info(f"Starting cleanup at {datetime.now()}")

        # Implement cleanup logic
        # Ví dụ:
        # - Xóa records cũ hơn 30 ngày
        # - Cleanup temp files
        # - Archive old logs

        deleted_count = 42  # Example số lượng đã xóa

        logger.info(f"Cleanup completed. Deleted {deleted_count} records")

        return JobResult(
            status=JobStatus.SUCCESS,
            result={'deleted_count': deleted_count},
            error=None
        )