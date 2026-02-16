# SAR Narrative Generator with Intelligent Audit Trail

> **Team:** [TeamName] | **Campus:** [CampusName] | **Date:** 16/02/2026  
> **Problem Statement:** SAR Narrative Generator with Audit Trail

---

## 1. Abstract

Banks are mandated to file Suspicious Activity Reports (SARs) whenever potential money laundering, fraud, or financial crime is detected. Drafting these narratives is a labor-intensive process, averaging 5–6 hours per report, with large institutions producing thousands annually. Quality inconsistencies and rising regulatory scrutiny further compound the challenge.

We present an AI-powered SAR Narrative Generator that automates the drafting of regulator-ready SAR narratives while maintaining full transparency and auditability. Our system employs a Multi-Agent RAG (Retrieval-Augmented Generation) pipeline — using Llama 3.1 8B as the local LLM, LangChain for orchestration, and ChromaDB for vector-based retrieval of regulatory templates and past SARs. Four specialized agents (Data Analyst, Compliance Mapper, Narrative Writer, QA Validator) collaboratively produce FinCEN-compliant narratives following the 5Ws+How structure. A complete audit trail captures every decision: which data points influenced the narrative, which regulatory patterns were matched, and why specific language was chosen. An integrated typology classifier (XGBoost trained on the SAML-D dataset) auto-identifies suspicious patterns like structuring, layering, and smurfing. The human-in-the-loop editor allows analysts to review, edit, and approve narratives before final submission, reducing drafting time by up to 95%.

---

## 2. System Architecture

### 2.1 Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                           │
│                        (Streamlit Frontend)                         │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────────────┐ │
│  │ Data Upload  │  │ SAR Editor &   │  │ Audit Trail Viewer &     │ │
│  │ & Dashboard  │  │ Approval Flow  │  │ Transaction Graph        │ │
│  └──────┬───────┘  └───────┬────────┘  └────────────┬─────────────┘ │
└─────────┼──────────────────┼────────────────────────┼───────────────┘
          │                  │                        │
          └──────────────────┼────────────────────────┘
                             │ REST API (HTTP/JSON)
┌────────────────────────────▼────────────────────────────────────────┐
│                        APPLICATION LAYER                            │
│                        (FastAPI Backend)                            │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              MULTI-AGENT PIPELINE (LangChain)                │   │
│  │  ┌────────────┐ ┌────────────┐ ┌──────────┐ ┌────────────┐  │   │
│  │  │ Data       │→│ Compliance │→│ Narrator │→│ QA         │  │   │
│  │  │ Analyst    │ │ Mapper     │ │ Agent    │ │ Validator  │  │   │
│  │  │ Agent      │ │ Agent      │ │          │ │ Agent      │  │   │
│  │  └────────────┘ └────────────┘ └──────────┘ └────────────┘  │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
│                             │                                       │
│  ┌──────────┐  ┌────────────▼──────┐  ┌────────────────────────┐   │
│  │ Data     │  │ RAG Pipeline      │  │ Audit Logger           │   │
│  │ Ingestion│  │ (Retrieval +      │  │ (Reasoning Trace +     │   │
│  │ Engine   │  │  Generation)      │  │  Decision Capture)     │   │
│  └────┬─────┘  └────────┬──────────┘  └───────────┬────────────┘   │
└───────┼────────────────┼──────────────────────────┼────────────────┘
        │                │                          │
┌───────▼────────────────▼──────────────────────────▼────────────────┐
│                        DATA LAYER                                   │
│                                                                     │
│  ┌──────────────┐  ┌───────────────┐  ┌────────────────────────┐   │
│  │ PostgreSQL   │  │ ChromaDB      │  │ Ollama                 │   │
│  │              │  │ (Vector DB)   │  │ (Local LLM Runtime)    │   │
│  │ • Cases      │  │               │  │                        │   │
│  │ • Txn Data   │  │ • SAR Templs  │  │ • Llama 3.1 8B         │   │
│  │ • KYC Data   │  │ • Regulatory  │  │ • Embeddings           │   │
│  │ • Audit Logs │  │   Guidelines  │  │                        │   │
│  │ • User RBAC  │  │ • Past SARs   │  │                        │   │
│  └──────────────┘  └───────────────┘  └────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Interactions

