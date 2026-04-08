from typing import FrozenSet, Tuple, Any, Dict, List

import copy
from .rule_matcher import match_rule
from rule_engine.explain.explanation import ExplanationTree, ExplanationNode
from rule_engine.models.rule import Rule
from rule_engine.engine.working_memory import WorkingMemory


def execute_rule(rule: Rule, memory: WorkingMemory, tree: ExplanationTree) -> Tuple[WorkingMemory, ExplanationTree]:
    # 1. Create a new ExplanationNode (Data/Value object)
    node = ExplanationNode(rule.name)
    for cond in rule.conditions:
        node.add_condition(cond.field, memory.get(cond.field))

    # 2. Compute new facts without mutating the original memory
    # We create a shallow copy of the facts to avoid side effects
    new_facts: Dict[str, Any] = memory.facts.copy()

    for action in rule.actions:
        value = action.expr.eval(new_facts)
        new_facts[action.field] = value
        node.add_result(action.field, value)

    # 3. Return a NEW memory object and a NEW tree state
    # Assuming Memory has a constructor that takes facts
    new_memory = memory.__class__(new_facts)

    # If ExplanationTree.add mutates, we copy it first
    new_tree = copy.deepcopy(tree)
    new_tree.add(node)

    return new_memory, new_tree


class InferenceEngine:

    def __init__(self, rules: List[Rule]) -> None:
        self.rules: List[Rule] = sorted(rules, key=lambda r: r.priority, reverse=True)

    def _step(self, memory: WorkingMemory, fired: FrozenSet[str], explanation: ExplanationTree) -> Tuple[Dict[str, Any], ExplanationTree]:
        # Find the first rule that hasn't fired and matches the current memory
        ready_rule = next(
            (r for r in self.rules if
             r.name not in fired and match_rule(r, memory, explanation)),
            None
        )

        # Base Case: No more rules can be executed
        if ready_rule is None:
            return memory.facts, explanation

        # Recursive Step:
        # Instead of mutating, we produce NEW versions of memory and the fired set
        new_memory, new_explanation = execute_rule(
            ready_rule,
            memory,
            explanation
        )
        new_fired = frozenset(fired | {ready_rule.name})

        # Recurse with the new state
        return self._step(new_memory, new_fired, new_explanation)

    def run(self, memory: WorkingMemory) -> Tuple[Dict[str, Any], ExplanationTree]:
        # We use a frozenset for 'fired' to ensure immutability
        return self._step(memory, frozenset(), ExplanationTree())
