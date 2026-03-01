# PDAC Sentinel v3.0: Metabolic Decoupling Detection Engine

## 🔬 Mission Statement
Our primary goal is to **save lives** through the early detection of Pancreatic Ductal Adenocarcinoma (PDAC). By identifying the "Metabolic Decoupling" signature—where blood glucose rises while body weight falls—Sentinel provides a critical window for intervention before the disease reaches advanced stages.

## 🚀 Overview
PDAC Sentinel is a Clinical Decision Support System (CDSS) designed for General Practitioners (GPs). It integrates deterministic clinical logic based on validated oncology protocols (END-PAC & UK-EDI) with Large Language Models (LLMs) to provide actionable diagnostic intelligence.

## 🛠️ System Architecture
The platform follows a robust three-tier architecture:
1.  **Clinical Engine (Deterministic):** Evaluates longitudinal data (HbA1c and BMI deltas) to calculate a risk score from 0 to 5.
2.  **AI Briefing Agent:** Utilizes the `Qwen2.5-Coder-32B` model via Hugging Face API to generate professional executive summaries.
3.  **Surveillance Dashboard:** A Streamlit-based interface for real-time patient stratification.

## 📊 Clinical Logic (Metabolic Decoupling)
The system monitors specific biomarkers over a 12-month horizon:
* **Hyperglycemia:** HbA1c increase ≥ 1.0%.
* **Involuntary Weight Loss:** BMI decrease ≥ 1.0 point.
* **New-Onset Diabetes (NOD):** Focus on patients diagnosed within the last 36 months.
* **Treatment Resistance:** Failure of Metformin to stabilize glucose levels in the presence of weight loss.

## 💻 Technical Stack
* **Backend:** FastAPI (Python 3.10+)
* **Frontend:** Streamlit
* **AI Integration:** Hugging Face Inference API
* **Validation:** Pydantic for medical data integrity
