from dataclasses import dataclass
from typing import List, Any

@dataclass
class Condition:
    column: str
    operator: str
    value: Any

@dataclass
class Rule:
    conditions: List[Condition]
    priority: int
    rollout: int = None  # 可选

@dataclass
class Flag:
    name: str
    rules: List[Rule]
    default: Any

@dataclass
class EvaluateRequest:
    user_id: str
    flag: str


@dataclass
class User:
    user_id: str  # Unique user identifier (abc123)
    region: str   # User's geographic region (us, eu, cn)
    tier: str    