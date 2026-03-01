import streamlit as st
from huggingface_hub import InferenceClient
from clinical_logic import evaluate_metabolic_risk
from schemas import ClinicalDataInput

# --- Security: Accessing the token via Streamlit Secrets ---
# On your local machine, this will look for a .streamlit/secrets.toml file.
# In the Cloud, you will configure this in the "Secrets" settings.
HF_TOKEN = st.secrets["HF_TOKEN"]

client = InferenceClient(
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=HF_TOKEN
)

def run_clinical_briefing(patient_data: ClinicalDataInput):
    """
    Orchestrates the analysis with hybrid control logic to prevent AI hallucinations.
    Ensures that for low-risk patients, the explanation is strictly deterministic.
    """
    # 1. Get validated clinical results
    results = evaluate_metabolic_risk(patient_data)
    
    # 2. Safety Gate: If Risk is LOW, do NOT use AI for reasoning. 
    # This prevents the AI from suggesting cancer in healthy patients.
    if results['score'] <= 1:
        return (f"The patient's metabolic profile is stable. No signs of PDAC-related 'metabolic decoupling' "
                f"were detected. Current HbA1c and BMI trajectories are within expected ranges for standard "
                f"diabetic management. No urgent oncological referral is indicated at this time.")

    # 3. AI Agentic Reasoning: Only for Moderate/High risk where 'Why' matters.
    messages = [
        {"role": "system", "content": "You are a professional Medical Oncologist. You must be precise and follow the provided score results."},
        {"role": "user", "content": f"""
            Analyze this case for the doctor:
            - Risk Score: {results['score']}/5
            - Risk Level: {results['risk_level']}
            - Detected Flags: {', '.join(results['clinical_flags'])}
            
            Provide a 3-sentence clinical rationale explaining why this specific patient 
            is at risk. Be direct and concise.
        """}
    ]
    
    try:
        response = client.chat_completion(messages=messages, max_tokens=300, temperature=0.1)
        return response.choices[0].message.content
    except Exception as e:
        # Professional fallback logging
        print(f"[LOG] AI Service unavailable: {str(e)}")
        return f"Clinical status is {results['risk_level']}. Please follow the recommended clinical guideline."