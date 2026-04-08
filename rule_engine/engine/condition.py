"""
File: condition.py
──────────────────────────
Author: santa
Project: agro_inference_engine
Created: 3/17/26 09:55 
Email: santa.basnet@wiseyak.com
Github: https://github.com/santabasnet
Organization: WiseYak / Integrated ICT
"""

from typing import Any, Dict

class Condition:

    def __init__(self, field: str, comparator: str, value: Any) -> None:
        self.field: str = field
        self.comparator: str = comparator
        self.value: Any = value

    def evaluate(self, facts: Dict[str, Any]) -> bool:

        if self.field not in facts:
            return False

        fact = facts[self.field]
        val = self.value.eval(facts) if hasattr(self.value, 'eval') else self.value

        if self.comparator == "==":
            return bool(fact == val)
        if self.comparator == "!=":
            return bool(fact != val)
        if self.comparator == "<":
            return bool(fact < val)
        if self.comparator == "<=":
            return bool(fact <= val)
        if self.comparator == ">":
            return bool(fact > val)
        if self.comparator == ">=":
            return bool(fact >= val)

        return False
