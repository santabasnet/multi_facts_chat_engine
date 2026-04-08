import json
from lark import Lark
from pathlib import Path
from typing import Any, List
from .transformer import DSLTransformer

grammar: Path = Path(__file__).parent / "grammar.lark"

parser: Lark = Lark.open(str(grammar), parser="lalr", transformer=DSLTransformer())

def load_rules(text: str) -> List[Any]:
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "rules" in data:
            rules_text = data["rules"]
        else:
            rules_text = text
    except (json.JSONDecodeError, TypeError):
        rules_text = text

    tree: Any = parser.parse(rules_text)
    return tree.children
