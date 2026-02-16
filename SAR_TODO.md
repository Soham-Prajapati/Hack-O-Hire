# 📋 SAR Narrative Generator — Phased TODO

> **Timeline:** 2 Days | **Team:** 5 Members  
> **Legend:** `[ ]` Todo · `[/]` In Progress · `[x]` Done

---

## Phase 1: Foundation & Setup (Day 1 — First 4 Hours)

**Owner(s): All 5 members — parallel setup**

- [ ] **Environment Setup**
  - [ ] Create project repo structure (see folder plan in `SAR_PROJECT_PLAN.md`)
  - [ ] Set up Python virtual environment (`python 3.11+`)
  - [ ] Install core dependencies: `langchain`, `chromadb`, `streamlit`, `fastapi`, `sqlalchemy`, `ollama`
  - [ ] Install Ollama and pull `llama3.1:8b` model
  - [ ] Set up PostgreSQL via Docker (`docker-compose.yml`)
  - [ ] Create `requirements.txt` / `pyproject.toml`

- [ ] **Data Preparation**
  - [ ] Download IBM AMLSim dataset from Kaggle
  - [ ] Download SAML-D dataset from Kaggle
  - [ ] Create sample demo data (5–10 mock transaction alerts with customer KYC)
  - [ ] Write data parser module (`data_parser.py`) — CSV/JSON → normalized format
  - [ ] Define database schema (cases, transactions, customers, audit_logs tables)

- [ ] **Knowledge Base Setup**
  - [ ] Collect & save FinCEN SAR narrative guidelines (PDF/text)
  - [ ] Create 3–5 SAR narrative templates (structuring, smurfing, layering typologies)
  - [ ] Collect AML typology reference documents
  - [ ] Index all documents into ChromaDB using LangChain document loader

---

## Phase 2: Core Engine (Day 1 — Hours 4–10)

**Owner(s): 2 members on backend, 1 member on RAG, 2 on frontend start**

- [ ] **RAG Pipeline (`rag_pipeline.py`)**
  - [ ] Set up LangChain with Ollama as LLM backend
  - [ ] Configure ChromaDB as vector store with embedding model
  - [ ] Implement document retrieval chain (regulatory templates → relevant context)
  - [ ] Build prompt template following FinCEN 5Ws + How structure
  - [ ] Test: Given sample alert data → retrieve relevant templates → generate narrative

- [ ] **SAR Narrative Generator (`llm_engine.py`)**
  - [ ] Create system prompt for SAR generation (unbiased, on-topic, structured)
  - [ ] Build narrative generation chain: Data Summary → Context Retrieval → Narrative Draft
  - [ ] Implement FinCEN format output: Introduction → Body (5Ws) → Conclusion
  - [ ] Add structured output parsing (Pydantic models for SAR sections)

- [ ] **Audit Trail Logger (`audit_logger.py`)**
  - [ ] Implement LangChain callback handler for tracing
  - [ ] Log every step: input_data → prompt_sent → context_retrieved → llm_response → reasoning
  - [ ] Store audit entries in PostgreSQL with timestamps & session IDs
  - [ ] Create reasoning trace format: `{ data_points, rules_matched, language_rationale }`

- [ ] **FastAPI Backend (`main.py`, `routes.py`)**
  - [ ] POST `/api/upload` — Upload transaction/customer data
  - [ ] POST `/api/generate-sar` — Trigger SAR narrative generation
  - [ ] GET `/api/sar/{id}` — Get SAR narrative + audit trail
  - [ ] PUT `/api/sar/{id}` — Update/edit SAR narrative
  - [ ] POST `/api/sar/{id}/approve` — Approve SAR
  - [ ] GET `/api/audit/{sar_id}` — Get full audit trail for a SAR

---

## Phase 3: Frontend & Visualization (Day 1 Evening + Day 2 Morning — ~6 Hours)

**Owner(s): 2 members on frontend, 1 member on integrations**

- [ ] **Main Dashboard (`dashboard.py`)**
  - [ ] Case overview cards (total cases, pending reviews, approved SARs)
  - [ ] Alert priority list (High/Medium/Low risk)
  - [ ] Quick stats: avg generation time, approval rate
  - [ ] Navigation sidebar

- [ ] **SAR Editor Page (`sar_editor.py`)**
  - [ ] Split-screen: Data Points (left) | Narrative Draft (right)
  - [ ] Editable text area for analyst modifications
  - [ ] Highlight AI-generated vs human-edited sections
  - [ ] Approve / Reject / Send Back buttons
  - [ ] Export to PDF button

