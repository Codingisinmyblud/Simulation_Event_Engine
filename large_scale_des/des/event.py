from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class Event:
    """
    Lightweight container for scheduled simulation events.
    """
    time: float
    type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    id: int = field(default_factory=lambda: 0) 
    
    def __lt__(self, other):
        if self.time == other.time:
            if self.priority == other.priority:
                return self.id < other.id
            return self.priority < other.priority
        return self.time < other.time
