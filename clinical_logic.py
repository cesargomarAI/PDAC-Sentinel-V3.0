from schemas import ClinicalDataInput

def evaluate_metabolic_risk(data: ClinicalDataInput) -> dict:
    """
    Core Deterministic Engine for PDAC Sentinel.
    Implements scoring based on END-PAC (Mayo Clinic) and UK-EDI thresholds.
    Focuses on the 'Metabolic Decoupling' signature (Rising Glucose + Falling Weight).
    """
    score = 0
    clinical_flags = []

    # 1. Eligibility Check (Rule out patients where the model is not validated)
    if data.age < 50 or data.months_since_diabetes_onset > 36:
        return {
            "score": 0,
            "risk_level": "LOW",
            "clinical_flags": ["Patient does not meet high-risk screening criteria (Age >= 50 and NOD < 36 months)."],
            "recommendation": "Follow standard Type 2 Diabetes management."
        }

    # 2. Glucose Dynamics Analysis (HbA1c)
    hba1c_delta = data.current_hba1c - data.previous_hba1c
    if hba1c_delta >= 1.0:
        score += 2
        clinical_flags.append("Accelerated hyperglycemia (HbA1c rise >= 1.0%).")
    elif hba1c_delta >= 0.5:
        score += 1
        clinical_flags.append("Significant hyperglycemia (HbA1c rise >= 0.5%).")

    # 3. Weight Dynamics Analysis (BMI)
    bmi_delta = data.current_bmi - data.previous_bmi
    if bmi_delta <= -1.0:
        score += 2
        clinical_flags.append("Severe involuntary weight loss (BMI drop >= 1.0).")
    elif bmi_delta <= -0.5:
        score += 1
        clinical_flags.append("Significant involuntary weight loss (BMI drop >= 0.5).")

    # 4. Metabolic Resistance / Other Factors
    if data.on_metformin and hba1c_delta > 0.2:
        score += 1
        clinical_flags.append("Treatment Resistance: Rising glucose despite Metformin.")
    
    if data.has_chronic_pancreatitis:
        score += 1
        clinical_flags.append("High-risk background: Chronic Pancreatitis history.")

    # 5. Risk Stratification
    # Score Thresholds: 0-1 (Low), 2 (Moderate), 3+ (High/Urgent)
    if score >= 3:
        risk_level = "HIGH"
        rec = "URGENT Referral: Request Contrast-enhanced CT and Oncology consultation."
    elif score >= 2:
        risk_level = "MODERATE"
        rec = "Secondary Screening: Perform Urinary Biomarker Test (PDAC-v2) or EUS."
    else:
        risk_level = "LOW"
        rec = "Close monitoring: Re-evaluate metabolic trends in 3 months."

    return {
        "score": score,
        "risk_level": risk_level,
        "clinical_flags": clinical_flags,
        "recommendation": rec
    }