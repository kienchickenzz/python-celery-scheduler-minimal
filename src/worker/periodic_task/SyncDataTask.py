"""
Example Periodic Task: Sync Data
"""
import logging
from datetime import datetime

from src.shared.interface.IPeriodicTaskProcessor import IPeriodicTaskProcessor
from src.shared.model.JobResult import JobResult
from src.shared.enum.JobStatus import JobStatus


logger = logging.getLogger("app")


class SyncDataTask(IPeriodicTaskProcessor):
    """
    Periodic task để đồng bộ dữ liệu
    """

    @staticmethod
    def get_task_name() -> str:
        """Tên task phải KHỚP với schedules.py"""
        return 'tasks.periodic.sync_data'

    def execute(self) -> JobResult:
        """
        Đồng bộ dữ liệu từ external source

        Returns:
            JobResult: Kết quả sync
        """
        logger.info(f"Starting data sync at {datetime.now()}")

        # Implement sync logic
        # Ví dụ:
        # - Fetch data từ external API
        # - Update local database
        # - Log sync status

        synced_records = 250  # Example

        logger.info(f"Sync completed. Synced {synced_records} records")

        return JobResult(
            status=JobStatus.SUCCESS,
            result={'synced_records': synced_records},
            error=None
        )