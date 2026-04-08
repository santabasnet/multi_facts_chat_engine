# --- Nepal Income Tax Rules (FY 2080/81) ---

# Status Initialization
rule status_unmarried:
    when status == "unmarried"
    then maritalFactor = 1.0

rule status_married:
    when status == "married"
    then maritalFactor = 1.2

# 1% Social Security Tax (Base Slab)
rule tax_slab_1_unmarried:
    when status == "unmarried" and annualSalary <= 500000
    then taxBase = annualSalary * 0.01

rule tax_slab_1_married:
    when status == "married" and annualSalary <= 600000
    then taxBase = annualSalary * 0.01

# 10% Slab Calculation
rule tax_slab_10_unmarried:
    when status == "unmarried" and annualSalary > 500000
    then taxTen = (min(annualSalary, 700000) - 500000) * 0.10

rule tax_slab_10_married:
    when status == "married" and annualSalary > 600000
    then taxTen = (min(annualSalary, 800000) - 600000) * 0.10

# 20% Slab Calculation
rule tax_slab_20_unmarried:
    when status == "unmarried" and annualSalary > 700000
    then taxTwenty = (min(annualSalary, 1000000) - 700000) * 0.20

rule tax_slab_20_married:
    when status == "married" and annualSalary > 800000
    then taxTwenty = (min(annualSalary, 1100000) - 800000) * 0.20

# 30% Slab Calculation
rule tax_slab_30_unmarried:
    when status == "unmarried" and annualSalary > 1000000
    then taxThirty = (min(annualSalary, 2000000) - 1000000) * 0.30

rule tax_slab_30_married:
    when status == "married" and annualSalary > 1100000
    then taxThirty = (min(annualSalary, 2000000) - 1100000) * 0.30

# 36% Highest Slab (Above 2 Million)
rule tax_slab_36_highest:
    when annualSalary > 2000000
    then taxHighest = (annualSalary - 2000000) * 0.36

# Final Total Tax Calculation
rule total_tax_calculation:
    when status in ["unmarried", "married"]
    then totalTax = taxBase + taxTen + taxTwenty + taxThirty + taxHighest

# Monthly Take Home Estimation
rule monthly_net_salary:
    when annualSalary > 0
    then monthlyTakeHome = (annualSalary - totalTax) / 12