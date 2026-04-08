from typing import Any, Dict, List, Tuple

class ExplanationNode:

    def __init__(self, rule_name: str) -> None:
        self.rule: str = rule_name
        self.conditions: List[Tuple[str, Any]] = []
        self.results: Dict[str, Any] = {}

    def add_condition(self, cond: str, value: Any) -> None:
        self.conditions.append((cond, value))

    def add_result(self, key: str, value: Any) -> None:
        self.results[key] = value


class ExplanationTree:

    def __init__(self) -> None:
        self.nodes: List[ExplanationNode] = []

    def add(self, node: ExplanationNode) -> None:
        self.nodes.append(node)

    def print(self) -> None:
        for n in self.nodes:
            print(f"Rule: {n.rule}")
            print(" Conditions:")
            for c,v in n.conditions:
                print("  ", c, "->", v)
            print(" Results:", n.results)
            print()
