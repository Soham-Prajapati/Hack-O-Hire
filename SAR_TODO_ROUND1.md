# 🏁 SAR Narrative Generator — Round 1 TODO

> **Goal:** Submit Abstract + Semi-Working Prototype with Screenshots/Video  
> **Deadline:** Feb 17, 2026 — 11:59 PM IST  
> **Legend:** `[ ]` Todo · `[/]` In Progress · `[x]` Done

---

## 👥 Team Roles

| Name | Role | Focus Areas |
|------|------|-------------|
| **Shubh** | Backend + AI Integration Lead | FastAPI, API routes, system integration, AI pipeline wiring |
| **Dev** | LLM/RAG + AI Core Lead | Ollama, LangChain, RAG pipeline, audit trail, prompt engineering |
| **Siddh** | Frontend Lead | Streamlit UI, dashboard, SAR editor, visualizations |
| **Het** | Data & ML Engineer | Datasets, data parsing, XGBoost classifier, SHAP |
| **Sakshi** | Docs, PPT & Submission Lead | Submission doc, PPT, screenshots, README |

---

## 📂 File Ownership Map (Zero Conflict Guarantee)

Each person works in **completely separate directories/files**. No merge conflicts.

```
Hack-O-Hire/
├── backend/
│   ├── app/
│   │   ├── main.py                ← SHUBH ONLY
│   │   ├── api/
│   │   │   ├── routes.py          ← SHUBH ONLY
│   │   │   └── schemas.py         ← SHUBH ONLY
│   │   ├── core/
│   │   │   ├── rag_pipeline.py    ← DEV ONLY
│   │   │   ├── llm_engine.py      ← DEV ONLY
│   │   │   └── audit_logger.py    ← DEV ONLY
│   │   └── utils/
│   │       └── data_parser.py     ← HET ONLY
│   ├── knowledge_base/            ← DEV ONLY
│   └── requirements.txt           ← SHUBH ONLY (others tell Shubh what to add)
├── frontend/
│   ├── app.py                     ← SIDDH ONLY
│   ├── pages/                     ← SIDDH ONLY
│   └── components/                ← SIDDH ONLY
├── ml_models/
│   └── typology_classifier.py     ← HET ONLY
├── data/
│   └── sample_data/               ← HET ONLY
├── screenshots/                   ← SAKSHI ONLY
├── TeamName_CampusName_160226.md  ← SAKSHI ONLY
├── SAR_PPT_DATA.md                ← SAKSHI ONLY
├── docker-compose.yml             ← SHUBH ONLY
└── README.md                      ← SAKSHI ONLY
```

---

## Phase 1: Setup & Skeleton ✅ (DONE — already pushed to GitHub)

> All skeleton files created and pushed. Everyone pulls `main` and runs setup.

```bash
git pull origin main
chmod +x setup.sh
./setup.sh shubh    # Replace "shubh" with your name
# See HOW_TO_RUN.md for full instructions
```

---

## Phase 2: Core Working Prototype (4 Hours — All Parallel)

> **Contract:** Everyone produces/consumes data as **JSON dicts** — no cross-file imports.  
> **Sync Point:** Quick call after Phase 2 to test connections.

### SHUBH — Backend + AI Integration
- [x] Implement `POST /api/upload` — parse uploaded CSV using Het's parser, store in memory
- [x] Implement `POST /api/generate-sar` — call Dev's `generate_sar()`, return result
- [x] Implement `GET /api/sar/{id}` — return stored SAR + audit trail
- [x] Implement `PUT /api/sar/{id}` — accept edited narrative, track diff
- [x] Implement `POST /api/sar/{id}/approve` — change status to approved
- [x] Wire up Het's `predict_typology()` into the generate pipeline
- [x] Test all endpoints with `curl` / Postman
- [x] Help Dev with any LLM integration issues

### DEV — LLM/RAG Core (AI Heavy)
- [x] Install Ollama, pull `llama3.1:8b` model (Download at ~80%)
- [x] Build full SAR generation system prompt (FinCEN format, 5Ws+How, guardrails)
- [x] Index knowledge base docs (SAR templates + FinCEN guidance) into ChromaDB
- [x] Build RAG chain: query → retrieve templates → augment prompt → generate
- [x] Implement LangChain callback handler for audit trail capture
- [x] Create `generate_sar(alert_data: dict) -> dict` returning:
  - `narrative` (intro + body + conclusion)
  - `audit_trail` (list of reasoning steps)
  - `quality_score` (completeness, compliance, readability, evidence)
- [x] Test: Feed `scenario_smurfing.csv` → get a real SAR narrative out
<<<<<<< Updated upstream
- [x] Experiment with prompt quality — iterate until narrative reads professional
=======
- [/] Experiment with prompt quality — iterate until narrative reads professional
>>>>>>> Stashed changes

### SIDDH — Frontend (Streamlit UI)
- [x] **Dashboard:** Case list with status badges (Draft/Review/Approved), metrics cards ✅
- [x] **Upload page:** File uploader → show parsed data in table ✅
- [x] **SAR Editor:** Split-screen (data left, narrative editor right), Approve/Reject/Export buttons ✅
- [x] **Audit Trail:** Expandable cards, color-coded steps ✅
- [x] **Wire up to backend API (`requests.get/post` to FastAPI) — `api_client.py` + all pages wired ✅
- [x] **IMPORTANT:** If backend not ready, use **mock JSON** so UI is fully demo-able ✅
- [x] **Add loading spinners, dark mode polish ✅

