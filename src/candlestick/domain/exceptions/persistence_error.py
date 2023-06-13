from dataclasses import dataclass
from typing import Optional



@dataclass
class PersistenceError(Exception):
    """
    Generic exception for any persistence related errors, for example IntegrityErrors.
    """

    reason: Optional[str] = None
