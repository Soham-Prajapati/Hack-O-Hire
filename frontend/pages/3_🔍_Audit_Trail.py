"""
Audit Trail — Full explainability view for SAR generation decisions.
Connected to backend API with mock fallback.
Owner: SIDDH ONLY
"""
import streamlit as st
import json
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from api_client import is_backend_available, get_audit_trail

st.set_page_config(page_title="Audit Trail | SAR Generator", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .trail-step {
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        animation: fadeInUp 0.5s ease-out both;
    }
    .step-data { background: #0d1b2a; border-left: 4px solid #58a6ff; }
    .step-compliance { background: #1a0d2b; border-left: 4px solid #a78bfa; }
    .step-rag { background: #0d2b1a; border-left: 4px solid #34d399; }
    .step-narrator { background: #2b1a0d; border-left: 4px solid #fbbf24; }
    .step-qa { background: #0d1b2b; border-left: 4px solid #f87171; }
    .step-system { background: #1a1a2e; border-left: 4px solid #8b949e; }
    .step-analyst { background: #1e1a2e; border-left: 4px solid #c084fc; }
    .conf-bar {
        height: 8px; border-radius: 4px; background: #21262d; overflow: hidden;
    }
    .conf-fill {
        height: 100%; border-radius: 4px;
    }
    .live-tag {
        display: inline-block; padding: 2px 8px; border-radius: 4px;
        font-size: 0.7rem; font-weight: 600;
    }
    .live-tag-on { background: #064e3b; color: #34d399; border: 1px solid #34d399; }
    .live-tag-off { background: #1f2937; color: #fbbf24; border: 1px solid #fbbf24; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔍 Audit Trail Viewer")
st.markdown("*Complete reasoning trace — every AI decision is traceable, defensible, and regulator-ready.*")

# Show data source
backend_online = is_backend_available()
if backend_online:
    st.markdown('<span class="live-tag live-tag-on">● LIVE DATA</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="live-tag live-tag-off">◌ DEMO DATA</span>', unsafe_allow_html=True)

st.markdown("---")

# --- MOCK AUDIT TRAIL ---
MOCK_AUDIT_TRAIL = [
    {
        "step": 1,
        "agent": "data_analyst",
        "action": "Analyzed 21 transactions for account XXXX-4521",
        "data_points_used": ["20 inbound transfers from 20 unique senders", "Total inbound: ₹50,12,000", "1 outbound SWIFT: ₹48,00,000", "Time window: 5 days (Jan 15-19)", "Outbound within 48 hrs of last credit"],
        "output": "HIGH-RISK PATTERN DETECTED: Multiple sub-threshold inbound transfers from unrelated senders, followed by immediate international consolidation transfer. Volume 16.7x above declared average.",
        "confidence": 0.96,
    },
    {
        "step": 2,
        "agent": "compliance_mapper",
        "action": "Matched transaction patterns to regulatory typologies",
        "data_points_used": ["FinCEN Advisory FIN-2024-A003 (Structuring)", "RBI Master Direction Sec 14.2 (Suspicious Patterns)", "FATF Typology: ML/TF Red Flag Indicator #23"],
        "output": "PRIMARY TYPOLOGY: Structuring/Smurfing (Confidence: 94%). SECONDARY: Layering via international wire (Confidence: 87%). Matched 3 regulatory references.",
        "confidence": 0.94,
    },
    {
        "step": 3,
        "agent": "rag_retriever",
        "action": "Retrieved regulatory templates and similar past SARs",
        "data_points_used": ["SAR Template T-005 (Structuring)", "FinCEN Narrative Guidance (5Ws+How)", "Similar SAR: CASE-2025-8821 (89% similarity)"],
        "output": "Retrieved 3 relevant documents. Template T-005 selected as primary narrative framework. Past SAR CASE-2025-8821 used as reference for language patterns.",
        "confidence": 0.91,
    },
    {
        "step": 4,
        "agent": "narrator",
        "action": "Generated FinCEN-compliant SAR narrative",
        "data_points_used": ["Structure: Introduction → Body (5Ws+How) → Conclusion", "Word count: 847 words", "All 5Ws addressed", "Evidence-linked throughout"],
        "output": "Draft SAR narrative generated in FinCEN format. All six elements (Who, What, When, Where, Why, How) addressed with specific data point citations. Three-part structure maintained.",
        "confidence": 0.93,
    },
    {
        "step": 5,
        "agent": "qa_validator",
        "action": "Validated narrative completeness, compliance, and quality",
        "data_points_used": ["Completeness: 95% (all required elements present)", "Compliance: 98% (FinCEN format met)", "Readability: Flesch-Kincaid Grade 12.1", "Evidence Linkage: 91% (43/47 claims backed)"],
        "output": "PASSED: Narrative meets quality thresholds. Minor suggestion: Add sender geographic distribution detail in WHERE section. Overall quality score: 93/100.",
        "confidence": 0.95,
    },
]

# Agent display mapping
AGENT_DISPLAY = {
    "data_analyst": {"icon": "🔍", "label": "Data Analyst Agent", "style": "step-data", "color": "#58a6ff"},
    "compliance_mapper": {"icon": "📋", "label": "Compliance Mapper Agent", "style": "step-compliance", "color": "#a78bfa"},
    "rag_retriever": {"icon": "📖", "label": "RAG Context Retriever", "style": "step-rag", "color": "#34d399"},
    "narrator": {"icon": "✍️", "label": "Narrator Agent (Llama 3.1 8B)", "style": "step-narrator", "color": "#fbbf24"},
    "qa_validator": {"icon": "✅", "label": "QA Validator Agent", "style": "step-qa", "color": "#f87171"},
    "system": {"icon": "⚙️", "label": "System", "style": "step-system", "color": "#8b949e"},
    "analyst": {"icon": "👤", "label": "Analyst (Manual)", "style": "step-analyst", "color": "#c084fc"},
}

# SAR selector
sar_case = st.selectbox(
    "Select SAR",
    ["SAR-001 — CASE-7A3F21 (Rajesh Kumar — Smurfing)", "SAR-002 — CASE-B92E44 (Meridian Trading — Layering)"],
)

# --- Try loading live audit trail ---
audit_trail = MOCK_AUDIT_TRAIL
live_loaded = False

if backend_online and st.session_state.get("sar_id"):
    live_trail, err = get_audit_trail(st.session_state.sar_id)
    if live_trail and not err and len(live_trail) > 0:
        audit_trail = live_trail
        live_loaded = True

# Summary metrics
total_steps = len(audit_trail)
agents_used = len(set(s.get("agent", "unknown") for s in audit_trail))
total_data_points = sum(len(s.get("data_points_used", [])) for s in audit_trail)
confidences = [s.get("confidence", 0) for s in audit_trail if s.get("confidence")]
avg_conf = sum(confidences) / len(confidences) * 100 if confidences else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Steps", str(total_steps))
m2.metric("Agents Used", str(agents_used))
m3.metric("Data Points Cited", str(total_data_points))
m4.metric("Avg Confidence", f"{avg_conf:.1f}%")

st.markdown("---")

# --- Render each step ---
for step_data in audit_trail:
    agent_key = step_data.get("agent", "system")
    agent_info = AGENT_DISPLAY.get(agent_key, AGENT_DISPLAY["system"])
    step_num = step_data.get("step", "?")
    confidence = step_data.get("confidence", 0)
    data_points = step_data.get("data_points_used", [])
    rules = step_data.get("rules_matched", [])
    output = step_data.get("output", "")
    action = step_data.get("action", "")
    timestamp = step_data.get("timestamp", "")

    with st.expander(f"{agent_info['icon']} Step {step_num} — {agent_info['label']}", expanded=True):
        st.markdown(f"""
        <div class="trail-step {agent_info['style']}">
            <strong style="color:{agent_info['color']};">Agent:</strong> {agent_info['label']}<br>
            <strong style="color:{agent_info['color']};">Action:</strong> {action}
            {"<br><small style='color:#8b949e;'>⏱ " + timestamp + "</small>" if timestamp else ""}
        </div>
        """, unsafe_allow_html=True)

        # Data points
        if data_points:
            st.markdown("##### 📊 Data Points Used")
            mid = (len(data_points) + 1) // 2
            col1, col2 = st.columns(2)
            with col1:
                for dp in data_points[:mid]:
                    st.markdown(f"- {dp}")
            with col2:
                for dp in data_points[mid:]:
                    st.markdown(f"- {dp}")

        # Rules matched
        if rules:
            st.markdown("##### 📜 Regulatory References Matched")
            for rule in rules:
                st.markdown(f"- {rule}")

        # Output
        if output:
            st.markdown("##### 🧠 Agent Output")
            # Color-code by severity keywords
            output_lower = output.lower()
            if "high-risk" in output_lower or "critical" in output_lower:
                st.error(f"**{output}**")
            elif "passed" in output_lower or "retrieved" in output_lower or "success" in output_lower:
                st.success(output)
            elif "typology" in output_lower or "warning" in output_lower:
                st.warning(output)
            else:
                st.info(output)

        # Confidence
        if confidence:
            st.markdown(f"**Confidence:** {int(confidence * 100)}%")
            st.progress(confidence)

st.markdown("---")

# Raw JSON
with st.expander("🗂️ Raw Audit Log (JSON)", expanded=False):
    raw_log = {
        "sar_id": st.session_state.get("sar_id", "SAR-001"),
        "case_id": "CASE-7A3F21",
        "generated_at": "2026-02-15T10:45:32.000Z",
        "model": "llama3.1:8b",
        "total_steps": total_steps,
        "total_data_points_cited": total_data_points,
        "avg_confidence": round(avg_conf / 100, 3),
        "source": "live_api" if live_loaded else "mock_data",
        "audit_trail": audit_trail,
    }
    st.json(raw_log)

st.markdown("---")
st.caption("Every step is logged, traceable, and auditable. No black-box decisions — full transparency for regulators and compliance teams.")
