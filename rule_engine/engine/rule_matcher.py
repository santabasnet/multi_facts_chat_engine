from typing import Any

def match_rule(rule: Any, memory: Any, explanation: Any) -> bool:

    node: Any = None

    for cond in rule.conditions:
        evaluate_fn = getattr(cond, 'evaluate', None)
        if callable(evaluate_fn):
            if not evaluate_fn(memory.facts):
                return False
            continue

        value = memory.get(cond.field)
        if value is None:
            return False

        if cond.op == "==" and value != cond.value:
            return False
        if cond.op == "!=" and value == cond.value:
            return False
        if cond.op == ">" and value <= cond.value:
            return False
        if cond.op == "<" and value >= cond.value:
            return False

    return True
