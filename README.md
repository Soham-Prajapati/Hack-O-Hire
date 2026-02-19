# 🏦 SAR Narrative Generator with Intelligent Audit Trail

> AI-powered Suspicious Activity Report drafting system with full audit trail for financial compliance.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41-red?logo=streamlit)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-purple)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🚀 What It Does

Banks must file **Suspicious Activity Reports (SARs)** whenever they detect potential money laundering, fraud, or financial crime. Drafting these takes **5–6 hours per report**.

Our system:
1. **Ingests** transaction alerts + customer KYC data
2. **Generates** FinCEN-compliant SAR narratives using a Multi-Agent AI pipeline
3. **Explains** every AI decision with a complete audit trail
4. **Enables** human analysts to review, edit, and approve drafts

**Result:** 95% reduction in drafting time. Fully transparent. Regulator-ready.

---

## 🏗️ Architecture

```
Frontend (Streamlit) → REST API (FastAPI) → Multi-Agent Pipeline (LangChain)
                                                    ↓
                                    ┌───────────────┼───────────────┐
                                    ↓               ↓               ↓
                              ChromaDB         Ollama/Llama     PostgreSQL
                            (RAG Templates)   (LLM Inference)  (Audit Logs)
```

### Multi-Agent Pipeline
| Agent | Role |
|-------|------|
| **Data Analyst** | Extracts transaction patterns & anomalies |
| **Compliance Mapper** | Maps findings to regulatory typologies |
| **Narrator** | Drafts SAR in FinCEN format (5Ws + How) |
| **QA Validator** | Scores completeness, compliance, evidence linkage |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Llama 3.1 8B (via Ollama) |
| Orchestration | LangChain |
| Vector DB | ChromaDB |
| Database | PostgreSQL |
| Backend | FastAPI |
| Frontend | Streamlit |
| ML Classifier | XGBoost |
| Deployment | Docker |

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- [Ollama](https://ollama.com/) installed

- [Ollama](https://ollama.com/) installed

### 🚀 1. One-Click Startup (Recommended)
Run the all-in-one script to start Backend, Frontend, and AI services:
```bash
./start.sh
```
*(This closes old processes, checks Ollama, and launches everything)*

### 2. Manual Setup
If you prefer running services separately:
```bash
git clone https://github.com/Soham-Prajapati/Hack-O-Hire.git
cd Hack-O-Hire

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 2. Start Services
```bash
# Pull the LLM model
ollama pull llama3.1:8b

# Start PostgreSQL
docker-compose up -d postgres

# Start Backend
cd backend && uvicorn app.main:app --reload --port 8000

# Start Frontend (new terminal)
cd frontend && streamlit run app.py --server.port 8501
```

### 3. Open in Browser
- **Frontend:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs

---

## 📁 Project Structure

```
Hack-O-Hire/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── api/
│   │   │   ├── routes.py        # API endpoints
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── core/
│   │   │   ├── rag_pipeline.py  # LangChain RAG setup
│   │   │   ├── llm_engine.py    # Ollama/Llama integration
│   │   │   └── audit_logger.py  # Reasoning trace logger
│   │   └── utils/
│   │       └── data_parser.py   # CSV/JSON ingestion
│   ├── knowledge_base/
│   │   ├── sar_templates/       # SAR narrative templates
│   │   └── regulations/         # FinCEN docs
│   └── requirements.txt
├── frontend/
│   ├── app.py                   # Streamlit main app
│   ├── pages/
│   │   ├── 1_📊_Dashboard.py
│   │   ├── 2_📝_SAR_Editor.py
│   │   └── 3_🔍_Audit_Trail.py
│   └── requirements.txt
├── ml_models/                   # XGBoost typology classifier
├── data/
│   └── sample_data/             # Demo transaction datasets
├── docker-compose.yml
└── README.md
```

---

## 📊 Datasets Used

| Dataset | Source |
|---------|--------|
| [IBM AMLSim](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) | Synthetic AML transactions |
| [SAML-D](https://www.kaggle.com/datasets/berkanoztas/anti-money-laundering-transaction-data-saml-d) | 9.5M transactions, 28 typologies |
| [FinCEN SAR Guidance](https://www.fincen.gov/resources/statutes-and-regulations/guidance/suspicious-activity-report-narrative) | Regulatory templates |

---

## 👥 Team — VayuDevs

> Sardar Patel Institute of Technology

| Member | Role |
|--------|------|
| Soham Prajapati | Backend + AI Integration Lead |
| Dev Gaglani | LLM/RAG + AI Core Lead |
| Siddh Sakariya | Frontend Lead |
| Het Salot | Data & ML Engineer |
| Sakshi Rathi | Docs, PPT & Submission Lead |

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built for Hack-O-Hire 2026 🏆*
