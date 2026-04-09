import json
from typing import Any, Dict, List
from rule_engine.dsl.parser import load_rules
from rule_engine.engine.working_memory import WorkingMemory
from rule_engine.engine.inference_engine import InferenceEngine
from rule_engine.models.rule import Rule
import config.string_literals as literals


def execute_dsl(rules: List[Rule], facts: Dict[str, Any]) -> Dict[str, Any]:
    memory = WorkingMemory(facts)
    engine = InferenceEngine(rules)

    result, explanation = engine.run(memory)

    print(literals.MSG_FINAL_FACTS)
    print(json.dumps(result, indent=4))

    print(literals.MSG_EXPLANATION_TREE)
    explanation.print()
    print("-" * 50 + "\n")

    return result


def format_salary_summary(name: str, facts: Dict[str, Any], result: Dict[str, Any]) -> None:
    """Print a structured, bullet-style salary summary grouped into clear sections."""
    annual = facts.get("annualSalary", 0)
    status = facts.get("status", "N/A").capitalize()
    cit = facts.get("citContribution", 0)

    tax_base    = result.get("taxBase", 0.0)
    tax_ten     = result.get("taxTen", 0.0)
    tax_twenty  = result.get("taxTwenty", 0.0)
    tax_thirty  = result.get("taxThirty", 0.0)
    tax_highest = result.get("taxHighest", 0.0)
    total_tax   = result.get("totalTax", 0.0)
    monthly     = result.get("monthlyTakeHome", 0.0)

    d = literals.SALARY_SUMMARY_DIVIDER
    print(f"{d}")
    print(f"  ✅  Salary Summary")
    print(f"{d}")

    print(f"\n  {literals.SALARY_SECTION_INTRO}")
    print(f"    • Name            : {name.title()}")
    print(f"    • Marital Status  : {status}")
    print(f"    • CIT Contribution: NPR {cit:>12,.0f}")

    print(f"\n  {literals.SALARY_SECTION_INCOME}")
    print(f"    • Annual Salary   : NPR {annual:>12,.0f}")

    print(f"\n  {literals.SALARY_SECTION_TAXES}")
    if tax_base:    print(f"     1% Slab        : NPR {tax_base:>12,.2f}")
    if tax_ten:     print(f"    10% Slab        : NPR {tax_ten:>12,.2f}")
    if tax_twenty:  print(f"    20% Slab        : NPR {tax_twenty:>12,.2f}")
    if tax_thirty:  print(f"    30% Slab        : NPR {tax_thirty:>12,.2f}")
    if tax_highest: print(f"    36% Slab        : NPR {tax_highest:>12,.2f}")
    print(f"    {'─' * 36}")
    print(f"    Total Tax         : NPR {total_tax:>12,.2f}")

    print(f"\n  {literals.SALARY_SECTION_TAKEHOME}")
    print(f"    • Net Monthly Pay : NPR {monthly:>12,.2f}")
    print(f"{d}\n")


def run_agro_facts() -> None:
    print(literals.TITLE_RUN_AGRO_FACTS)
    with open(literals.PATH_FERTILIZER_RULES) as f:
        rules_text: str = f.read()
    
    rules_json = json.dumps({"rules": rules_text})
    rules: List[Rule] = load_rules(rules_json)
    
    with open(literals.PATH_SAMPLE_FACTS) as f:
        facts: Dict[str, Any] = json.load(f)
    execute_dsl(rules, facts)


def run_salary_facts() -> None:
    print(literals.TITLE_RUN_SALARY_FACTS)
    with open(literals.PATH_SALARY_TAX_RULES) as f:
        rules_text: str = f.read()
        
    rules_json = json.dumps({"rules": rules_text})
    rules: List[Rule] = load_rules(rules_json)
    
    with open(literals.PATH_SALARY_FACTS) as f:
        facts: Dict[str, Any] = json.load(f)
    execute_dsl(rules, facts)


def _fill_missing_salary_facts(facts: Dict[str, Any]) -> Dict[str, Any]:
    """Interactively ask follow-up questions for any salary field that is missing or empty."""

    def _is_blank(value: Any) -> bool:
        return value is None or value == "" or value == 0 and isinstance(value, str)

    missing_any = any(_is_blank(facts.get(k)) for k in ("name", "annualSalary", "status", "citContribution"))
    if not missing_any:
        return facts

    print(literals.MSG_MISSING_FIELDS)

    # --- name ---
    if _is_blank(facts.get("name")):
        while True:
            val = input(literals.PROMPT_FOLLOWUP_NAME).strip()
            if val:
                facts["name"] = val
                break

    # --- annualSalary ---
    if _is_blank(facts.get("annualSalary")):
        while True:
            val = input(literals.PROMPT_FOLLOWUP_ANNUAL_SALARY).strip()
            try:
                facts["annualSalary"] = float(val)
                break
            except ValueError:
                print(literals.ERR_FOLLOWUP_SALARY_NUMBER)

    # --- status ---
    if _is_blank(facts.get("status")):
        while True:
            val = input(literals.PROMPT_FOLLOWUP_STATUS).strip().lower()
            if val in ("married", "unmarried"):
                facts["status"] = val
                break
            print(literals.ERR_FOLLOWUP_STATUS_INVALID)

    # --- citContribution ---
    if _is_blank(facts.get("citContribution")):
        while True:
            val = input(literals.PROMPT_FOLLOWUP_CIT).strip()
            try:
                facts["citContribution"] = float(val)
                break
            except ValueError:
                print(literals.ERR_FOLLOWUP_CIT_NUMBER)

    print(literals.MSG_FACTS_COMPLETE)
    return facts


def run_salary_from_biography() -> None:
    from agent.extractor import extract_facts

    print(literals.TITLE_RUN_BIO_SALARY)
    biography = input(literals.PROMPT_ENTER_BIO).strip()

    if not biography:
        print(literals.ERR_EMPTY_INPUT)
        return

    print(literals.MSG_EXTRACTING)
    facts: Dict[str, Any] = extract_facts(literals.DOMAIN_SALARY, biography)

    if not facts:
        print(literals.MSG_SALARY_FAILURE)
        return

    print(literals.TITLE_EXTRACTED_FACTS)
    print(json.dumps(facts, indent=4))

    # Fill in any fields Gemini could not extract
    facts = _fill_missing_salary_facts(facts)

    print(literals.MSG_COMPUTING_SALARY)

    with open(literals.PATH_SALARY_TAX_RULES) as f:
        rules_text: str = f.read()

    rules_json = json.dumps({"rules": rules_text})
    rules: List[Rule] = load_rules(rules_json)

    result = execute_dsl(rules, facts)

    monthly = result.get("monthlyTakeHome")
    total_tax = result.get("totalTax")
    name = result.get("name", facts.get("name", "The person"))

    if monthly is not None and total_tax is not None:
        format_salary_summary(name, facts, result)
    else:
        print(literals.MSG_SALARY_FAILURE)


if __name__ == "__main__":
    # run_agro_facts()
    # run_salary_facts()
    run_salary_from_biography()
