from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ProcessedToken:
    token: str
    agent_name: Optional[str] = None
    event_type: Optional[str] = None
