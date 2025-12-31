from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Any, Optional

from src.shared.enum.JobStatus import JobStatus

@dataclass(frozen=True)
class JobResult:
    status: JobStatus # SUCCESS, FAILED, RETRY
    result: Optional[Any]
    error: Optional[str]

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize JobResult thành dict để return từ Celery task

        Returns:
            dict: Dictionary representation của JobResult
        """
        data = asdict(self)
        # Convert enum to value
        data['status'] = self.status.value
        return data
    