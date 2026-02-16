# 🏁 SAR Narrative Generator — Round 1 TODO

> **Goal:** Submit Abstract + Semi-Working Prototype with Screenshots  
> **Deadline:** Feb 17, 2026 — 11:59 PM IST  
> **Team:** 5 Members | **Legend:** `[ ]` Todo · `[/]` In Progress · `[x]` Done

---

## 📂 File Ownership Map (Zero Conflict Guarantee)

Each person works in **completely separate directories/files**. No two people touch the same file.

```
Hack-O-Hire/
├── backend/
│   ├── app/
│   │   ├── main.py                ← P1 ONLY
│   │   ├── api/
│   │   │   ├── routes.py          ← P1 ONLY
│   │   │   └── schemas.py         ← P1 ONLY
│   │   ├── core/
│   │   │   ├── rag_pipeline.py    ← P2 ONLY
│   │   │   ├── llm_engine.py      ← P2 ONLY
│   │   │   └── audit_logger.py    ← P2 ONLY
│   │   └── utils/
│   │       └── data_parser.py     ← P4 ONLY
│   ├── knowledge_base/            ← P2 ONLY
│   └── requirements.txt           ← P1 ONLY (others tell P1 what to add)
├── frontend/
│   ├── app.py                     ← P3 ONLY
│   ├── pages/
│   │   ├── dashboard.py           ← P3 ONLY
│   │   ├── sar_editor.py          ← P3 ONLY
│   │   └── audit_trail.py         ← P3 ONLY
│   └── components/                ← P3 ONLY
├── ml_models/
│   └── typology_classifier.py     ← P4 ONLY
├── data/
│   └── sample_data/               ← P4 ONLY
├── screenshots/                   ← P5 ONLY
├── TeamName_CampusName_160226.md  ← P5 ONLY
├── SAR_PPT_DATA.md                ← P5 ONLY
├── docker-compose.yml             ← P1 ONLY
└── README.md                      ← P5 ONLY
```

---

## Phase 1: Setup & Skeleton (First 2 Hours — All Parallel)

> Everyone sets up their environment + creates their file skeletons.  
> **Sync Point:** Quick 5-min call after Phase 1 to confirm all skeletons are in place.

