# 🤖 Agent Prompts — Paste These to Get Started

> Each person pastes their prompt into their AI agent (Cursor / Copilot / Claude / ChatGPT).  
> Make sure you have the project open in your IDE first.

---

## 🔷 SHUBH — Backend + AI Integration Lead

```
I am Shubh, the Backend + AI Integration Lead for the SAR Narrative Generator hackathon project.

PROJECT CONTEXT:
- This is a FinCEN SAR (Suspicious Activity Report) narrative generator using AI
- Tech stack: FastAPI backend, Streamlit frontend, Ollama + Llama 3.1 (LLM), ChromaDB (RAG), XGBoost (ML classifier)
- Deadline: Feb 17, 2026 — 11:59 PM IST
- My role: FastAPI API routes, system integration, wiring the AI pipeline together

KEY FILES I OWN (only edit these — see File Ownership Map in SAR_TODO_ROUND1.md):
- backend/app/main.py
- backend/app/api/routes.py
- backend/app/api/schemas.py
- docker-compose.yml

HOW TO WORK:
1. Read SAR_TODO_ROUND1.md FIRST — it has the full plan organized in Phases (I → II → III)
2. Check which Phase I'm currently in — look at the checkboxes ([ ] = todo, [x] = done, [/] = in progress)
3. Work through MY tasks in the current phase, one by one
4. Mark each task [x] when done, [/] when in progress
5. Only move to the next phase when all my tasks in the current phase are complete
6. Follow the Integration Contracts at the bottom of SAR_TODO_ROUND1.md — they define the JSON format my code must produce/consume

IMPORTANT FILES TO READ:
- SAR_TODO_ROUND1.md — Master task list (start here, always)
- backend/app/api/routes.py — My API endpoints
- backend/app/api/schemas.py — Data models / integration contracts
- backend/app/core/llm_engine.py — LLM engine (Dev owns this, I wire it into routes)
- HOW_TO_RUN.md — How to run frontend + backend

Start by reading SAR_TODO_ROUND1.md. Identify which phase I'm in, which of MY tasks are still incomplete, and help me work through them in order.
```

---

## 🔷 DEV — LLM/RAG + AI Core Lead

```
I am Dev, the LLM/RAG + AI Core Lead for the SAR Narrative Generator hackathon project.

PROJECT CONTEXT:
- This is a FinCEN SAR (Suspicious Activity Report) narrative generator using AI
- Tech stack: FastAPI backend, Streamlit frontend, Ollama + Llama 3.1 8B (LLM), ChromaDB (RAG), LangChain
- Deadline: Feb 17, 2026 — 11:59 PM IST
- My role: Build the AI core — LLM inference, RAG pipeline, prompt engineering, audit trail logging

KEY FILES I OWN (only edit these — see File Ownership Map in SAR_TODO_ROUND1.md):
- backend/app/core/llm_engine.py
- backend/app/core/rag_pipeline.py
- backend/app/core/audit_logger.py
- backend/knowledge_base/ (all files in this directory)

HOW TO WORK:
1. Read SAR_TODO_ROUND1.md FIRST — it has the full plan organized in Phases (I → II → III)
2. Check which Phase I'm currently in — look at the checkboxes ([ ] = todo, [x] = done, [/] = in progress)
3. Work through MY tasks in the current phase, one by one
4. Mark each task [x] when done, [/] when in progress
5. Only move to the next phase when all my tasks in the current phase are complete
6. Follow the Integration Contracts at the bottom of SAR_TODO_ROUND1.md — my generate_sar() function must return the exact JSON format specified there

IMPORTANT FILES TO READ:
- SAR_TODO_ROUND1.md — Master task list (start here, always)
- backend/app/core/llm_engine.py — Has the SAR system prompt skeleton
- backend/app/core/rag_pipeline.py — ChromaDB skeleton
- backend/app/core/audit_logger.py — Audit trail skeleton
- backend/knowledge_base/sar_templates/ — SAR narrative templates
- backend/knowledge_base/regulations/fincen_guidance.txt — FinCEN rules
- docker-compose.yml — Ollama runs via Docker
- HOW_TO_RUN.md — Setup instructions including Ollama Docker setup

Start by reading SAR_TODO_ROUND1.md. Identify which phase I'm in, which of MY tasks are still incomplete, and help me work through them in order.
```

---

## 🔷 SIDDH — Frontend Lead (Streamlit)

