from lark import Transformer
from typing import Any, List, Union

from rule_engine.dsl.ast_nodes import BinaryNode, NumberNode, VarNode, StringNode, MinNode, MaxNode
from rule_engine.engine.in_condition import InCondition
from rule_engine.engine.condition import Condition
from rule_engine.models.rule import Rule, Action


class DSLTransformer(Transformer):

    def rule(self, items: List[Any]) -> Rule:
        name = items[0]
        # when_clause now returns a list of conditions, so we map directly to Rule conditions
        when = items[1]
        then = items[2]
        return Rule(str(name), when, [then])

    def when_clause(self, items: List[Any]) -> List[Any]:
        # We can have multiple conditions separated by 'and'
        return items

    def then_clause(self, items: List[Any]) -> Any:
        return items[0]

    def condition(self, items: List[Any]) -> Union[Condition, InCondition]:

        if len(items) == 3:
            field, comp, value = items
            return Condition(str(field), str(comp), value)

        # IN operator
        field, values = items
        return InCondition(str(field), values)

    def eq(self, items: List[Any]) -> str: return "=="
    def neq(self, items: List[Any]) -> str: return "!="
    def lte(self, items: List[Any]) -> str: return "<="
    def gte(self, items: List[Any]) -> str: return ">="
    def lt(self, items: List[Any]) -> str: return "<"
    def gt(self, items: List[Any]) -> str: return ">"

    def field(self, items: List[Any]) -> str:
        return str(items[0])

    def string_val(self, items: List[Any]) -> StringNode:
        return StringNode(str(items[0]))

    def number_val(self, items: List[Any]) -> NumberNode:
        return NumberNode(float(items[0]))

    def value(self, items: List[Any]) -> str:
        return str(items[0]).replace('"', '')

    def list_value(self, items: List[Any]) -> List[str]:
        return [str(v).replace('"', '') for v in items]

    def assignment(self, items: List[Any]) -> Action:
        name, expr = items
        return Action(str(name), expr)

    def mul(self, items: List[Any]) -> BinaryNode: return BinaryNode(items[0], "*", items[1])
    def add(self, items: List[Any]) -> BinaryNode: return BinaryNode(items[0], "+", items[1])
    def sub(self, items: List[Any]) -> BinaryNode: return BinaryNode(items[0], "-", items[1])
    def div(self, items: List[Any]) -> BinaryNode: return BinaryNode(items[0], "/", items[1])

    def min_func(self, items: List[Any]) -> MinNode: return MinNode(items)
    def max_func(self, items: List[Any]) -> MaxNode: return MaxNode(items)

    def number(self, items: List[Any]) -> NumberNode: return NumberNode(float(items[0]))
    def string(self, items: List[Any]) -> StringNode: return StringNode(str(items[0]))
    def var(self, items: List[Any]) -> VarNode: return VarNode(str(items[0]))