import json

# Load policy rules
with open("server/policy_rules.json") as f:
    RULES = json.load(f)

def check_exclusions(appraisal_data):
    """Returns True if no exclusions are violated."""
    description = appraisal_data.get("description", "").lower()
    for exclusion in RULES["exclusions"]:
        if exclusion.lower() in description:
            return False
    return True

def check_coverage_limit(appraisal_data):
    """Returns True if estimated value is within coverage limit."""
    property_type = appraisal_data.get("propertyType")
    value = appraisal_data.get("estimatedValue", 0)
    limit = RULES["coverageLimits"].get(property_type, float("inf"))
    return value <= limit

def compute_hazard_score(hazards):
    """Returns a weighted hazard score based on detected issues."""
    score = 0.0
    for hazard in hazards:
        weight = RULES["hazardWeights"].get(hazard, 0)
        score += weight
    return round(score, 2)

def get_risk_level(score):
    """Categorizes risk score into low, moderate, or high."""
    thresholds = RULES["riskThresholds"]
    if score >= thresholds["high"]:
        return "high"
    elif score >= thresholds["moderate"]:
        return "moderate"
    else:
        return "low"

def requires_manual_review(appraisal_data, score):
    """Checks if appraisal triggers manual review rules."""
    value = appraisal_data.get("estimatedValue", 0)
    property_type = appraisal_data.get("propertyType")
    limit = RULES["coverageLimits"].get(property_type, float("inf"))
    year_built = appraisal_data.get("yearBuilt", 2020)

    if value > limit:
        return True
    if score >= RULES["riskThresholds"]["high"]:
        return True
    if not appraisal_data.get("address"):
        return True
    if year_built < 1980:
        return True
    return False

def evaluate_appraisal(appraisal_data):
    """Main function to evaluate underwriting decision."""
    hazards = appraisal_data.get("hazards", [])
    score = compute_hazard_score(hazards)
    risk_level = get_risk_level(score)

    decision = {
        "risk_score": score,
        "risk_level": risk_level,
        "excluded": not check_exclusions(appraisal_data),
        "coverage_ok": check_coverage_limit(appraisal_data),
        "manual_review": requires_manual_review(appraisal_data, score),
        "underwriting_decision": "rejected" if not check_exclusions(appraisal_data) else (
            "manual_review" if requires_manual_review(appraisal_data, score) else "approved"
        )
    }

    return decision
