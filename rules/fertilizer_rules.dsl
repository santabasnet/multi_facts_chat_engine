# Soil Factors
rule soil_factor_sandy:
    when soilType == "sandy"
    then soilFactor = 1.2

rule soil_factor_clay:
    when soilType == "clay"
    then soilFactor = 1.5

rule soil_factor_loamy:
    when soilType == "loamy"
    then soilFactor = 1.0

# Base Fertilizer per Crop
rule wheat_base_fertilizer:
    when crop == "wheat"
    then basePerHectare = 80.0

rule rice_base_fertilizer:
    when crop == "rice"
    then basePerHectare = 100.0

rule maize_base_fertilizer:
    when crop == "maize"
    then basePerHectare = 90.0

# Water Adjustment based on Rainfall
rule rainfall_low_adjustment:
    when rainfall == "low"
    then waterAdjustment = 1.3

rule rainfall_medium_adjustment:
    when rainfall == "medium"
    then waterAdjustment = 1.1

rule rainfall_high_adjustment:
    when rainfall == "high"
    then waterAdjustment = 0.9

# Fertilizer Calculation
rule fertilizer_calculation:
    when crop in ["rice", "wheat", "maize"]
    then fertilizer = basePerHectare * soilFactor * areaHectare * waterAdjustment

# Irrigation Requirement
rule irrigation_requirement:
    when rainfall == "low"
    then irrigationRequired = 1.0

rule irrigation_requirement_medium:
    when rainfall == "medium"
    then irrigationRequired = 0.5

rule irrigation_requirement_high:
    when rainfall == "high"
    then irrigationRequired = 0.0

# Estimated Yield
rule yield_estimation:
    when crop in ["rice", "wheat", "maize"]
    then estimatedYield = areaHectare * 6 * soilFactor

# Advisory Score
rule advisory_message:
    when crop in ["rice", "wheat", "maize"]
    then advisoryScore = fertilizer + estimatedYield