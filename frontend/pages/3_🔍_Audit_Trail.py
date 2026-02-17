"""
Audit Trail — Full explainability view for SAR generation decisions.
Owner: Het
"""
import streamlit as st
import json

st.set_page_config(page_title="Audit Trail | SAR Generator", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    .trail-step {
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .step-data { background: #0d1b2a; border-left: 4px solid #58a6ff; }
    .step-compliance { background: #1a0d2b; border-left: 4px solid #a78bfa; }
    .step-rag { background: #0d2b1a; border-left: 4px solid #34d399; }
    .step-narrator { background: #2b1a0d; border-left: 4px solid #fbbf24; }
    .step-qa { background: #0d1b2b; border-left: 4px solid #f87171; }
    .conf-bar {
        height: 8px; border-radius: 4px; background: #21262d; overflow: hidden;
    }
    .conf-fill {
        height: 100%; border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔍 Audit Trail Viewer")
st.markdown("*Complete reasoning trace — every AI decision is traceable, defensible, and regulator-ready.*")
st.markdown("---")

# SAR selector
sar_case = st.selectbox(
    "Select SAR",
    ["SAR-001 — CASE-7A3F21 (Rajesh Kumar — Smurfing)", "SAR-002 — CASE-B92E44 (Meridian Trading — Layering)"],
)

# Summary metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Steps", "5")
m2.metric("Agents Used", "4 + RAG")
m3.metric("Data Points Cited", "47")
m4.metric("Avg Confidence", "93.8%")

st.markdown("---")

# ===== STEP 1: Data Analyst =====
with st.expander("🔍 Step 1 — Data Analyst Agent", expanded=True):
    st.markdown("""
    <div class="trail-step step-data">
        <strong style="color:#58a6ff;">Agent:</strong> Data Analyst Agent<br>
        <strong style="color:#58a6ff;">Action:</strong> Analyzed 21 transactions for account XXXX-4521
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📊 Data Points Used")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - 20 inbound transfers from **20 unique senders**
        - Total inbound: **₹50,12,000**
        - Time window: **5 days** (Jan 15–19, 2026)
        - Individual amounts: ₹76K – ₹1.45L range
        """)
    with col2:
        st.markdown("""
        - 1 outbound SWIFT transfer: **₹48,00,000**
        - Destination: Deutsche Bank AG, Frankfurt
        - Outbound within **48 hours** of last credit
        - **14 different originating banks**
        """)

    st.markdown("##### 🧠 Agent Output")
    st.error("**HIGH-RISK PATTERN DETECTED:** Multiple sub-threshold inbound transfers from unrelated senders, followed by immediate international consolidation transfer. Volume 16.7x above declared average monthly volume (₹50.12L received vs. ₹3L declared).")
    
    st.markdown("**Confidence:** 96%")
    st.progress(0.96)

# ===== STEP 2: Compliance Mapper =====
with st.expander("📋 Step 2 — Compliance Mapper Agent", expanded=True):
    st.markdown("""
    <div class="trail-step step-compliance">
        <strong style="color:#a78bfa;">Agent:</strong> Compliance Mapper Agent<br>
        <strong style="color:#a78bfa;">Action:</strong> Matched transaction patterns against regulatory typology database
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📜 Regulatory References Matched")
    st.markdown("""
    | Rule | Source | Match Confidence |
    |------|--------|:---:|
    | Structuring / Smurfing | FinCEN Advisory FIN-2024-A003 | 94% |
    | Layering via International Wire | FATF Red Flag Indicator #23 | 87% |
    | Suspicious Transaction Pattern | RBI Master Direction Sec 14.2 | 91% |
    """)

    st.markdown("##### 🧠 Agent Output")
    st.warning("**PRIMARY TYPOLOGY:** Structuring/Smurfing (Confidence: 94%). **SECONDARY:** Layering via international wire transfer (Confidence: 87%). Three regulatory references matched across FinCEN, FATF, and RBI guidelines.")
    
    st.markdown("**Confidence:** 94%")
    st.progress(0.94)

# ===== STEP 3: RAG Context Retrieval =====
with st.expander("📖 Step 3 — RAG Context Retriever", expanded=True):
    st.markdown("""
    <div class="trail-step step-rag">
        <strong style="color:#34d399;">Agent:</strong> RAG Context Retriever (ChromaDB + LangChain)<br>
        <strong style="color:#34d399;">Action:</strong> Retrieved relevant regulatory templates and similar past SAR narratives
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📄 Documents Retrieved (Top 3)")
    
    doc1, doc2, doc3 = st.columns(3)
    with doc1:
        st.markdown("""
        **📑 SAR Template T-005**  
        *Structuring/Smurfing Template*  
        Relevance: 96%  
        Source: `sar_templates/template_structuring.txt`
        """)
    with doc2:
        st.markdown("""
        **📑 FinCEN Narrative Guidance**  
        *5Ws + How Framework*  
        Relevance: 93%  
        Source: `regulations/fincen_guidance.txt`
        """)
    with doc3:
        st.markdown("""
        **📑 Similar SAR: CASE-2025-8821**  
        *89% pattern similarity*  
        Relevance: 89%  
        Source: `past_sars/case_8821.txt`
        """)

    st.markdown("##### 🧠 Agent Output")
    st.success("Retrieved 3 relevant documents from knowledge base (47 total indexed). Template T-005 selected as primary narrative framework. Past SAR CASE-2025-8821 used as reference for regulatory language patterns.")

    st.markdown("**Confidence:** 91%")
    st.progress(0.91)

# ===== STEP 4: Narrator Agent =====
with st.expander("✍️ Step 4 — Narrator Agent (Llama 3.1 8B)", expanded=True):
    st.markdown("""
    <div class="trail-step step-narrator">
        <strong style="color:#fbbf24;">Agent:</strong> Narrator Agent (Llama 3.1 8B via Ollama)<br>
        <strong style="color:#fbbf24;">Action:</strong> Generated FinCEN-compliant SAR narrative using augmented context
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📝 Generation Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Word Count", "847")
    with col2:
        st.metric("Sections", "3 (Intro/Body/Conclusion)")
    with col3:
        st.metric("5Ws Coverage", "6/6 ✓")

    st.markdown("##### 📋 Prompt Components")
    st.markdown("""
    1. **System Prompt:** FinCEN SAR narrative expert role + format instructions + guardrails
    2. **Retrieved Context:** Template T-005 + FinCEN guidance + past SAR reference
    3. **Case Data:** 21 transactions, customer KYC profile, typology prediction (94%)
    4. **Instructions:** Address all 5Ws+How, cite specific data points, maintain objectivity
    """)

    st.markdown("##### 🧠 Agent Output")
    st.info("Draft SAR narrative generated successfully in FinCEN three-part format. All six elements (Who, What, When, Where, Why, How) addressed with specific data point citations. 43 out of 47 relevant data points referenced in the narrative.")

    st.markdown("**Confidence:** 93%")
    st.progress(0.93)

# ===== STEP 5: QA Validator =====
with st.expander("✅ Step 5 — QA Validator Agent", expanded=True):
    st.markdown("""
    <div class="trail-step step-qa">
        <strong style="color:#f87171;">Agent:</strong> QA Validator Agent<br>
        <strong style="color:#f87171;">Action:</strong> Validated narrative completeness, compliance, readability, and evidence linkage
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📊 Quality Scores")
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.metric("Completeness", "95%")
        st.progress(0.95)
    with q2:
        st.metric("Compliance", "98%")
        st.progress(0.98)
    with q3:
        st.metric("Readability", "88%")
        st.progress(0.88)
    with q4:
        st.metric("Evidence Linkage", "91%")
        st.progress(0.91)

    st.markdown("##### ⚠️ Suggestions")
    st.warning("**Minor:** Consider adding sender geographic distribution detail in the WHERE section to strengthen spatial pattern evidence.")
    st.success("**Overall:** PASSED — Narrative meets all quality thresholds. Overall quality score: **93/100**.")

    st.markdown("**Confidence:** 95%")
    st.progress(0.95)

st.markdown("---")

# Raw JSON
with st.expander("🗂️ Raw Audit Log (JSON)", expanded=False):
    raw_log = {
        "sar_id": "SAR-001",
        "case_id": "CASE-7A3F21",
        "generated_at": "2026-02-15T10:45:32.000Z",
        "model": "llama3.1:8b",
        "total_steps": 5,
        "total_data_points_cited": 47,
        "avg_confidence": 0.938,
        "audit_trail": [
            {
                "step": 1, "agent": "data_analyst",
                "action": "Analyzed 21 transactions for account XXXX-4521",
                "data_points_used": ["20 unique senders", "₹50,12,000 total inbound", "5-day window", "1 SWIFT outbound ₹48L", "14 originating banks"],
                "output": "HIGH-RISK: Multiple sub-threshold inbound transfers + international consolidation",
                "confidence": 0.96
            },
            {
                "step": 2, "agent": "compliance_mapper",
                "action": "Matched to regulatory typologies",
                "rules_matched": ["FinCEN FIN-2024-A003 (Structuring)", "FATF Red Flag #23 (Layering)", "RBI Sec 14.2"],
                "output": "Primary: Structuring (94%), Secondary: Layering (87%)",
                "confidence": 0.94
            },
            {
                "step": 3, "agent": "rag_retriever",
                "action": "Retrieved 3 documents from knowledge base",
                "documents": ["template_structuring.txt (96%)", "fincen_guidance.txt (93%)", "case_8821 (89%)"],
                "output": "Template T-005 selected as primary framework",
                "confidence": 0.91
            },
            {
                "step": 4, "agent": "narrator",
                "action": "Generated SAR narrative (847 words, 3 sections, 6/6 5Ws)",
                "data_points_cited": 43,
                "output": "FinCEN-compliant narrative generated",
                "confidence": 0.93
            },
            {
                "step": 5, "agent": "qa_validator",
                "action": "Quality validation (completeness:95%, compliance:98%, readability:88%, evidence:91%)",
                "output": "PASSED — Score: 93/100. Minor: add sender geographic distribution.",
                "confidence": 0.95
            },
        ]
    }
    st.json(raw_log)

st.markdown("---")
st.caption("Every step is logged, traceable, and auditable. No black-box decisions — full transparency for regulators and compliance teams.")
