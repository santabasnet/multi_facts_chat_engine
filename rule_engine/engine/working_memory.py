from typing import Any, Dict

class WorkingMemory:

    def __init__(self, facts: Dict[str, Any]) -> None:
        self.facts: Dict[str, Any] = dict(facts)

    def get(self, key: str) -> Any:
        return self.facts.get(key)

    def set(self, key: str, value: Any) -> None:
        self.facts[key] = value
