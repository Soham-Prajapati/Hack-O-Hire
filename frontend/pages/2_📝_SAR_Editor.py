"""
SAR Editor Page — Draft, edit, and approve SAR narratives.

Owner: P3
"""
import streamlit as st

st.set_page_config(page_title="SAR Editor | SAR Generator", page_icon="📝", layout="wide")

st.markdown("# 📝 SAR Narrative Editor")
st.markdown("Review, edit, and approve AI-generated SAR narratives.")
st.markdown("---")

# Split layout
col_data, col_editor = st.columns([1, 1])

with col_data:
    st.markdown("### 📋 Case Data")
    st.info("Select a case from the Dashboard to view transaction data here.")

    st.markdown("#### Transaction Summary")
    st.json({
        "total_transactions": 0,
        "total_amount": "₹0",
        "unique_senders": 0,
        "time_window": "N/A",
        "risk_level": "N/A",
    })

with col_editor:
    st.markdown("### ✍️ SAR Narrative")

    st.markdown("**Introduction**")
    intro = st.text_area("Introduction", value="", height=100, key="intro",
                         placeholder="SAR introduction will be generated here...")

    st.markdown("**Body (5Ws + How)**")
    body = st.text_area("Body", value="", height=200, key="body",
                        placeholder="WHO, WHAT, WHEN, WHERE, WHY, HOW...")

    st.markdown("**Conclusion**")
    conclusion = st.text_area("Conclusion", value="", height=100, key="conclusion",
                              placeholder="Summary and recommendations...")

    # Action buttons
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    with col_btn1:
        st.button("🔄 Regenerate", disabled=True)
    with col_btn2:
        st.button("✅ Approve", type="primary", disabled=True)
    with col_btn3:
        st.button("❌ Reject", disabled=True)
    with col_btn4:
        st.button("📄 Export PDF", disabled=True)
