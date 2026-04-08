"""
File: fact_loader.py
──────────────────────────
Author: santa
Project: agro_inference_engine
Created: 3/17/26 09:56 
Email: santa.basnet@wiseyak.com
Github: https://github.com/santabasnet
Organization: WiseYak / Integrated ICT
"""
from typing import Dict, Union

def load_facts(text: str) -> Dict[str, Union[float, str]]:
    facts: Dict[str, Union[float, str]] = {}

    for line in text.splitlines():

        line = line.strip()

        if not line or line.startswith("#"):
            continue

        key, value_str = line.split("=", 1)

        key = key.strip()
        value = value_str.strip()

        if value.startswith('"'):
            facts[key] = value.replace('"', "")
        else:
            facts[key] = float(value)

    return facts