| Component | Role | Interacts With |
|-----------|------|----------------|
| **Streamlit Frontend** | Interactive UI for data upload, SAR editing, audit trail viewing, and alert management | FastAPI Backend via REST API |
| **FastAPI Backend** | Core application server — handles routing, authentication (RBAC), and orchestrates the multi-agent pipeline | Frontend, PostgreSQL, RAG Pipeline, Audit Logger |
| **Multi-Agent Pipeline** | 4 specialized LangChain agents working sequentially: (1) Data Analyst extracts patterns, (2) Compliance Mapper identifies regulatory typologies, (3) Narrator drafts the SAR, (4) QA Validator checks completeness | RAG Pipeline, Ollama LLM, Audit Logger |
| **RAG Pipeline** | Retrieves relevant regulatory templates, past SAR examples, and typology references from ChromaDB to ground LLM generation in factual context | ChromaDB, Ollama |
| **Audit Logger** | Captures every step of the generation process — input data, prompts, retrieved context, LLM responses, and reasoning rationale — using LangChain callback handlers | PostgreSQL (storage), Frontend (display) |
| **Data Ingestion Engine** | Parses uploaded CSV/JSON files, normalizes transaction and KYC data, and stores in PostgreSQL | PostgreSQL |
| **PostgreSQL** | Relational database storing case data, transactions, customer profiles, audit trail logs, and user access roles | Backend, Audit Logger |
| **ChromaDB** | Vector database storing embedded regulatory documents, SAR templates, and typology references for semantic retrieval | RAG Pipeline |
| **Ollama (Llama 3.1 8B)** | Local LLM inference engine — generates narratives, performs reasoning, and produces structured outputs. Runs entirely on-premise ensuring zero data exfiltration | Multi-Agent Pipeline, RAG Pipeline |
| **Typology Classifier (XGBoost)** | ML model trained on SAML-D dataset (17 suspicious typologies) — classifies transaction patterns and feeds context to the Narrator Agent | Data Analyst Agent, Narrator Agent |

### 2.3 Data Flow

1. **Ingestion:** Analyst uploads transaction alerts + KYC data → Data Ingestion Engine parses, normalizes, stores in PostgreSQL
2. **Analysis:** Data Analyst Agent summarizes patterns; Typology Classifier predicts suspicious category (e.g., structuring, smurfing)
3. **Retrieval:** RAG Pipeline queries ChromaDB for relevant FinCEN templates, regulatory guidelines, and similar past SARs
4. **Generation:** Narrator Agent generates FinCEN-compliant narrative (Introduction → Body [5Ws+How] → Conclusion) using retrieved context
5. **Validation:** QA Agent scores the narrative on completeness, compliance, readability, and evidence linkage
6. **Audit Logging:** Every step (1–5) is logged with full reasoning trace in PostgreSQL
7. **Human Review:** Analyst reviews draft in the SAR Editor, makes edits (tracked via diff), approves/rejects
8. **Export:** Finalized SAR exported as PDF with audit trail attached

---

## 3. Methodology / Proposed System

### 3.1 Core Methodology

Our solution employs a **Retrieval-Augmented Generation (RAG)** approach combined with a **Multi-Agent Architecture** to produce high-quality, defensible SAR narratives.

**Why Multi-Agent over Single-Prompt?**
A single LLM call for SAR generation produces inconsistent results — it conflates data analysis, regulatory mapping, and narrative writing into one step. Our multi-agent approach separates concerns:

| Agent | Responsibility | Output |
|-------|---------------|--------|
| **Data Analyst** | Extracts transaction patterns, anomalies, velocity metrics, counterparty links | Structured Data Summary JSON |
| **Compliance Mapper** | Maps findings to FinCEN typologies, identifies applicable regulations | Typology Classification + Regulatory References |
| **Narrator** | Drafts SAR narrative in FinCEN format using data summary + regulatory context + RAG-retrieved templates | Draft SAR Narrative (Introduction → Body → Conclusion) |
| **QA Validator** | Checks: all 5Ws covered? Format compliant? Claims backed by data? Readability score? | Quality Score + Improvement Suggestions |

**RAG Knowledge Base Contents:**
- FinCEN SAR narrative guidelines and advisory documents
- RBI AML/CFT master directions
- SAR narrative templates per typology (structuring, layering, smurfing, etc.)
- AML typology reference library
- Sample SAR narratives for few-shot learning

### 3.2 Scalability

