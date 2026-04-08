import sys
import json
print("starting debug")
from rule_engine.dsl.parser import load_rules
from rule_engine.engine.inference_engine import InferenceEngine
from rule_engine.engine.working_memory import WorkingMemory

print("imported ok")
with open("rules/salary_tax.dsl") as f:
    r_text = f.read()
print("read rules")
try:
    rules_json = json.dumps({"rules": r_text})
    rules = load_rules(rules_json)
    print(f"loaded {len(rules)} rules")
except Exception as e:
    print(f"error loading rules: {e}")
    sys.exit(1)

with open("resources/salary_facts.json") as f:
    facts = json.load(f)
print("loaded facts:", facts)
    
memory = WorkingMemory(facts)
engine = InferenceEngine(rules)
print("running engine")
try:
    res, expl = engine.run(memory)
    print("engine finished")
    
    import json
    print("Final Facts:")
    print(json.dumps(res, indent=4))

    print("\nExplanation Tree")
    expl.print()
    print("-" * 50 + "\n")
except Exception as e:
    print(f"engine error: {e}")
