from typing import Any, Dict, List, Union

class NumberNode:
    def __init__(self, value: Union[float, int, str]) -> None:
        self.value: float = float(value)

    def eval(self, env: Dict[str, Any]) -> float:
        return self.value


class StringNode:
    def __init__(self, value: str) -> None:
        self.value: str = value.strip('"')

    def eval(self, env: Dict[str, Any]) -> str:
        return self.value


class VarNode:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def eval(self, env: Dict[str, Any]) -> Any:
        return env.get(self.name, 0.0)


class BinaryNode:
    def __init__(self, left: Any, op: str, right: Any) -> None:
        self.left = left
        self.op: str = op
        self.right = right

    def eval(self, env: Dict[str, Any]) -> float:
        l = self.left.eval(env)
        r = self.right.eval(env)

        if self.op == "*":
            return float(l * r)
        if self.op == "+":
            return float(l + r)
        if self.op == "-":
            return float(l - r)
        if self.op == "/":
            return float(l / r) if float(r) != 0.0 else 0.0
        return 0.0


class MinNode:
    def __init__(self, args: List[Any]) -> None:
        self.args: List[Any] = args

    def eval(self, env: Dict[str, Any]) -> float:
        return float(min(arg.eval(env) for arg in self.args))


class MaxNode:
    def __init__(self, args: List[Any]) -> None:
        self.args: List[Any] = args

    def eval(self, env: Dict[str, Any]) -> float:
        return float(max(arg.eval(env) for arg in self.args))