### HET — Data & ML
- [x] Download SAML-D dataset (or subset ~50K rows) from Kaggle
- [x] Create `data_parser.py` — CSV/JSON → normalized dict format
- [x] Create 2 more demo CSVs: `scenario_layering.csv`, `scenario_structuring.csv`
- [x] Train XGBoost on SAML-D features (amount, frequency, counterparties, time gaps)
- [x] Save model as `.joblib`
- [x] Implement `predict_typology(transactions) -> dict` with confidence + feature importance
- [x] Add SHAP explanations for top features

### SAKSHI — Docs & PPT
- [ ] Finalize submission doc — replace [TeamName], [CampusName], member names
- [ ] Polish Abstract (100-200 words, crisp)
- [ ] Start building PPT (use `SAR_PPT_DATA.md` content)
- [ ] Take screenshots of Siddh's UI (mock data is fine for now) — **UI is demo-ready now!**
- [ ] Research competitor SAR tools for "why we're better" slide

---

## Phase 3: Integration & Demo-Ready (3 Hours)

> **Shubh leads integration.** Others provide their modules.

### SHUBH — Integration Captain
- [x] Integrate Dev's `generate_sar()` into API route
- [x] Integrate Het's `predict_typology()` into pipeline
- [x] Test full E2E: Upload → Generate → Audit → Edit → Approve
- [x] Fix any integration bugs
- [ ] Help record demo video

### DEV — LLM Quality + Polish
- [x] Improve prompt based on initial outputs
- [x] Add quality scoring logic (are all 5Ws present?)
- [x] Test all 3 demo scenarios — ensure good output
- [x] Help Shubh with integration debugging

### SIDDH — Frontend Final + Video
- [x] Connect to live backend (replace mocks) — graceful fallback when offline ✅
- [x] Polish UI (animations, error handling) — fade-in, pulse, hover, toast ✅
- [ ] Take **final screenshots** of working prototype
- [ ] **Record demo video** (3-4 min screen recording)

### HET — Final Model + Data
- [x] Verify classifier accuracy (aim >80%) — achieved 100%
- [x] Generate predictions for all 3 demo scenarios
- [x] Create accuracy/F1/precision stats for submission doc
- [x] Ensure data parser handles all edge cases

### SAKSHI — Final Submission
- [ ] Update submission doc with final screenshots + metrics
- [ ] Add sample SAR narrative output to document
- [ ] Final proofread
- [ ] Convert to `.doc` format
- [ ] Build final PPT
- [ ] Rename: `TeamName_CampusName_170226.doc` / `.ppt`
- [ ] Verify size < 45 MB
- [ ] **SUBMIT** 🎉

---

## ⏰ Timeline

| Time | Phase | Lead |
|------|-------|------|
| **12:30 AM – 4:30 AM** (Feb 17) | Phase 2: Core Prototype | All parallel |
| 4:30 AM | ⚡ **Sync call** (10 min) | Test connections |
| **4:30 AM – 7:30 AM** | Phase 3: Integration + Polish | Shubh leads |
| **8:00 AM – 12:00 PM** | Final polish + Submission prep | Sakshi leads |
| **12:00 PM – 11:59 PM** | Buffer + Submit | |

---

## 🤝 Integration Contracts

### Het → Shubh (Data Parser → API)
```json
{
  "case_id": "CASE-001",
  "transactions": [
    { "txn_id": "TXN-001", "sender": "Account-A", "receiver": "Account-B",
      "amount": 500000, "currency": "INR", "timestamp": "2026-01-15T10:30:00", "type": "NEFT" }
  ],
  "customer": {
    "name": "Rajesh Kumar", "account_id": "XXXX-4521",
    "kyc_status": "verified", "business_type": "Textile Export", "avg_monthly_volume": 300000
  }
}
```

### Shubh → Dev (API → LLM Engine)
```json
{
  "sar_id": "SAR-001",
  "narrative": { "introduction": "...", "body": "...", "conclusion": "..." },
  "audit_trail": [
    { "step": 1, "agent": "data_analyst", "action": "...", "data_points_used": [...], "output": "..." }
  ],
  "quality_score": { "completeness": 0.95, "compliance": 0.98, "readability": 0.88, "evidence_linkage": 0.91 },
  "typology": { "prediction": "structuring", "confidence": 0.92 },
  "status": "draft"
}
```

### Het → Dev (ML Model → LLM Engine)
```json
{
  "typology": "structuring",
  "confidence": 0.92,
  "top_features": { "num_unique_senders": 0.35, "total_amount": 0.28, "time_window_days": 0.22 }
}
```

---

## 🎯 Round 1 Submission Checklist

- [x] Project skeleton pushed to GitHub ✓
- [ ] Abstract document (100-200 words)
- [ ] System Architecture + component descriptions
- [ ] Methodology (scalability, performance, security)
- [ ] Tech stack listing
- [ ] Future scope
- [ ] Screenshots of working prototype (min 3)
- [ ] Demo video (3-4 min)
- [x] Semi-working prototype (Streamlit UI with mock data) ✓
- [ ] File: `TeamName_CampusName_170226.doc` + `.ppt`
- [ ] Total size < 45 MB

---

## 📄 Reference Files

- **`HOW_TO_RUN.md`** — Step-by-step setup & run instructions
- **`Downloaded_Things.md`** — What's installed, sizes, who needs what
- **`setup.sh`** — One-command setup (run: `./setup.sh <your-name>`)
- **`docker-compose.yml`** — Ollama + PostgreSQL via Docker
