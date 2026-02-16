"""
Audit Trail Page — View the reasoning trace for SAR generation decisions.

Owner: P3
"""
import streamlit as st

st.set_page_config(page_title="Audit Trail | SAR Generator", page_icon="🔍", layout="wide")

st.markdown("# 🔍 Audit Trail Viewer")
st.markdown("Explore the complete reasoning trace behind every AI-generated SAR narrative.")
st.markdown("---")

# SAR selector
sar_id = st.selectbox("Select SAR to view audit trail:", ["No SARs available"], disabled=True)

st.markdown("---")

# Placeholder audit trail
st.markdown("### Reasoning Steps")
st.info("Audit trail will appear here once a SAR is generated. Each step shows:")

st.markdown("""
| Step | Element | What's Captured |
|------|---------|----------------|
| 1 | 🔵 **Data Points** | Which transaction records influenced the narrative |
| 2 | 🟠 **Rules Matched** | Which regulatory patterns were triggered |
| 3 | 🟣 **Context Retrieved** | RAG documents pulled for reference |
| 4 | 🟢 **Language Rationale** | Why specific phrases were chosen |
| 5 | ⚪ **Confidence Score** | How confident the AI is per section |
""")

st.markdown("---")
st.markdown("### Raw Audit Log")
st.code('{\n  "audit_trail": []\n}', language="json")
