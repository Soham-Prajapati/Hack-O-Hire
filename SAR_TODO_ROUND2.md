# 🚀 SAR Narrative Generator — Round 2 TODO (Deadline: Feb 19)

> **Status:** DEADLINE EXTENDED! 🎉  
> **New Goal:** Add "WOW" features to guarantee a win.  
> **Deadline:** Feb 19, 2026 — 11:59 PM IST

---

## 🌟 New Feature Additions (The "Wow" Factors)

We have 2 extra days. We are moving beyond "functional" to **"impressive."**

1.  **🕸️ Transaction Network Graph** (Interactive Visuals)
2.  **📄 One-Click PDF Export** (Professional FinCEN format)
3.  **💬 Chat-with-SAR** (Q&A with the Audit Trail)
4.  **🌍 Geo-Spatial Map** (Where is the money going?)
5.  **⚡ "Time Saved" ROI Metric** (Instant business value)

---

## 👥 Updated Role Assignments

### 👨‍💻 SIDDH (Frontend Lead) — *Status: High Capacity*
> *Mission: Make the UI strictly "Enterprise Grade" and add visual storytelling.*

- [x] **Transaction Network Graph:**
    - Implementation: Use `streamlit-agraph` or `plotly` to show money flow.
    - *Visual:* Central node = Subject, Peripheral nodes = Beneficiaries. Edge thickness = Amount.
- [x] **Geo-Spatial Map:**
    - Implementation: `st.map` or `plotly.scatter_mapbox`.
    - Show pins for "Source Bank" and "Destination Bank" locations.
- [x] **Chat-with-SAR Widget:**
    - Add a floating chat interface (or sidebar tab) to "Ask questions about this SAR."
- [x] **PDF Export Button:**
    - Frontend button to trigger the backend PDF generation and handle the file download.
- [x] **ROI Dashboard Metric:**
    - Add a dynamic counter: *"Time Saved: ~5 hours by AI"* next to the generation button.

### 📊 HET (Data & ML Lead) — *Status: Critical Path*
> *Mission: Deliver the core model, then enrich data for the new visuals.*

- [x] **CRITICAL:** Finish `data_parser.py` (CSV → JSON) — *Blocker for everyone.*
- [x] **CRITICAL:** Train XGBoost model & save `.joblib`.
- [x] **Enrich Mock Data:**
    - Add dummy `latitude`/`longitude` to the CSVs for Siddh's map.
    - Ensure `beneficiary_bank` names are diverse (e.g., "Deutsche Bank, Frankfurt", "Chase, NY") for the map/graph.
- [x] **Risk Scoring Logic:**
    - Update `predict_typology` to return a `risk_score` (0-100) alongside the class.
    - *Why?* So Siddh can show a "Risk Gauge" on the dashboard.

### 📝 SAKSHI (Product & Docs Lead) — *Status: Medium Capacity*
> *Mission: Craft the "Winning Narrative" (Video + Pitch).*

- [ ] **Competitor Research (The "Kill Slide"):**
    - Research **Actimize** and **Oracle AML**.
    - Create a slide comparing us vs. them. *Key wins: Local Privacy (Ollama), Full Audit Trail, Cost.*
- [ ] **Demo Video Script:**
    - Write a strict second-by-second script for the 3-minute video.
    - *0:00-0:30:* The Pain (Manual SARs).
    - *0:30-1:30:* The Solution (Upload -> Generate).
    - *1:30-2:30:* The "Wow" (Graph, Map, Chat).
    - *2:30-3:00:* The Audit Trail (Trust).
- [x] **PDF Template Design:**
    - Sketch how the final PDF layout should look. Hand off requirements to Shubh for backend gen.
- [ ] **User Manual:**
    - Add a "How to Use" section to the main submission document.

### ⚙️ SHUBH & DEV (Backend & AI Core)
- [x] **Shubh:** Build `/api/export-pdf` (ReportLab) & `/api/graph-data` endpoints.
- [x] **Dev:** Build `chat_with_sar` RAG chain (allow querying the specific SAR context).
- [x] **Dev:** Refine prompts to be strict/regulatory professional.

---

## 📅 Revised Timeline (Feb 17 - Feb 19)

| Time | Goal | Owner |
|------|------|-------|
| **Feb 17 (Tonight)** | **Finish Parser + Model** (Het) \| **Scaffold New UI** (Siddh) | Het, Siddh |
| **Feb 18 (Morning)** | **Backend Integration** (PDF, Graph API) | Shubh |
| **Feb 18 (Evening)** | **Chat-with-SAR Integration** \| **Demo Script Final** | Dev, Sakshi |
| **Feb 19 (Morning)** | **Full End-to-End Testing** \| **Video Recording** | All |
| **Feb 19 (Evening)** | **Final Submission** | Sakshi |
