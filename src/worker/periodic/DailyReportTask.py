"""
Example Periodic Task: Generate Daily Report
"""
from typing import Dict, Any
from datetime import datetime

from src.shared.interface.IPeriodicTaskProcessor import IPeriodicTaskProcessor


class DailyReportTask(IPeriodicTaskProcessor):
    """
    Periodic task để tạo báo cáo hàng ngày
    """

    @staticmethod
    def get_task_name() -> str:
        """Tên task phải KHỚP với schedules.py"""
        return 'tasks.periodic.generate_daily_report'

    def execute(self) -> Dict[str, Any]:
        """
        Tạo báo cáo hàng ngày

        Returns:
            Dict: Kết quả tạo báo cáo
        """
        print(f"[DailyReportTask] 📊 Generating daily report at {datetime.now()}")

        # Implement report generation
        # Ví dụ:
        # - Tổng hợp số liệu trong ngày
        # - Tạo file PDF/Excel
        # - Gửi email báo cáo

        report_items = 100  # Example

        print(f"[DailyReportTask] ✅ Report generated with {report_items} items")

        return {
            'status': 'success',
            'report_items': report_items,
            'timestamp': datetime.now().isoformat(),
        }