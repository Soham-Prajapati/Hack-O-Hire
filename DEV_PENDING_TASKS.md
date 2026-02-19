# 🧠 Dev's Pending Tasks (AI Core & Evaluation)

> **Status:** Handover Mode
> **Owner:** Dev (AI Lead)

The system is technically functional (API, Frontend, RAG pipeline are live). The remaining work is **qualitative** and **evaluative**.

---

## 1. 🧪 Evaluation ("The EV")
**Goal:** Prove the AI writes *better* SARs than a junior analyst.

- [ ] **Run the 3 Scenarios:**
    - Use the Dashboard or API to generate SARs for:
        1.  `scenario_smurfing.csv`
        2.  `scenario_layering.csv`
        3.  `scenario_structuring.csv`
- [ ] **Quality Audit (Manual Review):**
    - Check for **Hallucinations**: Did it invent a middle name? Did it get the total amount right?
    - Check **Tone**: Is it dry, factual, and strictly professional? (No "It appears that...", just "The data shows...")
    - Check **Structure**: Does it strictly follow the Introduction / Body / Conclusion format?

## 2. 🔧 Advanced Prompt Tuning
**File:** `backend/app/core/llm_engine.py`

- [ ] **Refine `SAR_SYSTEM_PROMPT`:**
    - If the "EV" shows issues, tweak the system prompt.
    - *Tip:* Add negative constraints like "Do not use flowery language" or "Do not summarize the data if it is already listed in the table."
- [ ] **Few-Shot Examples (Optional but Recommended):**
    - Add a "Perfect SAR" example to the prompt context if the model struggles with format.

## 3. 📚 Knowledge Base Population
**Directory:** `backend/knowledge_base/`

- [ ] **Verify Content:**
    - Ensure `regulations/` has text files with actual FinCEN guidance (PDF usage requires OCR, sticking to .txt is safer for now).
    - Ensure `sar_templates/` has at least one good example of a narrative.
- [ ] **Re-index:**
    - If you add files, restart the backend to trigger the RAG re-indexing (it runs on startup in `lifespan` or `__init__`).

---

## 4. 🚀 Final Output Check
**Success Criteria:**
1.  The PDF export looks like a human wrote it.
2.  The "Risk Score" in the narrative justification matches the ML model's score.
3.  The "Audit Trail" logs the specific documents retrieved by RAG.
