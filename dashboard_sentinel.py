import streamlit as st
from datetime import datetime

# --- Internal Logic Imports (Direct call for Cloud compatibility) ---
from clinical_logic import evaluate_metabolic_risk
from agent_logic import run_clinical_briefing
from schemas import ClinicalDataInput

# --- UI Configuration: Medical Grade Interface ---
st.set_page_config(
    page_title="PDAC Sentinel v3.0 | Clinical Support",
    page_icon="🔬",
    layout="wide"
)

# Professional CSS to align with corporate medical software aesthetics
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .report-card { 
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 12px; 
        border-left: 6px solid #005a87;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 PDAC Sentinel: Metabolic Decoupling Engine")
st.info("Decision Support System based on END-PAC (Mayo Clinic) and UK-EDI validated protocols.")

# --- Sidebar: Clinical Data Acquisition ---
with st.sidebar:
    st.header("Patient Entry Panel")
    
    # Using st.form to decouple widget interaction from API execution
    # This ensures increments (+/-) are responsive and fluid
    with st.form("clinical_input_form"):
        patient_id = st.text_input("Patient ID (Anonymized)", value="PT-1024")
        age = st.number_input("Age at Screening", min_value=18, max_value=110, value=60, step=1)
        
        st.divider()
        st.subheader("Longitudinal Biomarkers (12m)")
        
        col1, col2 = st.columns(2)
        with col1:
            curr_hba1c = st.number_input("Current HbA1c (%)", value=7.5, step=0.1, format="%.1f")
            curr_bmi = st.number_input("Current BMI", value=26.0, step=0.1, format="%.1f")
        with col2:
            prev_hba1c = st.number_input("Previous HbA1c (%)", value=6.2, step=0.1, format="%.1f")
            prev_bmi = st.number_input("Previous BMI", value=28.0, step=0.1, format="%.1f")
            
        st.divider()
        months_onset = st.slider("Months since Diabetes diagnosis", 0, 60, 12)
        on_metformin = st.checkbox("Active Antidiabetic Therapy (Metformin)")
        has_pancreatitis = st.checkbox("History of Chronic Pancreatitis")
        
        # Form submission trigger
        submit_btn = st.form_submit_button("ANALYZE CASE", type="primary", use_container_width=True)

# --- Main Logic: Direct Logic Execution (Cloud Optimized) ---
if submit_btn:
    # Prepare data object for internal processing
    input_data = ClinicalDataInput(
        patient_id=patient_id,
        age=age,
        current_hba1c=curr_hba1c,
        previous_hba1c=prev_hba1c,
        current_bmi=curr_bmi,
        previous_bmi=prev_bmi,
        months_since_diabetes_onset=months_onset,
        on_metformin=on_metformin,
        has_chronic_pancreatitis=has_pancreatitis
    )

    with st.spinner("Processing clinical trajectories via Sentinel v3..."):
        try:
            # Direct execution of the engines instead of requests.post
            results = evaluate_metabolic_risk(input_data)
            briefing = run_clinical_briefing(input_data)
            
            st.subheader("Diagnostic Stratification Report")
            
            # Executive Dashboard Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Risk Score", f"{results['score']} / 5")
            
            # Visual Risk Indicator
            risk_lvl = results['risk_level']
            color = "#d9534f" if risk_lvl == "HIGH" else "#f0ad4e" if risk_lvl == "MODERATE" else "#5cb85c"
            m2.markdown(f"### Status: <span style='color:{color}'>{risk_lvl}</span>", unsafe_allow_html=True)
            m3.metric("Analysis Timestamp", datetime.now().strftime("%H:%M:%S"))

            # Detected Pathological Flags
            if results['clinical_flags']:
                with st.expander("Detected Metabolic Anomalies", expanded=True):
                    for flag in results['clinical_flags']:
                        st.warning(f"**Flag:** {flag}")

            # AI-Generated Clinical Rationale
            st.markdown("### 📄 GP Executive Briefing")
            st.markdown(f"""
            <div class="report-card">
                {briefing}
            </div>
            """, unsafe_allow_html=True)
            
            # Actionable Recommendation
            st.success(f"**CLINICAL GUIDELINE:** {results['recommendation']}")

        except Exception as e:
            st.error(f"Inference Error: {str(e)}")

# --- Footer: Professional Disclaimer ---
st.divider()
st.caption("PDAC Sentinel v3.0 | Proprietary Diagnostic Algorithm | Restricted to Clinical Professional Use.")