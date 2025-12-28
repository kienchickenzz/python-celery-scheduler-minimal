"""
Example Periodic Task: Sync Data
"""
from typing import Dict, Any
from datetime import datetime

from src.shared.interface.IPeriodicTaskProcessor import IPeriodicTaskProcessor


class SyncDataTask(IPeriodicTaskProcessor):
    """
    Periodic task để đồng bộ dữ liệu
    """

    @staticmethod
    def get_task_name() -> str:
        """Tên task phải KHỚP với schedules.py"""
        return 'tasks.periodic.sync_data'

    def execute(self) -> Dict[str, Any]:
        """
        Đồng bộ dữ liệu từ external source

        Returns:
            Dict: Kết quả sync
        """
        print(f"[SyncDataTask] 🔄 Starting data sync at {datetime.now()}")

        # Implement sync logic
        # Ví dụ:
        # - Fetch data từ external API
        # - Update local database
        # - Log sync status

        synced_records = 250  # Example

        print(f"[SyncDataTask] ✅ Sync completed. Synced {synced_records} records")

        return {
            'status': 'success',
            'synced_records': synced_records,
            'timestamp': datetime.now().isoformat(),
        }