- [ ] **Audit Trail Viewer (`audit_trail.py`)**
  - [ ] Timeline view of LLM reasoning steps
  - [ ] Expandable cards per decision point
  - [ ] Show: which data influenced each narrative section
  - [ ] Color-coded: data points (blue), rules matched (orange), language choices (green)

- [ ] **Alert Management (`alerts.py`)**
  - [ ] Alert creation from uploaded data
  - [ ] Risk scoring display (rule-based + ML score)
  - [ ] Filter by severity, date, typology
  - [ ] One-click "Generate SAR" from alert

- [ ] **Visualizations**
  - [ ] Transaction flow network graph (NetworkX + Streamlit)
  - [ ] Risk heatmap visualization
  - [ ] Data distribution charts for uploaded alerts

---

## Phase 4: USP Features (Day 2 — Hours 4–8)

**Owner(s): Split across team based on strength**

- [ ] **Multi-Agent Pipeline**
  - [ ] Data Analyst Agent — summarizes transaction patterns
  - [ ] Compliance Agent — maps to regulatory typologies
  - [ ] Narrator Agent — writes SAR narrative
  - [ ] QA Agent — validates completeness & quality
  - [ ] Chain all 4 agents using LangChain sequential chain

- [ ] **Typology Auto-Classifier**
  - [ ] Train XGBoost on SAML-D dataset (17 suspicious typologies)
  - [ ] Feature engineering: amount, frequency, counterparties, time patterns
  - [ ] Integrate classifier output into narrative context
  - [ ] Show typology prediction with confidence in UI

- [ ] **SAR Quality Scorer**
  - [ ] Completeness check: are all 5Ws addressed?
  - [ ] Format compliance: FinCEN structure met?
  - [ ] Readability score (Flesch-Kincaid)
  - [ ] Evidence linkage: every claim tied to data?
  - [ ] Display score as gauge/meter in editor

- [ ] **Alerting Mechanism**
  - [ ] Define rule-based triggers (amount thresholds, velocity checks)
  - [ ] LLM-based anomaly description generation
  - [ ] Alert dashboard with severity sorting
  - [ ] Alert → SAR generation flow

---

## Phase 5: Polish, Testing & Demo Prep (Day 2 — Final 4 Hours)

**Owner(s): All members — all hands on deck**

- [ ] **Integration Testing**
  - [ ] End-to-end flow: Upload data → Generate SAR → View Audit → Edit → Approve
  - [ ] Test with 3+ different suspicious activity scenarios
  - [ ] Verify audit trail completeness
  - [ ] Test RBAC (if implemented)

- [ ] **UI/UX Polish**
  - [ ] Dark mode theme for professional look
  - [ ] Loading animations during generation
  - [ ] Error handling & user feedback messages
  - [ ] Responsive layout tweaks

- [ ] **Demo Preparation**
  - [ ] Prepare 3 demo scenarios (see examples below)
  - [ ] Pre-load sample data for smooth demo
  - [ ] Create demo script (what to show, in what order)
  - [ ] Prepare backup screenshots/recordings in case of live demo issues

- [ ] **Documentation**
  - [ ] README.md with setup instructions
  - [ ] Architecture diagram polished
  - [ ] Record 2-min demo video (optional)

- [ ] **Presentation**
  - [ ] Finalize PPT using data from `SAR_PPT_DATA.md`
  - [ ] Practice presentation (5 min target)
  - [ ] Assign presentation roles (intro, demo, tech deep-dive, Q&A)

---

## 🎯 Demo Scenarios

### Scenario 1: Smurfing / Structuring
> Customer receives ₹50 lakhs from 47 different accounts in one week, then immediately transfers abroad.

### Scenario 2: Layering
> Multiple shell company transactions with round-tripping across 3 countries within 48 hours.

### Scenario 3: Unusual Cash Patterns
> Small business account with sudden 10x increase in cash deposits, all just below reporting threshold (₹9.9L each).

---

## 👥 Suggested Team Role Allocation

| Member | Primary Role | Phases |
|--------|-------------|--------|
| **Member 1** | Backend Lead (FastAPI + DB) | Phase 1, 2, 4 |
| **Member 2** | LLM/RAG Engineer (LangChain + Ollama) | Phase 1, 2, 4 |
| **Member 3** | Frontend Lead (Streamlit UI) | Phase 1, 3, 5 |
| **Member 4** | ML Engineer (Typology + Risk Scoring) | Phase 1, 4, 5 |
| **Member 5** | Data + Integration + Presentation | Phase 1, 2, 3, 5 |
