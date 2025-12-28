from dataclasses import dataclass, asdict
from typing import Any, Optional

"""
Trách nhiệm: Mang dữ liệu giữa client và worker
Immutable, serializable
Không chứa business logic
"""
@dataclass(frozen=True)
class JobData:
    id: str
    type: str
    payload: dict[str, Any]
    metadata: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize JobData thành dict để gửi qua Celery

        Returns:
            dict: Dictionary representation của JobData
        """
        return asdict(self)
