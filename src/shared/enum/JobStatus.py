from enum import Enum

class JobStatus(str, Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    RETRY = "Retry"
