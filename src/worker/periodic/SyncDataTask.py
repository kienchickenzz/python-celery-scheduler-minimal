"""
Example Periodic Task: Sync Data
"""
from datetime import datetime

from src.shared.interface.IPeriodicTaskProcessor import IPeriodicTaskProcessor
from src.shared.model.JobResult import JobResult
from src.shared.enum.JobStatus import JobStatus


class SyncDataTask(IPeriodicTaskProcessor):
    """
    Periodic task để đồng bộ dữ liệu
    """

    @staticmethod
    def get_task_name() -> str:
        """Tên task phải KHỚP với schedules.py"""
        return 'tasks.periodic.sync_data'

    def execute(self) -> dict:
        """
        Đồng bộ dữ liệu từ external source

        Returns:
            dict: Kết quả sync
        """
        print(f"[SyncDataTask] 🔄 Starting data sync at {datetime.now()}")

        # Implement sync logic
        # Ví dụ:
        # - Fetch data từ external API
        # - Update local database
        # - Log sync status

        synced_records = 250  # Example

        print(f"[SyncDataTask] ✅ Sync completed. Synced {synced_records} records")

        return JobResult(
            status=JobStatus.SUCCESS,
            result={'synced_records': synced_records},
            error=None
        ).to_dict()