from dataclasses import dataclass
from typing import Any, List


@dataclass
class Condition:
    field: str
    op: str
    value: object

@dataclass
class Action:
    field: str
    expr: Any

@dataclass
class Rule:
    name: str
    conditions: List[Condition]
    actions: List[Action]
    priority: int = 0
