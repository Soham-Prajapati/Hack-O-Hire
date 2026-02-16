# 🏦 SAR Narrative Generator with Audit Trail — Project Plan

> **Hackathon:** Hack-O-Hire | **Team Size:** 5 | **Timeline:** 2 Days  
> **Date Created:** Feb 16, 2026

---

## 📌 Problem Summary

Banks must file **Suspicious Activity Reports (SARs)** for potential money laundering, fraud, or financial crime. Writing these narratives is **mandatory, high-risk, and takes 5–6 hours per report**. We're building an AI system that:

1. Takes **transaction alerts + customer data** as input
2. Generates a **draft SAR narrative** in **FinCEN regulatory format**
3. Maintains a **complete audit trail** (explains *why* it wrote *what* it wrote)
4. Allows **human analysts to edit & approve**

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Streamlit)                   │
│   ┌──────────┐  ┌──────────────┐  ┌───────────────────┐     │
│   │ Data     │  │ SAR Narrative│  │ Audit Trail       │     │
│   │ Upload   │  │ Editor       │  │ Viewer            │     │
│   └──────────┘  └──────────────┘  └───────────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │ REST API
┌───────────────────────▼─────────────────────────────────────┐
│                    BACKEND (FastAPI)                        │
│  ┌────────────┐ ┌─────────────┐ ┌────────────────────────┐  │
│  │ Data       │ │ RAG Pipeline│ │ Audit Logger           │  │
│  │ Ingestion  │ │ (LangChain) │ │ (Reasoning Tracer)     │  │
│  │ Engine     │ │             │ │                        │  │
│  └─────┬──────┘ └──────┬──────┘ └───────────┬────────────┘  │
│        │               │                    │               │
│  ┌─────▼──────┐ ┌──────▼──────┐ ┌───────────▼────────────┐  │
│  │ PostgreSQL │ │ ChromaDB    │ │ Audit Log Store        │  │
│  │ (Cases &   │ │ (Vector DB) │ │ (PostgreSQL + JSON)    │  │
│  │ Txn Data)  │ │ SAR Templs  │ │                        │  │
│  └────────────┘ └─────────────┘ └────────────────────────┘  │
│                        │                                    │
│                ┌───────▼───────┐                            │
│                │ LLM Engine   │                             │
│                │ Ollama +     │                             │
│                │ Llama 3.1 8B │                             │
│                └──────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 Tech Stack (Final Selections)

| Layer | Technology | Why |
|-------|-----------|-----|
| **LLM** | Llama 3.1 8B (via Ollama) | Open-source, runs locally, no API costs, good for structured text |
| **Orchestration** | LangChain | RAG pipeline, prompt chaining, callback hooks for audit trail |
| **Vector DB** | ChromaDB | Lightweight, Python-native, zero infra needed |
| **Database** | PostgreSQL | Case storage, transaction data, audit logs |
| **Frontend** | Streamlit | Rapid prototyping, interactive UI, built-in editors |
| **Backend** | FastAPI | REST API, async support, easy to scale |
| **Explainability** | LangChain Callbacks + Custom Reasoning Tracer | Captures every decision step for audit |
| **Alerting** | Custom rule-based + LLM anomaly scoring | Flags high-risk patterns before SAR generation |

---

## 🎯 Core Features (What PS Expects)

