from dataclasses import dataclass
from typing import Optional


@dataclass
class InvalidInstrumentISINException(Exception):
    """
    Raised if an instrument is not found.
    """
    reason: Optional[str] = None
