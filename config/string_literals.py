# Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"

# Domains
DOMAIN_SALARY = "salary"
DOMAIN_AGRICULTURE = "agriculture"

# Headings
TITLE_FACT_EXTRACTION = "=== Fact Extraction using Gemini ==="
TITLE_EXTRACTED_FACTS = "\n=== Extracted Facts ==="

# Prompts
PROMPT_CHOOSE_DOMAIN = f"Which domain do you want to extract for? ({DOMAIN_SALARY}/{DOMAIN_AGRICULTURE}): "
PROMPT_ENTER_DESC = "Enter the biography or description: \n> "

# Error & Status Messages
ERR_MISSING_API_KEY = "Please set the GEMINI_API_KEY environment variable or edit config/settings.py."
ERR_INVALID_DOMAIN = f"Invalid domain. Choose '{DOMAIN_SALARY}' or '{DOMAIN_AGRICULTURE}'."
ERR_RESTART_DOMAIN = f"Please choose either '{DOMAIN_SALARY}' or '{DOMAIN_AGRICULTURE}'."
ERR_EMPTY_INPUT = "Input cannot be empty."
ERR_PARSE_JSON = "Failed to parse JSON response from Gemini.\nRaw response:\n{response}"
ERR_API_CALL = "Error during API call: {e}"

MSG_EXTRACTING = "\nExtracting facts..."

# Main execution messages
TITLE_RUN_AGRO_FACTS = "=== Running Agro Facts ==="
TITLE_RUN_SALARY_FACTS = "=== Running Salary Facts ==="
TITLE_RUN_BIO_SALARY = "=== Salary Computation from Biography ==="

PROMPT_ENTER_BIO = "Enter a person's biography:\n> "
MSG_COMPUTING_SALARY = "\nComputing monthly salary from extracted facts..."
SALARY_SUMMARY_DIVIDER = "\n" + "─" * 48
SALARY_SECTION_INTRO = "👤  Intro"
SALARY_SECTION_INCOME = "💰  Income"
SALARY_SECTION_TAXES = "🧾  Calculated Taxes"
SALARY_SECTION_TAKEHOME = "📬  Monthly Take-Home"
MSG_SALARY_FAILURE = (
    "\n❌ Unable to compute monthly salary. "
    "Please ensure the biography contains salary, marital status, "
    "and CIT contribution information."
)

# Follow-up question prompts (used when extracted facts are incomplete)
MSG_MISSING_FIELDS = "\n⚠️  Some details could not be extracted. Please answer the follow-up questions below."
PROMPT_FOLLOWUP_NAME           = "  • What is the person's full name? > "
PROMPT_FOLLOWUP_ANNUAL_SALARY  = "  • What is their annual salary in NPR? > "
PROMPT_FOLLOWUP_STATUS         = "  • What is their marital status? (married/unmarried) > "
PROMPT_FOLLOWUP_CIT            = "  • What is their annual CIT contribution in NPR? (enter 0 if none) > "
ERR_FOLLOWUP_SALARY_NUMBER     = "     ⚠️  Please enter a valid number for salary."
ERR_FOLLOWUP_CIT_NUMBER        = "     ⚠️  Please enter a valid number for CIT contribution."
ERR_FOLLOWUP_STATUS_INVALID    = "     ⚠️  Please enter either 'married' or 'unmarried'."
MSG_FACTS_COMPLETE             = "\n✅  All required details collected. Proceeding with salary computation..."

MSG_FINAL_FACTS = "Final Facts:"
MSG_EXPLANATION_TREE = "\nExplanation Tree"

# File Paths
PATH_FERTILIZER_RULES = "rules/fertilizer_rules.dsl"
PATH_SAMPLE_FACTS = "resources/sample_facts.json"
PATH_SALARY_TAX_RULES = "rules/salary_tax.dsl"
PATH_SALARY_FACTS = "resources/salary_facts.json"
