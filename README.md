# PDAC Sentinel v3.0: Metabolic Decoupling Detection Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pdac-sentinel-v3.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🔬 Mission Statement
Our primary goal is to **save lives** through the early detection of Pancreatic Ductal Adenocarcinoma (PDAC). By identifying the "Metabolic Decoupling" signature—where blood glucose rises while body weight falls—Sentinel provides a critical window for intervention before the disease reaches advanced stages.

> **[🚀 Access the Live Clinical Dashboard](https://pdac-sentinel-v3.streamlit.app/)**

---

## 🚀 Overview
PDAC Sentinel is a **Clinical Decision Support System (CDSS)** designed for General Practitioners (GPs). It bridges the gap between raw longitudinal data and clinical action by integrating deterministic medical protocols with state-of-the-art Large Language Models (LLMs).

### 🛠️ System Architecture
The platform follows a robust three-tier architecture designed for reliability and safety:
1. **Clinical Engine (Deterministic):** Evaluates longitudinal data (HbA1c and BMI deltas) to calculate a risk score (0-5) based on validated oncology protocols (END-PAC & UK-EDI).
2. **AI Briefing Agent (LLM):** Utilizes **Qwen2.5-Coder-32B** via Hugging Face Inference API to synthesize complex metabolic flags into professional executive summaries.
3. **Safety Gate:** A hybrid validation layer that prevents AI hallucinations by forcing deterministic outputs in low-risk cases.

---

## 📊 Clinical Intelligence
The system monitors specific biomarkers over a 12-month horizon to detect PDAC's paraneoplastic effects:
* **Hyperglycemia:** HbA1c increase ≥ 1.0%.
* **Involuntary Weight Loss:** BMI decrease ≥ 1.0 point.
* **New-Onset Diabetes (NOD):** Focus on patients diagnosed within <36 months.
* **Treatment Resistance:** Failure of Metformin to stabilize glucose levels in the presence of weight loss.

---

## 💻 Technical Stack & Engineering Highlights
* **Core:** Python 3.10+ (Clean Code, Modular Design).
* **AI Integration:** Hugging Face Inference API with `smolagents` for structured reasoning.
* **Data Integrity:** **Pydantic** models for strict validation of clinical inputs.
* **Frontend:** **Streamlit** for real-time data visualization and UX.
* **Security:** Environment-based secret management (No hardcoded API keys).

### 🌟 Why this matters for Applied AI:
* **Hybrid AI:** Combines the reliability of hard-coded medical rules with the synthesis power of LLMs.
* **Production-Ready:** Developed with CI/CD compatibility and cloud-native deployment.
* **Ethical AI:** Implements "Guardrails" to ensure high-stakes medical decisions are always backed by data-driven flags.

---

## 📂 Project Structure
```text
├── dashboard_sentinel.py  # Streamlit UI & Orchestration
├── agent_logic.py        # LLM integration & Prompt Engineering
├── clinical_logic.py     # Deterministic Risk Scoring Engine
├── schemas.py           # Pydantic data models
└── requirements.txt      # Dependency management
