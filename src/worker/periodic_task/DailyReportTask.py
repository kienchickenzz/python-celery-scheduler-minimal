"""
Example Periodic Task: Generate Daily Report
"""
import logging
from datetime import datetime

from src.shared.interface.IPeriodicTaskProcessor import IPeriodicTaskProcessor
from src.shared.model.JobResult import JobResult
from src.shared.enum.JobStatus import JobStatus


logger = logging.getLogger("app")


class DailyReportTask(IPeriodicTaskProcessor):
    """
    Periodic task để tạo báo cáo hàng ngày
    """

    @staticmethod
    def get_task_name() -> str:
        """Tên task phải KHỚP với schedules.py"""
        return 'tasks.periodic.generate_daily_report'

    def execute(self) -> JobResult:
        """
        Tạo báo cáo hàng ngày

        Returns:
            JobResult: Kết quả tạo báo cáo
        """
        logger.info(f"Generating daily report at {datetime.now()}")

        # Implement report generation
        # Ví dụ:
        # - Tổng hợp số liệu trong ngày
        # - Tạo file PDF/Excel
        # - Gửi email báo cáo

        report_items = 100  # Example

        logger.info(f"Report generated with {report_items} items")

        return JobResult(
            status=JobStatus.SUCCESS,
            result={'report_items': report_items},
            error=None
        )