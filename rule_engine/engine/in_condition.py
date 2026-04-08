"""
File: in_condition.py
──────────────────────────
Author: santa
Project: agro_inference_engine
Created: 3/17/26 09:53 
Email: santa.basnet@wiseyak.com
Github: https://github.com/santabasnet
Organization: WiseYak / Integrated ICT
"""

from typing import Any, Dict, List

class InCondition:

    def __init__(self, field: str, values: List[Any]) -> None:
        self.field: str = field
        self.values: List[Any] = values

    def evaluate(self, facts: Dict[str, Any]) -> bool:

        if self.field not in facts:
            return False

        return bool(facts[self.field] in self.values)