```
I am Siddh, the Frontend Lead for the SAR Narrative Generator hackathon project.

PROJECT CONTEXT:
- This is a FinCEN SAR (Suspicious Activity Report) narrative generator using AI
- Tech stack: Streamlit (frontend), FastAPI (backend), dark theme UI
- Deadline: Feb 17, 2026 — 11:59 PM IST
- My role: Streamlit UI — dashboard, SAR editor, audit trail viewer, visualizations

KEY FILES I OWN (only edit these — see File Ownership Map in SAR_TODO_ROUND1.md):
- frontend/app.py
- frontend/pages/ (all page files)
- frontend/components/ (if any)

HOW TO WORK:
1. Read SAR_TODO_ROUND1.md FIRST — it has the full plan organized in Phases (I → II → III)
2. Check which Phase I'm currently in — look at the checkboxes ([ ] = todo, [x] = done, [/] = in progress)
3. Work through MY tasks in the current phase, one by one
4. Mark each task [x] when done, [/] when in progress
5. Only move to the next phase when all my tasks in the current phase are complete
6. The frontend already has demo-ready mock data — pages work standalone without the backend

IMPORTANT FILES TO READ:
- SAR_TODO_ROUND1.md — Master task list (start here, always)
- frontend/app.py — Main page with metrics, case cards, file upload
- frontend/pages/1_📊_Dashboard.py — Case table, analytics, alerts
- frontend/pages/2_📝_SAR_Editor.py — Split-screen SAR editor
- frontend/pages/3_🔍_Audit_Trail.py — AI reasoning trace viewer
- HOW_TO_RUN.md — How to run the frontend

Start by reading SAR_TODO_ROUND1.md. Identify which phase I'm in, which of MY tasks are still incomplete, and help me work through them in order.
```

---

## 🔷 HET — Data & ML Engineer

```
I am Het, the Data & ML Engineer for the SAR Narrative Generator hackathon project.

PROJECT CONTEXT:
- This is a FinCEN SAR (Suspicious Activity Report) narrative generator using AI
- Tech stack: XGBoost (classifier), SHAP (explainability), Pandas (data processing)
- Deadline: Feb 17, 2026 — 11:59 PM IST
- My role: Datasets, data parsing, XGBoost typology classifier, SHAP explanations

KEY FILES I OWN (only edit these — see File Ownership Map in SAR_TODO_ROUND1.md):
- backend/app/utils/data_parser.py
- ml_models/typology_classifier.py
- data/sample_data/ (all files in this directory)

HOW TO WORK:
1. Read SAR_TODO_ROUND1.md FIRST — it has the full plan organized in Phases (I → II → III)
2. Check which Phase I'm currently in — look at the checkboxes ([ ] = todo, [x] = done, [/] = in progress)
3. Work through MY tasks in the current phase, one by one
4. Mark each task [x] when done, [/] when in progress
5. Only move to the next phase when all my tasks in the current phase are complete
6. Follow the Integration Contracts at the bottom of SAR_TODO_ROUND1.md — my predict_typology() function must return the exact JSON format specified there

IMPORTANT FILES TO READ:
- SAR_TODO_ROUND1.md — Master task list (start here, always)
- ml_models/typology_classifier.py — XGBoost classifier skeleton
- backend/app/utils/data_parser.py — Data parser skeleton
- data/sample_data/scenario_smurfing.csv — Example demo data
- HOW_TO_RUN.md — How to run the project

Start by reading SAR_TODO_ROUND1.md. Identify which phase I'm in, which of MY tasks are still incomplete, and help me work through them in order.
```

---

## 🔷 SAKSHI — Docs, PPT & Submission Lead

```
I am Sakshi, the Docs, PPT & Submission Lead for the SAR Narrative Generator hackathon project.

PROJECT CONTEXT:
- This is a FinCEN SAR (Suspicious Activity Report) narrative generator using AI
- Tech stack: Python, FastAPI, Streamlit, Ollama/Llama 3.1, ChromaDB, XGBoost
- Deadline: Feb 17, 2026 — 11:59 PM IST
- My role: Submission document, PowerPoint presentation, screenshots, README

KEY FILES I OWN (only edit these — see File Ownership Map in SAR_TODO_ROUND1.md):
- screenshots/ (all files)
- TeamName_CampusName_160226.md
- SAR_PPT_DATA.md
- README.md

HOW TO WORK:
1. Read SAR_TODO_ROUND1.md FIRST — it has the full plan organized in Phases (I → II → III) plus a Submission Checklist
2. Check which Phase I'm currently in — look at the checkboxes ([ ] = todo, [x] = done, [/] = in progress)
3. Work through MY tasks in the current phase, one by one
4. Mark each task [x] when done, [/] when in progress
5. Only move to the next phase when all my tasks in the current phase are complete
6. The frontend UI is already demo-ready — you can take screenshots now by running: cd frontend && streamlit run app.py

IMPORTANT FILES TO READ:
- SAR_TODO_ROUND1.md — Master task list + submission checklist (start here, always)
- README.md — Current project README
- Downloaded_Things.md — Tech stack overview
- HOW_TO_RUN.md — How the project runs (useful for methodology section)

Start by reading SAR_TODO_ROUND1.md. Identify which phase I'm in, which of MY tasks are still incomplete, and help me work through them in order. Pay special attention to the Round 1 Submission Checklist at the bottom.
```

---

## 💡 Tips for Everyone

1. **Always read `SAR_TODO_ROUND1.md` first** — it's the single source of truth
2. **Follow phases in order** — Phase I → II → III. Don't skip ahead
3. **Only edit YOUR files** — see the File Ownership Map to avoid merge conflicts
4. **Mark tasks as you go** — `[/]` when starting, `[x]` when done
5. **Pull before you push** — `git pull origin main` before `git push`
6. **Check Integration Contracts** — they define how your code connects to others'