| Aspect | Approach |
|--------|----------|
| **Horizontal Scaling** | Stateless FastAPI instances behind a load balancer; any instance can process any request against shared PostgreSQL + ChromaDB |
| **Batch Processing** | Upload multiple alerts → generate multiple SARs in parallel using async task queue (Celery/Redis optional) |
| **LLM Scaling** | Ollama supports multiple concurrent inference requests; can add GPU nodes for higher throughput |
| **Database Scaling** | PostgreSQL read replicas for audit trail queries; ChromaDB supports sharded collections |
| **Container Orchestration** | Docker Compose for local; Kubernetes-ready for production deployment |
| **Multi-Instance Design** | PS requirement met — multiple tool instances can run against the same data source simultaneously |

**Capacity Estimate:**
- Single instance (RTX 3060 GPU): ~4–6 SAR narratives/hour
- 3 parallel instances: ~12–18 SARs/hour
- With GPU cluster (4× A100): ~50+ SARs/hour

### 3.3 Performance

| Metric | Target | How Achieved |
|--------|--------|--------------|
| SAR generation time | < 3 minutes per report | Llama 3.1 8B quantized (Q4) for fast inference; pre-cached ChromaDB embeddings |
| First response time | < 5 seconds | Streaming LLM output; async API endpoints |
| Data ingestion | < 10 seconds for 10K transactions | Batch PostgreSQL inserts with COPY command |
| Audit trail query | < 500ms | PostgreSQL indexed on SAR ID + timestamps |
| UI responsiveness | < 200ms interaction | Streamlit with cached computations |

**Optimization Techniques:**
- **Model quantization:** Llama 3.1 8B in Q4_K_M format (~5GB VRAM)
- **Embedding caching:** Regulatory documents embedded once, persisted in ChromaDB
- **Prompt caching:** Similar alert types reuse cached prompt templates
- **Streaming output:** LLM tokens streamed to UI in real-time for perceived speed

### 3.4 Security

| Threat | Control | Implementation |
|--------|---------|---------------|
| **Data leakage across domains** | Domain isolation | Separate PostgreSQL schemas for customer, transaction, fraud data — enforced at ORM level |
| **Unauthorized access** | RBAC | Role-based access: Analyst (view/edit own cases), Reviewer (approve), Admin (all access) — JWT-based auth |
| **Data exfiltration via LLM** | Local inference only | Ollama runs 100% on-premise; no data sent to external APIs |
| **LLM output bias** | Guardrailed system prompts | System prompt explicitly instructs: unbiased, factual-only, on-topic, no discriminatory language |
| **LLM scope creep** | Output constraints | LLM outputs limited to SAR-related content only; off-topic prompts rejected via classifier |
| **PII in audit logs** | Data masking | Customer PII redacted/masked in audit trail entries |
| **Tamper-proof audit** | Immutable logging | Audit trail records are INSERT-only; no UPDATE/DELETE permissions on audit tables |
| **Session security** | Ephemeral data handling | Raw uploaded data purged after processing; only structured summaries persisted |

### 3.5 Audit Trail Implementation

The audit trail — the most critical differentiator — is implemented as a multi-layer logging system:

**Layer 1: LangChain Callback Tracing**
Every LLM call triggers callbacks that capture:
```json
{
  "step_id": "uuid",
  "agent": "narrator",
  "timestamp": "2026-02-16T10:34:21Z",
  "input_data": { "transaction_summary": "...", "typology": "structuring" },
  "prompt_sent": "Given the following transaction data...",
  "context_retrieved": [
    { "source": "FinCEN Advisory FIN-2024-A003", "relevance_score": 0.94 },
    { "source": "SAR Template T-005 (Structuring)", "relevance_score": 0.91 }
  ],
  "llm_response": "This SAR is being filed to report...",
  "reasoning": {
    "data_points_used": ["47 inbound transfers", "₹50L total", "7-day window"],
    "rules_matched": ["Structuring: multiple sub-threshold transfers"],
    "language_rationale": "Used 'rapid succession' because transfers within 72hrs"
  },
  "confidence_score": 0.92
}
```

**Layer 2: Decision Provenance**
Each sentence in the generated narrative is linked back to:
- Source data points that justified it
- Regulatory rules/patterns it references
- Alternative phrasings considered and why the chosen one was selected

**Layer 3: Human Edit Tracking**
- Full diff between AI draft and analyst-modified version
- Timestamp and user ID for every edit
- Approval chain: Draft → Reviewed → Approved → Finalized

---

## 4. Tech Stack

### 4.1 Core Stack

