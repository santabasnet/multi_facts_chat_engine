from string import Template

SALARY_EXTRACTION_PROMPT = Template("""
# Your are Natural language to structured data converter in simple salary information in Json format.
The input is 'English' sentence.

The output Json format is:
```Json
{
	"name": ?,
	"annualSalary": ?,
	"status": ?,
	"citContribution": ?  
}
```

### The fields description:
	* `name`: is the full or given name of a person.
	* `annualSalary`: is the annual amount of salary a person received in Nepalese rupees.
	* `status`: is the matrial status, either `married` or `unmarried`.
	* `citContributes`: it is a the anual amount that a person agrees to put as an investment, it benifits tax slab in Nepal.
	
### Example:
NL Question: My name is Ram Krishna and married one. I recevied Rs 15,000,000/- annualy from a company named XCOM. I have
no any investment at all.

Output: 
```Json
{
	"name": "Ram Krishna", 
	"annualSalary": 1500000,
	"status": "married",
	"citContribution": 0  
}
```

## Rule: You exactly output the json formatted data, no other one. Put empty string like "" in case
you did not find the values.

## Task:
Convert the given sentence to Json output format.
$nl_query
"""
) 

AGRICUTURAL_EXTRACTION_PROMPT = Template("""
# You are a Natural Language to structured data converter for agricultural facts in JSON format.
The input is an 'English' sentence.

The output JSON format is:
```json
{
  "crop": ?,  # e.g., "wheat", "rice", "potato"
  "soilType": ?,  # e.g., "loamy", "sandy", "clay"
  "season": ?,  # e.g., "winter", "summer", "monsoon"
  "rainfall": ?,  # e.g., "high", "medium", "low"
  "areaHectare": ?,  # numeric value in hectares
  "temperature": ?  # numeric value in Celsius
}
```

### Field Descriptions:
- `crop`: The type of crop being cultivated.
- `soilType`: The type of soil in the field.
- `season`: The agricultural season (e.g., winter, summer, monsoon).
- `rainfall`: The amount of rainfall (e.g., high, medium, low).
- `areaHectare`: The area of land in hectares.
- `temperature`: The temperature in Celsius.

### Example:
NL Question: "In my 3-hectare farm, I grow wheat during the winter season. The soil here is loamy, 
and while the temperature stays around 20 degrees, we usually get medium rainfall"

Output:
```json
{
  "crop": "wheat",
  "soilType": "loamy",
  "season": "winter",
  "rainfall": "medium",
  "areaHectare": 3,
  "temperature": 20
}
```

## Rule: You exactly output the JSON formatted data, no other one. Put empty string like "" in case you did not find the values.

## Task:
Convert the given sentence to Json output format.
$nl_query
"""
) 


