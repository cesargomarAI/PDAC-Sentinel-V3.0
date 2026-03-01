from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ClinicalDataInput(BaseModel):
    """
    Data contract for PDAC Sentinel v3. 
    Strict validation for Early Pancreatic Cancer detection via Metabolic Decoupling.
    Based on END-PAC (Mayo Clinic) and UK-EDI (University College London) studies.
    """
    patient_id: str = Field(..., description="Anonymized patient identifier")
    age: int = Field(..., gt=18, lt=110, description="Patient age at screening")
    
    # Blood Glucose Dynamics (HbA1c)
    current_hba1c: float = Field(..., description="Current HbA1c level (%)")
    previous_hba1c: float = Field(..., description="HbA1c level 6-12 months ago (%)")
    
    # Weight Dynamics (BMI)
    current_bmi: float = Field(..., description="Current Body Mass Index")
    previous_bmi: float = Field(..., description="BMI 6-12 months ago")
    
    # Clinical History and Resistance
    months_since_diabetes_onset: int = Field(..., ge=0, le=60, description="Months since Type 2 Diabetes diagnosis")
    on_metformin: bool = Field(default=False, description="Is the patient currently on Metformin or other antidiabetics?")
    has_chronic_pancreatitis: bool = Field(default=False, description="History of chronic inflammation")

    # Professional validation for physiological ranges
    @field_validator('current_hba1c', 'previous_hba1c')
    @classmethod
    def validate_hba1c(cls, v):
        if not (3.0 <= v <= 20.0):
            raise ValueError(f"HbA1c value {v}% is out of clinical range (3.0-20.0).")
        return v

    @field_validator('current_bmi', 'previous_bmi')
    @classmethod
    def validate_bmi(cls, v):
        if not (10.0 <= v <= 60.0):
            raise ValueError(f"BMI value {v} is out of clinical range (10.0-60.0).")
        return v