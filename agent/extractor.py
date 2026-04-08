import os
import sys
import json
import google.generativeai as genai

# Add project root to sys.path so we can import from resources and config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from resources.prompts import SALARY_EXTRACTION_PROMPT, AGRICUTURAL_EXTRACTION_PROMPT
from config.settings import GEMINI_API_KEY
import config.string_literals as literals

def configure_gemini():
    api_key = GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(literals.ERR_MISSING_API_KEY)
        sys.exit(1)
    genai.configure(api_key=api_key)

def sanitize_gemini_json(text: str) -> str:
    """Applies a collection of sanitation rules sequentially to clean up Gemini JSON output."""
    sanitation_rules = [
        str.strip,
        lambda t: t.removeprefix("```json"),
        lambda t: t.removeprefix("```Json"),
        lambda t: t.removeprefix("```"),
        lambda t: t.removesuffix("```"),
        str.strip
    ]
    
    for rule in sanitation_rules:
        text = rule(text)
        
    return text

def extract_facts(domain: str, user_input: str) -> dict:
    configure_gemini()
    
    model = genai.GenerativeModel(literals.GEMINI_MODEL)
    
    if domain.lower() == literals.DOMAIN_SALARY:
        prompt = SALARY_EXTRACTION_PROMPT.substitute(nl_query=user_input)
    elif domain.lower() == literals.DOMAIN_AGRICULTURE:
        prompt = AGRICUTURAL_EXTRACTION_PROMPT.substitute(nl_query=user_input)
    else:
        print(literals.ERR_INVALID_DOMAIN)
        return {}
        
    try:
        response = model.generate_content(prompt)
        text = response.text
        # Clean up the markdown block formatting using collector style
        text = sanitize_gemini_json(response.text)
        data = json.loads(text)
        return data
        
    except json.JSONDecodeError as e:
        print(literals.ERR_PARSE_JSON.format(response=response.text))
        return {}
    except Exception as e:
        print(literals.ERR_API_CALL.format(e=e))
        return {}

def main():
    print(literals.TITLE_FACT_EXTRACTION)
    domain = input(literals.PROMPT_CHOOSE_DOMAIN).strip()
    
    if domain.lower() not in [literals.DOMAIN_SALARY, literals.DOMAIN_AGRICULTURE]:
        print(literals.ERR_RESTART_DOMAIN)
        sys.exit(1)
        
    user_input = input(literals.PROMPT_ENTER_DESC).strip()
    
    if not user_input:
        print(literals.ERR_EMPTY_INPUT)
        sys.exit(1)
        
    print(literals.MSG_EXTRACTING)
    facts = extract_facts(domain, user_input)
    
    if facts:
        print(literals.TITLE_EXTRACTED_FACTS)
        print(json.dumps(facts, indent=4))

if __name__ == "__main__":
    main()
