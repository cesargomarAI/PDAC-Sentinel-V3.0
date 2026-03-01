from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn

# Project Imports
from schemas import ClinicalDataInput
from clinical_logic import evaluate_metabolic_risk
from agent_logic import run_clinical_briefing

app = FastAPI(
    title="PDAC Sentinel - Clinical Support System",
    version="3.0.0",
    description="Advanced Early Detection Engine for Pancreatic Cancer based on Metabolic Decoupling (END-PAC & UK-EDI)."
)

@app.post("/api/v3/stratify", tags=["Clinical Diagnostics"])
async def stratify_patient(patient_data: ClinicalDataInput):
    """
    Standardized endpoint for PDAC risk stratification. 
    Returns both the numerical score and the AI-generated clinical briefing.
    """
    try:
        # 1. Scientific Stratification (The Deterministic Brain)
        analysis_results = evaluate_metabolic_risk(patient_data)
        
        # 2. Agentic Reasoning (The AI Briefing)
        # This provides the 'why' behind the numbers for the GP.
        clinical_briefing = run_clinical_briefing(patient_data)
        
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "patient_id": patient_data.patient_id,
            "clinical_results": analysis_results,
            "ai_briefing": clinical_briefing,
            "disclaimer": "This tool is a Clinical Decision Support System (CDSS) for professional use only."
        }
    except Exception as e:
        # Professional medical logging
        print(f"[CRITICAL ERROR] Inference Engine Failure: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred in the Clinical Inference Engine."
        )

if __name__ == "__main__":
    # Standard production-ready configuration
    uvicorn.run(app, host="0.0.0.0", port=8000)