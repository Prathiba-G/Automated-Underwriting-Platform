import json
import numpy as np
import joblib

# Load hazard weights and thresholds from policy rules
with open("server/policy_rules.json") as f:
    RULES = json.load(f)

# Load ML model and scaler (if using ML-based scoring)
try:
    model = joblib.load("server/models/risk_scorer/risk_model.pkl")
    scaler = joblib.load("server/models/risk_scorer/feature_scaler.pkl")
except:
    model = None
    scaler = None

def compute_rule_based_score(hazards):
    """Calculates risk score using weighted hazard rules."""
    score = 0.0
    for hazard in hazards:
        score += RULES["hazardWeights"].get(hazard, 0)
    return round(score, 2)

def compute_ml_score(appraisal_data):
    """Uses trained ML model to predict risk score."""
    if not model or not scaler:
        return None

    features = [
        appraisal_data.get("yearBuilt", 2020),
        appraisal_data.get("squareFootage", 1500),
        appraisal_data.get("estimatedValue", 300000),
        len(appraisal_data.get("hazards", []))
    ]
    scaled = scaler.transform([features])
    score = model.predict(scaled)[0]
    return round(float(score), 2)

def get_risk_level(score):
    """Categorizes score into low, moderate, or high."""
    thresholds = RULES["riskThresholds"]
    if score >= thresholds["high"]:
        return "high"
    elif score >= thresholds["moderate"]:
        return "moderate"
    else:
        return "low"

def assess_risk(appraisal_data, use_ml=False):
    """Main function to compute score and risk level."""
    score = compute_ml_score(appraisal_data) if use_ml else compute_rule_based_score(appraisal_data.get("hazards", []))
    level = get_risk_level(score)
    return {
        "risk_score": score,
        "risk_level": level
    }