### P1 — Backend Lead
- [ ] Create project folder structure (`backend/app/`, `api/`, `core/`, `utils/`)
- [ ] Set up Python venv, create `requirements.txt` with: `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `python-multipart`
- [ ] Create `docker-compose.yml` with PostgreSQL service
- [ ] Create `main.py` — FastAPI app with CORS, basic health check endpoint
- [ ] Create `schemas.py` — Pydantic models for: `TransactionAlert`, `CustomerKYC`, `SARNarrative`, `AuditEntry`
- [ ] Create stub `routes.py` with endpoint signatures (return dummy data for now):
  - `POST /api/upload` — accept CSV/JSON upload
  - `POST /api/generate-sar` — trigger SAR generation
  - `GET /api/sar/{id}` — get SAR + audit trail
  - `PUT /api/sar/{id}` — update SAR
  - `POST /api/sar/{id}/approve` — approve SAR

### P2 — LLM/RAG Engineer
- [ ] Install Ollama, pull `llama3.1:8b` model
- [ ] Create `llm_engine.py` — wrapper class to call Ollama with system prompt
- [ ] Create `rag_pipeline.py` — skeleton with ChromaDB setup + LangChain retrieval chain
- [ ] Create `audit_logger.py` — LangChain callback handler that captures: input → prompt → context → output → reasoning
- [ ] Create `knowledge_base/` folder with:
  - [ ] `sar_templates/` — 3 sample SAR narrative templates (structuring, smurfing, layering)
  - [ ] `regulations/` — Copy-paste key FinCEN guidelines into text files
- [ ] Test: Ollama responds to a basic prompt

### P3 — Frontend Lead
- [ ] Create `frontend/app.py` — Streamlit multipage app skeleton
- [ ] Create `pages/dashboard.py` — layout with sidebar nav, placeholder cards
- [ ] Create `pages/sar_editor.py` — split-screen layout (data left, editor right)
- [ ] Create `pages/audit_trail.py` — expandable timeline layout
- [ ] Set up Streamlit theming (dark mode, custom colors)
- [ ] Add placeholder/mock data so each page renders something visual

### P4 — Data & ML Engineer
- [ ] Download SAML-D dataset from Kaggle (or a subset ~50K rows)
- [ ] Download IBM AMLSim sample from Kaggle
- [ ] Create `data/sample_data/` with 3 curated demo scenarios:
  - `scenario_smurfing.csv` — 47 senders, 1 receiver, ₹50L total
  - `scenario_layering.csv` — shell company round-tripping
  - `scenario_structuring.csv` — sub-threshold deposits
- [ ] Create `data_parser.py` — reads CSV/JSON, returns normalized `TransactionAlert` objects
- [ ] Create `typology_classifier.py` — skeleton: load data, feature engineering stubs
- [ ] Begin training XGBoost on SAML-D (can run overnight if needed)

### P5 — Docs & Submission Lead
- [ ] Finalize `TeamName_CampusName_160226.md` — replace placeholders (team name, campus, member names)
- [ ] Review & polish Abstract (keep 100-200 words)
- [ ] Set up `screenshots/` folder
- [ ] Start preparing PPT structure (from `SAR_PPT_DATA.md`)
- [ ] Create `README.md` with project overview + setup instructions
- [ ] Research competitor SAR tools for "why we're better" slide

---

## Phase 2: Core Working Prototype (Next 4 Hours — All Parallel)

> Each person builds their working component independently.  
> **Contract:** Everyone exposes/consumes data via **JSON dict** format — no cross-imports.  
> **Sync Point:** Quick call after Phase 2 to test connections.

### P1 — Backend: Wire Up Real API
- [ ] Implement `POST /api/upload` — parse uploaded CSV, store in PostgreSQL (or in-memory dict for prototype)
- [ ] Implement `POST /api/generate-sar` — call P2's `llm_engine` module, return result
- [ ] Implement `GET /api/sar/{id}` — return stored SAR + audit trail
- [ ] Implement `PUT /api/sar/{id}` — accept edited narrative, track diff
- [ ] Implement `POST /api/sar/{id}/approve` — change status to approved
- [ ] Add simple in-memory storage (dict) as DB fallback if PostgreSQL isn't ready
- [ ] Test all endpoints with `curl` or Postman

### P2 — LLM/RAG: Working Narrative Generation
- [ ] Build full system prompt for SAR generation:
  - Instruct FinCEN format (Introduction → Body → Conclusion)
  - Include 5Ws + How structure
  - Add unbiased/on-topic guardrails
- [ ] Index knowledge base documents into ChromaDB
- [ ] Build RAG chain: query → retrieve templates → augment prompt → generate
- [ ] Implement audit logger callback: capture full trace per generation
- [ ] Create a `generate_sar(alert_data: dict) -> dict` function that returns:
  ```python
  {
    "narrative": "...",      # The SAR text
    "audit_trail": [...],    # List of reasoning steps
    "quality_score": 0.85,   # Basic completeness check
    "typology": "structuring" # Detected pattern
  }
  ```
- [ ] Test: Feed scenario_smurfing.csv → get a real SAR narrative out

### P3 — Frontend: Working UI Pages
- [ ] **Dashboard:** Show list of uploaded cases with status badges (Draft/Review/Approved)
- [ ] **Upload page:** File uploader → show parsed data in table
- [ ] **SAR Editor:**
  - Left panel: show transaction data summary + risk highlights
  - Right panel: editable text area with generated narrative
  - Buttons: Regenerate, Approve, Export
- [ ] **Audit Trail page:**
  - Expandable cards showing each reasoning step
  - Color-coded: data points (blue), rules (orange), rationale (green)
- [ ] Wire up to backend API (use `requests` to call FastAPI endpoints)
- [ ] If backend not ready, use **mock JSON responses** so UI is fully demo-able

### P4 — ML: Working Classifier + Data Pipeline
- [ ] Complete XGBoost training on SAML-D dataset features:
  - Transaction amount, frequency, num counterparties, time gaps, amount variance
- [ ] Save trained model as `.joblib` file
- [ ] Create `predict_typology(transactions: list) -> dict` function:
  ```python
  {
    "typology": "structuring",
    "confidence": 0.92,
    "features_importance": {"amount": 0.35, "frequency": 0.28, ...}
  }
  ```
- [ ] Create SHAP explanation for top features
- [ ] Wire `data_parser.py` to produce clean input for both P1's API and P2's LLM engine
- [ ] Generate risk scores for demo scenarios

### P5 — Screenshots & Submission Polish
- [ ] Take screenshots of P3's UI (even with mock data — it's fine)
- [ ] Take screenshot of P2's generated SAR narrative (terminal output is fine)
- [ ] Take screenshot of audit trail output
- [ ] Add screenshots to submission document under architecture/methodology sections
- [ ] Polish submission doc: add performance claims, accuracy numbers from P4's classifier
- [ ] Start building PPT slides (Google Slides / PowerPoint)

---

## Phase 3: Integration & Demo-Ready (Final 3 Hours)

> **This is the ONLY phase where people touch shared integration points.**  
> P1 leads integration; others provide their modules.

### P1 — Integration Captain
- [ ] Integrate P2's `generate_sar()` function into `POST /api/generate-sar` route
- [ ] Integrate P4's `predict_typology()` into the generation pipeline
- [ ] Ensure audit trail flows from P2 → PostgreSQL → API → Frontend
- [ ] Test full end-to-end: Upload CSV → Generate SAR → View Audit → Edit → Approve
- [ ] Fix any bugs in API contracts

### P2 — LLM Quality Tuning
- [ ] Improve prompt based on initial outputs (make narrative more professional)
- [ ] Add quality scoring logic (completeness check: are all 5Ws present?)
- [ ] Test with all 3 demo scenarios — ensure each produces good output
- [ ] Fine-tune audit trail formatting for clean display

### P3 — Frontend Polish + Screenshots
- [ ] Connect to live backend (replace mocks with real API calls)
- [ ] Add loading spinners during SAR generation
- [ ] Polish dark mode styling
- [ ] Take **final screenshots** of working prototype for submission
- [ ] Record screen GIF/video if time permits

### P4 — Final Model + Demo Data
- [ ] Verify classifier accuracy on test set (aim for >80%)
- [ ] Generate prediction results for all 3 demo scenarios
- [ ] Create summary stats for submission doc (accuracy, F1, precision)
- [ ] Ensure data_parser handles edge cases in demo CSVs

### P5 — Final Submission Assembly
- [ ] Update submission doc with final screenshots
- [ ] Add classifier accuracy metrics to methodology section
- [ ] Add SAR narrative sample output to the document
- [ ] Final proofread of Abstract (100-200 words, crisp)
- [ ] Convert markdown → `.doc` format
- [ ] Build final PPT (from `SAR_PPT_DATA.md`)
- [ ] Rename files: `TeamName_CampusName_170226.doc` / `.ppt`
- [ ] Verify total size < 45 MB
- [ ] **SUBMIT** 🎉

---

## ⏰ Timeline (Clock-based for Feb 16–17)

| Time | Phase | Status |
|------|-------|--------|
| **8:00 PM – 10:00 PM** (Feb 16) | Phase 1: Setup & Skeleton | All parallel |
| 10:00 PM | ⚡ **Sync call** (5 min) | Confirm skeletons work |
| **10:00 PM – 2:00 AM** (Feb 16–17) | Phase 2: Core Prototype | All parallel |
| 2:00 AM | ⚡ **Sync call** (10 min) | Test API connections |
| **2:00 AM – 5:00 AM** (Feb 17) | Phase 3: Integration & Polish | P1 leads integration |
| **5:00 AM – 8:00 AM** | Sleep / Break 💤 | |
| **8:00 AM – 12:00 PM** | Final polish + Submission prep | P5 leads |
| **12:00 PM – 11:59 PM** | Buffer + Submit | |

---

## 🤝 Integration Contracts (How Modules Connect)

> These are the **agreed JSON shapes** that each person's code must produce/consume.  
> As long as everyone follows these, code will plug together with zero conflicts.

### Contract 1: P4 → P1 (Data Parser → API)
```json
// P4's data_parser.parse_csv(file) returns:
{
  "case_id": "CASE-001",
  "transactions": [
    {
      "txn_id": "TXN-001",
      "sender": "Account-A",
      "receiver": "Account-B",
      "amount": 500000,
      "currency": "INR",
      "timestamp": "2026-01-15T10:30:00",
      "type": "NEFT"
    }
  ],
  "customer": {
    "name": "Rajesh Kumar",
    "account_id": "XXXX-4521",
    "kyc_status": "verified",
    "business_type": "Textile Export",
    "avg_monthly_volume": 300000
  }
}
```

### Contract 2: P1 → P2 (API → LLM Engine)
```json
// P1 calls: P2.generate_sar(case_data)
// Input: the parsed case data from Contract 1
// Output:
{
  "sar_id": "SAR-001",
  "narrative": {
    "introduction": "This SAR is being filed to report...",
    "body": "WHO: ... WHAT: ... WHEN: ... WHERE: ... WHY: ... HOW: ...",
    "conclusion": "Based on the above analysis..."
  },
  "audit_trail": [
    {
      "step": 1,
      "agent": "data_analyst",
      "action": "Analyzed 47 inbound transactions",
      "data_points_used": ["47 senders", "₹50L total", "7-day window"],
      "output": "High-risk pattern: multiple small transfers consolidated"
    },
    {
      "step": 2,
      "agent": "compliance_mapper",
      "action": "Matched to FinCEN typology",
      "rules_matched": ["Structuring", "Smurfing"],
      "output": "Primary typology: Structuring (confidence: 92%)"
    }
  ],
  "quality_score": {
    "completeness": 0.95,
    "compliance": 0.98,
    "readability": 0.88,
    "evidence_linkage": 0.91
  },
  "typology": {
    "prediction": "structuring",
    "confidence": 0.92
  },
  "status": "draft"
}
```

### Contract 3: P1 → P3 (API → Frontend)
```json
// P3 calls GET /api/sar/{id} and receives the same structure as Contract 2
// P3 calls GET /api/cases and receives:
{
  "cases": [
    {
      "case_id": "CASE-001",
      "customer_name": "Rajesh Kumar",
      "alert_type": "High Volume Inbound",
      "risk_level": "HIGH",
      "sar_status": "draft",
      "created_at": "2026-02-17T10:30:00"
    }
  ]
}
```

### Contract 4: P4 → P2 (ML Model → LLM Engine)
```json
// P2 calls: P4.predict_typology(transactions)
// Output:
{
  "typology": "structuring",
  "confidence": 0.92,
  "top_features": {
    "num_unique_senders": 0.35,
    "total_amount": 0.28,
    "time_window_days": 0.22,
    "amount_variance": 0.15
  }
}
```

---

## 🎯 Round 1 Submission Checklist

- [ ] Abstract document (100-200 words) ✓
- [ ] System Architecture diagram with component descriptions ✓
- [ ] Methodology section (scalability, performance, security) ✓
- [ ] Tech stack listing ✓
- [ ] Future scope ✓
- [ ] Screenshots of working prototype (minimum 3):
  - [ ] Dashboard / upload screen
  - [ ] Generated SAR narrative
  - [ ] Audit trail view
- [ ] Semi-working prototype running locally
- [ ] ML model trained with accuracy metrics
- [ ] File named: `TeamName_CampusName_170226.doc`
- [ ] PPT named: `TeamName_CampusName_170226.ppt`
- [ ] Total size < 45 MB