| Layer | Technology | Version | Purpose | Link |
|-------|-----------|---------|---------|------|
| **LLM** | Llama 3.1 8B Instruct | 3.1 | Primary narrative generation engine | [HuggingFace](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) |
| **LLM Runtime** | Ollama | Latest | Local LLM inference server | [ollama.com](https://ollama.com/) |
| **Orchestration** | LangChain | 0.3.x | Multi-agent pipeline, RAG chain, callback hooks | [langchain.com](https://www.langchain.com/) |
| **Vector DB** | ChromaDB | 0.5.x | Semantic storage for regulatory templates & past SARs | [trychroma.com](https://www.trychroma.com/) |
| **Database** | PostgreSQL | 16 | Case data, transactions, KYC, audit logs, RBAC | [postgresql.org](https://www.postgresql.org/) |
| **Backend** | FastAPI | 0.115.x | REST API server with async support | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| **Frontend** | Streamlit | 1.41.x | Interactive dashboard, SAR editor, audit viewer | [streamlit.io](https://streamlit.io/) |
| **ML Classifier** | XGBoost | 2.1.x | Typology auto-classification (17 suspicious patterns) | [GitHub](https://github.com/dmlc/xgboost) |
| **Explainability** | SHAP | 0.46.x | Feature attribution for ML model decisions | [GitHub](https://github.com/slundberg/shap) |
| **Containerization** | Docker + Docker Compose | Latest | Reproducible deployment, service orchestration | [docker.com](https://www.docker.com/) |

### 4.2 Supporting Libraries

| Library | Purpose |
|---------|---------|
| SQLAlchemy | ORM for PostgreSQL interactions |
| Pydantic | Data validation and structured LLM output parsing |
| NetworkX | Transaction flow network graphs |
| Matplotlib/Plotly | Data visualizations and risk heatmaps |
| ReportLab / FPDF | PDF export of finalized SAR narratives |
| Pandas | Data manipulation and analysis |
| scikit-learn | Feature engineering for ML classifier |

### 4.3 Datasets Used

| Dataset | Size | Purpose | Link |
|---------|------|---------|------|
| IBM AMLSim | ~1M transactions | Synthetic AML transactions with labeled laundering patterns | [Kaggle](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) |
| SAML-D | 9.5M transactions, 28 typologies | ML training data for typology classifier (17 suspicious + 11 normal patterns) | [Kaggle](https://www.kaggle.com/datasets/berkanoztas/anti-money-laundering-transaction-data-saml-d) |
| PaySim | 6.3M transactions | Synthetic mobile money fraud simulation | [Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1) |
| OpenSanctions | 325 global sources | Sanctions lists & PEP matching for entity screening | [opensanctions.org](https://www.opensanctions.org/) |
| FinCEN SAR Stats | Aggregate data | SAR filing statistics for validation/benchmarking | [Data.gov](https://catalog.data.gov/dataset/suspicious-activity-report-statistics-sar-stats) |

### 4.4 Regulatory References

| Document | Source |
|----------|--------|
| FinCEN SAR Narrative Guidance | [fincen.gov](https://www.fincen.gov/resources/statutes-and-regulations/guidance/suspicious-activity-report-narrative) |
| FinCEN SAR Filing Instructions | [fincen.gov](https://www.fincen.gov/resources/filing-information) |
| FFIEC BSA/AML Examination Manual | [ffiec.gov](https://bsaaml.ffiec.gov/manual) |
| RBI Master Direction on KYC/AML | [rbi.org.in](https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566) |

---

## 5. Future Scope

### 5.1 Short-Term Enhancements (1–3 Months)

| Feature | Description | Impact |
|---------|-------------|--------|
| **Fine-Tuned Domain LLM** | Fine-tune Llama 3.1 on anonymized real SAR narratives using LoRA/QLoRA for higher quality output | 30–50% improvement in first-draft acceptance rate |
| **Case Management Integration** | REST API connectors for Actimize, SAS AML, Oracle Financial Crime — ingest alerts directly from existing tools | Zero-copy workflow; no manual data upload |
| **Real-Time Transaction Monitoring** | Stream processing pipeline (Kafka + Flink) for live transaction analysis and proactive alert generation | Shift from reactive to proactive SAR filing |
| **Multi-Language SAR Generation** | Support Hindi, Tamil, and other regional languages for Indian regulatory submissions (RBI/FIU-IND) | Accessibility for regional banking institutions |

### 5.2 Medium-Term Vision (3–6 Months)

| Feature | Description | Impact |
|---------|-------------|--------|
| **Cross-Institution Federated Learning** | Privacy-preserving collaborative model training across banks without sharing raw data | Better pattern detection across the financial ecosystem |
| **Automated Regulatory Update Ingestion** | Web scraper + RAG updater that auto-fetches new FinCEN advisories, RBI circulars, and FATF guidance | Knowledge base always current without manual updates |
| **Advanced Network Analysis** | Graph neural networks (GNNs) for identifying complex multi-hop laundering networks across institutions | Uncovers sophisticated crime rings invisible to single-case analysis |
| **Voice-to-SAR Interface** | Analyst dictates observations, AI converts speech to structured SAR narrative sections | Hands-free drafting for field investigators |

### 5.3 Long-Term Vision (6–12 Months)

| Feature | Description |
|---------|-------------|
| **Predictive SAR Filing** | AI predicts which accounts will likely require SAR filing before manual triggers |
| **Regulatory Response Simulator** | Simulates how regulators might interpret a SAR narrative and suggests improvements |
| **Global Compliance Adapter** | One system adaptable to FinCEN (US), FCA (UK), FIU-IND (India), AUSTRAC (Australia) formats |
| **Autonomous SAR Quality Assurance** | AI reviewer that matches quality of experienced compliance officers before human review |

---

## 6. Other Comments on Solution

### 6.1 Key Differentiators

1. **Zero Data Exfiltration:** Unlike cloud-based LLM solutions (OpenAI, Claude), our system runs Llama 3.1 entirely locally via Ollama. Customer data, transaction records, and SAR narratives never leave the organization's infrastructure.

2. **Full Audit Defensibility:** Every AI-generated sentence is traceable to source data, matched rules, and retrieved regulatory context. This directly addresses the FinCEN requirement that AI-assisted SARs must be explainable and defensible.

3. **Zero Vendor Lock-In:** 100% open-source stack with no proprietary dependencies. Any component (LLM, vector DB, database) can be swapped without architectural changes. The environment-aware configuration supports local, cloud, and hybrid deployments.

4. **Cost Efficiency:** Total operational cost of ₹0–₹1,000 vs. commercial SAR automation tools costing $50K–$500K/year. The entire solution runs on consumer-grade hardware (RTX 3060+ or M1/M2 Mac).

5. **Human-in-the-Loop by Design:** The system deliberately does not fully automate SAR filing. It positions AI as an analyst's assistant — generating drafts, providing reasoning, and scoring quality — while keeping human judgment as the final authority.

### 6.2 Compliance with PS Design Considerations

| PS Requirement | Our Implementation | Status |
|---------------|-------------------|--------|
| Output: Draft SAR with human edit/approve | SAR Editor with diff tracking + approval workflow | ✅ |
| Alerting Mechanism | Rule-based triggers + LLM anomaly scoring + severity dashboard | ✅ |
| Interactive UI for prompt input | Streamlit dashboard with data upload and parameter controls | ✅ |
| Horizontal Scalability | Stateless API + Docker instances + shared data sources | ✅ |
| Unbiased LLM via system prompt | Explicit guardrails in system prompt; output scope limited to SAR topics | ✅ |
| Environment-Aware (on-prem/cloud/hybrid) | Config-based deployment switch: Ollama (local) ↔ Bedrock (cloud) | ✅ |
| No cross-domain data leakage | Separate PostgreSQL schemas + ORM-level enforcement | ✅ |
| Role-Based Access Controls | JWT-based RBAC: Analyst / Reviewer / Admin roles | ✅ |
| Complete Audit Trail | 3-layer logging: LangChain callbacks + decision provenance + edit tracking | ✅ |

### 6.3 Demo Scenario

**Real-World Example (from PS):** A customer receives ₹50 lakhs from 47 different accounts in one week, then immediately transfers it abroad.

Our system will:
1. Ingest the 47 transaction records + customer KYC data
2. Data Analyst Agent identifies: 47 unique senders, ₹50L total, 7-day window, immediate outbound transfer
3. Typology Classifier predicts: **Structuring/Smurfing** (confidence: 92%)
4. RAG retrieves: FinCEN Advisory on structuring, SAR Template T-005
5. Narrator Agent generates a 2-page SAR narrative covering all 5Ws + How
6. QA Agent scores: Completeness 95%, Compliance 98%, Readability 88%
7. Analyst reviews, makes minor edits, approves
8. Full audit trail available showing every decision in the pipeline

---

*Document prepared for Hack-O-Hire 2026 submission.*
