from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class AgentOutput:
    agent: str
    data: Dict[str, Any]
    status: str = "completed"
