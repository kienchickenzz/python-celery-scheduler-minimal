"""
Example Periodic Task: Cleanup old data
"""
from typing import Dict, Any
from datetime import datetime

from src.shared.interface.IPeriodicTaskProcessor import IPeriodicTaskProcessor


class CleanupTask(IPeriodicTaskProcessor):
    """
    Periodic task để cleanup dữ liệu cũ
    Chạy định kỳ để xóa data quá hạn
    """

    @staticmethod
    def get_task_name() -> str:
        """Trả về tên task phải KHỚP với tên trong schedules.py"""
        return 'tasks.periodic.cleanup_old_data'

    def execute(self) -> Dict[str, Any]:
        """
        Thực hiện cleanup logic

        Returns:
            Dict: Kết quả cleanup
        """
        print(f"[CleanupTask] 🧹 Starting cleanup at {datetime.now()}")

        # Implement cleanup logic
        # Ví dụ:
        # - Xóa records cũ hơn 30 ngày
        # - Cleanup temp files
        # - Archive old logs

        deleted_count = 42  # Example số lượng đã xóa

        print(f"[CleanupTask] ✅ Cleanup completed. Deleted {deleted_count} records")

        return {
            'status': 'success',
            'deleted_count': deleted_count,
            'timestamp': datetime.now().isoformat(),
        }