### 1. Data Ingestion & Alert Processing
- Upload **CSV/JSON** of transaction alerts, customer KYC data, account data
- Parse and normalize data from varied formats
- Auto-detect suspicious patterns using rule-based + ML scoring
- **Dataset Used:** [IBM AMLSim](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) — Synthetic AML transaction data with labeled laundering patterns
- **Dataset Used:** [SAML-D (Anti Money Laundering Transaction Data)](https://www.kaggle.com/datasets/berkanoztas/anti-money-laundering-transaction-data-saml-d) — 9.5M transactions with 28 typologies

### 2. SAR Narrative Generation (LLM-Powered)
- Generates narratives in **FinCEN-compliant format** (Introduction → Body → Conclusion)
- Follows the **5Ws + How** structure: Who, What, When, Where, Why, How
- Uses RAG to pull from regulatory templates & past SAR examples
- **Reference Templates:** [FinCEN SAR Narrative Guidance](https://www.fincen.gov/resources/statutes-and-regulations/guidance/suspicious-activity-report-narrative) 
- **RAG Knowledge Base includes:**
  - FinCEN guidelines & advisory documents
  - RBI circulars on AML/CFT reporting
  - Sample SAR narrative structures
  - Money laundering typology references

### 3. Complete Audit Trail
- Every LLM call logs: **input data → prompt → retrieved context → generated output → reasoning**
- Uses **LangChain Callbacks** to capture the full decision pipeline
- Reasoning trace explains:
  - Which data points triggered suspicion
  - Which regulatory rules/patterns were matched
  - Why specific language was chosen
- Viewable in the UI as an expandable trail per SAR section
- **Reference:** [SHAP LLM Explainability Framework](https://github.com/slundberg/shap)

### 4. Human-in-the-Loop Editing
- Rich **text editor** in Streamlit for analysts to modify generated narrative
- Track all edits with **diff view** (original AI draft vs. final analyst version)
- Approval workflow: Draft → Review → Approve → Final
- Status tracking per SAR report

### 5. Alerting Mechanism
- Rule-based triggers (e.g., >₹50L from 40+ accounts in a week)
- LLM-scored risk levels (Low / Medium / High / Critical)
- Dashboard showing pending alerts with priority sorting
- Push notification simulation for critical alerts

### 6. Interactive Visualization / UI
- **Dashboard:** Overview of all cases, alerts, SAR statuses
- **Transaction Flow Graph:** Network visualization of money flows (using NetworkX + Streamlit)
- **Risk Heatmap:** Geographic/temporal distribution of suspicious activity
- **SAR Editor:** Side-by-side view of data points + narrative draft

---

## 🚀 USP Features (Beyond PS Requirements — Our Differentiators)

### 🔥 USP 1: Multi-Agent SAR Pipeline
Instead of one monolithic LLM call, we use **specialized agents**:
- **Data Analyst Agent** — Summarizes transaction patterns & anomalies
- **Compliance Agent** — Maps findings to regulatory typologies
- **Narrative Writer Agent** — Drafts the actual SAR narrative
- **QA Agent** — Validates completeness, checks for missing fields
- This produces **higher quality, more defensible** narratives

### 🔥 USP 2: Typology Auto-Classifier
- ML classifier that auto-detects money laundering typology (structuring, layering, smurfing, etc.)
- Trained on labeled data from SAML-D dataset (17 suspicious typologies)
- Feeds typology context into the narrative generator
- **Dataset:** [SAML-D](https://www.kaggle.com/datasets/berkanoztas/anti-money-laundering-transaction-data-saml-d) — 28 typologies (11 normal, 17 suspicious)
- **Model:** Lightweight XGBoost classifier on transaction features

### 🔥 USP 3: SAR Quality Scorer
- Automated scoring of generated SAR narratives on:
  - Completeness (all 5Ws covered?)
  - Regulatory compliance (proper format?)
  - Clarity & readability (Flesch score)
  - Evidence linkage (all claims backed by data?)
- Gives analysts confidence in the draft before review

### 🔥 USP 4: Cross-Case Pattern Detection
- Identifies links between cases (same beneficiary across multiple SARs)
- Network graph of entity relationships across cases
- Helps discover larger criminal rings, not just individual SARs

### 🔥 USP 5: Environment-Aware Deployment Config
- Single config file to switch between:
  - **Local** (Ollama + SQLite + ChromaDB file store)
  - **Cloud** (AWS Bedrock + RDS + OpenSearch)
  - **Hybrid** (Local LLM + Cloud DB)
- Demonstrates platform-agnostic design as PS requires

---

## 📊 Approximate Cost Estimate

| Item | Cost | Notes |
|------|------|-------|
| **Compute (Local Dev)** | ₹0 | Using local machines with GPU (RTX 3060+ or M1/M2 Mac) |
| **Ollama + Llama 3.1 8B** | ₹0 | Fully open-source, runs locally |
| **ChromaDB** | ₹0 | Open-source, in-memory/file-based |
| **PostgreSQL** | ₹0 | Local Docker instance |
| **Streamlit** | ₹0 | Open-source framework |
| **LangChain** | ₹0 | Open-source |
| **Cloud Hosting (Optional Demo)** | ~₹500–1,000 | If deploying to AWS EC2 for demo (t3.xlarge spot) |
| **Domain/SSL (Optional)** | ₹0 | Use localhost / ngrok for hackathon |
| **Datasets** | ₹0 | All open-source (Kaggle, FinCEN) |
| | | |
| **Total Estimated Cost** | **₹0 – ₹1,000** | Entirely free with local setup |

> **Note:** If using AWS Bedrock (Claude) instead of Ollama, API costs would be ~$5–15 for hackathon usage.

---

## 🔗 Key Resources & Links

### Datasets
| Dataset | Link | Usage |
|---------|------|-------|
| IBM AMLSim | [Kaggle](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) | Synthetic AML transactions with labeled patterns |
| SAML-D (9.5M txns) | [Kaggle](https://www.kaggle.com/datasets/berkanoztas/anti-money-laundering-transaction-data-saml-d) | 28 typologies, ML training data |
| PaySim Fraud Detection | [Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1) | Synthetic mobile transactions for fraud detection |
| Global Black Money Txns | [Kaggle](https://www.kaggle.com/datasets/waqi786/global-black-money-transactions-dataset) | Risk scoring & money laundering patterns |
| FinCEN SAR Stats | [Data.gov](https://catalog.data.gov/dataset/suspicious-activity-report-statistics-sar-stats) | Aggregate SAR filing statistics |
| OpenSanctions | [opensanctions.org](https://www.opensanctions.org/) | Sanctions lists & PEP data for entity matching |

### LLM & ML Models
| Model | Link | Usage |
|-------|------|-------|
| Llama 3.1 8B Instruct | [HuggingFace](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | Primary narrative generator |
| Mistral 7B Instruct | [HuggingFace](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) | Backup/comparison LLM |
| Fin-Llama 3.1 8B | [HuggingFace](https://huggingface.co/FinGPT/fingpt-mt_llama3.1-8b_lora) | Finance-tuned variant |
| XGBoost | [GitHub](https://github.com/dmlc/xgboost) | Typology classifier |
| SHAP | [GitHub](https://github.com/slundberg/shap) | Model explainability |

### Frameworks & Tools
| Tool | Link | Usage |
|------|------|-------|
| LangChain | [langchain.com](https://www.langchain.com/) | RAG pipeline & orchestration |
| ChromaDB | [trychroma.com](https://www.trychroma.com/) | Vector store for templates |
| Ollama | [ollama.com](https://ollama.com/) | Local LLM inference |
| Streamlit | [streamlit.io](https://streamlit.io/) | Frontend UI |
| FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) | Backend API |
| NetworkX | [GitHub](https://github.com/networkx/networkx) | Transaction network graphs |

### Regulatory References
| Document | Link |
|----------|------|
| FinCEN SAR Narrative Guidance | [fincen.gov](https://www.fincen.gov/resources/statutes-and-regulations/guidance/suspicious-activity-report-narrative) |
| FinCEN SAR Filing Instructions | [fincen.gov](https://www.fincen.gov/resources/filing-information) |
| FFIEC BSA/AML Examination Manual | [ffiec.gov](https://bsaaml.ffiec.gov/manual) |
| RBI Master Direction on KYC | [rbi.org.in](https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566) |

---

## 💡 Brainstormed Ideas (Realistically Doable in 2 Days)

### ✅ Definitely Doable
1. **Batch SAR Generation** — Upload 10 alerts, generate 10 SAR drafts in parallel
2. **Template Library** — Pre-built narrative templates for common typologies (structuring, smurfing, layering)
3. **Export to PDF** — One-click export of finalized SAR to PDF with proper formatting
4. **Role-Based Access** — Simple login system (Analyst / Reviewer / Admin roles)
5. **Dark Mode UI** — Professional-looking compliance dashboard

### ⚡ Stretch Goals (If Time Permits)
1. **Voice-to-SAR** — Analyst speaks observations, AI converts to narrative sections
2. **Regulatory Update Watcher** — Auto-fetch latest FinCEN advisories into RAG knowledge base
3. **SAR Similarity Search** — "Find similar past SARs" for reference during drafting
4. **Multi-Language Support** — Generate SAR narratives in Hindi/regional languages for Indian bank submissions
5. **Real-time Collaboration** — Two analysts editing same SAR simultaneously

---

## 🔐 Security & Compliance Considerations

- **Data Isolation:** Customer, transaction, and fraud data in separate schemas — no cross-domain leakage
- **RBAC:** Role-based access controls enforced at API level
- **Audit Logging:** Every user action logged (who viewed what, who edited what, when)
- **LLM Guardrails:** System prompt explicitly instructs unbiased, on-topic-only responses
- **No External API Calls:** All LLM inference is local (Ollama) — data never leaves the system
- **Session-based Data Handling:** No persistent storage of raw customer data beyond the session

---

## 🗂️ Folder Structure (Proposed)

```
Hack-O-Hire/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── api/
│   │   │   ├── routes.py        # API endpoints
│   │   │   └── auth.py          # RBAC middleware
│   │   ├── core/
│   │   │   ├── rag_pipeline.py  # LangChain RAG setup
│   │   │   ├── llm_engine.py    # Ollama/Llama integration
│   │   │   ├── audit_logger.py  # Reasoning trace logger
│   │   │   └── alerting.py      # Rule-based + ML alerting
│   │   ├── models/
│   │   │   ├── schemas.py       # Pydantic models
│   │   │   └── db_models.py     # SQLAlchemy models
│   │   ├── agents/
│   │   │   ├── data_analyst.py  # Data analysis agent
│   │   │   ├── compliance.py    # Regulatory mapping agent
│   │   │   ├── narrator.py      # SAR writer agent
│   │   │   └── qa_checker.py    # Quality assurance agent
│   │   └── utils/
│   │       ├── data_parser.py   # CSV/JSON ingestion
│   │       └── sar_formatter.py # FinCEN format templating
│   ├── knowledge_base/
│   │   ├── sar_templates/       # SAR narrative templates
│   │   ├── regulations/         # FinCEN docs, RBI circulars
│   │   └── typologies/          # AML typology descriptions
│   ├── data/
│   │   └── sample_data/         # Demo transaction datasets
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py                   # Streamlit main app
│   ├── pages/
│   │   ├── dashboard.py         # Main dashboard
│   │   ├── sar_editor.py        # SAR editing interface
│   │   ├── audit_trail.py       # Audit trail viewer
│   │   └── alerts.py            # Alert management
│   └── components/
│       ├── transaction_graph.py # Network visualization
│       └── risk_heatmap.py      # Risk visualization
├── ml_models/
│   ├── typology_classifier/     # XGBoost typology model
│   └── risk_scorer/             # Transaction risk scoring
├── docker-compose.yml
├── SAR_PROJECT_PLAN.md          # This file
├── SAR_PPT_DATA.md              # Presentation data
└── ps.txt                       # Problem statement
```

---
