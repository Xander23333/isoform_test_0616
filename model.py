from pydantic import BaseModel
from typing import List, Any

class Condition(BaseModel):
    column: str
    operator: str
    value: Any

class Rule(BaseModel):
    conditions: List[Condition]
    priority: int
    rollout: int = None  # 可选

class Flag(BaseModel):
    name: str
    rules: List[Rule]
    default: Any

    @classmethod
    def from_dict(cls, data):
        if 'rules' in data:
            data['rules'] = [Rule(**rule) for rule in data['rules']]
        return cls(**data)

class EvaluateRequest(BaseModel):
    user_id: str
    flag: str

class User(BaseModel):
    user_id: str  # Unique user identifier (abc123)
    region: str   # User's geographic region (us, eu, cn)
    tier: str    