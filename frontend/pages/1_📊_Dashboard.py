"""
Dashboard — Case overview with analytics.
Owner: Het
"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard | SAR Generator", page_icon="📊", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    .dash-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📊 Case Dashboard")
st.markdown("Overview of all suspicious activity cases and SAR generation pipeline status.")
st.markdown("---")

# Tabs
tab_cases, tab_analytics, tab_alerts = st.tabs(["🗂️ All Cases", "📈 Analytics", "🚨 Alerts"])

with tab_cases:
    cases_df = pd.DataFrame([
        {"Case ID": "CASE-7A3F21", "Customer": "Rajesh Kumar", "Alert": "High Volume Inbound", "Risk": "🔴 CRITICAL", "Status": "Draft", "Amount": "₹50,12,000", "Txns": 21, "Date": "Feb 15"},
        {"Case ID": "CASE-B92E44", "Customer": "Meridian Trading LLC", "Alert": "Shell Company Round-Trip", "Risk": "🔴 CRITICAL", "Status": "Review", "Amount": "₹2,34,00,000", "Txns": 83, "Date": "Feb 14"},
        {"Case ID": "CASE-D1F087", "Customer": "Anita Chauhan", "Alert": "Sub-Threshold Deposits", "Risk": "🟠 HIGH", "Status": "Approved", "Amount": "₹9,85,000", "Txns": 12, "Date": "Feb 13"},
        {"Case ID": "CASE-E4C5A2", "Customer": "Vikram Malhotra", "Alert": "Unusual Wire Pattern", "Risk": "🟡 MEDIUM", "Status": "Draft", "Amount": "₹15,40,000", "Txns": 7, "Date": "Feb 16"},
    ])
    st.dataframe(cases_df, use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🏷️ Status Breakdown")
        st.markdown("""
        - 📝 **Draft:** 2 cases (CASE-7A3F21, CASE-E4C5A2)
        - 🔍 **Under Review:** 1 case (CASE-B92E44)
        - ✅ **Approved:** 1 case (CASE-D1F087)
        - ❌ **Rejected:** 0 cases
        """)
    with col2:
        st.markdown("#### ⏱️ Processing Metrics")
        st.metric("Avg SAR Generation Time", "45 sec", "-30 sec vs. manual")
        st.metric("Avg Quality Score", "93/100", "+12 pts vs. baseline")

with tab_analytics:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Typology Distribution")
        typo_df = pd.DataFrame({
            "Typology": ["Structuring", "Smurfing", "Layering", "Shell Company", "Other"],
            "Count": [8, 5, 3, 2, 1],
        })
        st.bar_chart(typo_df.set_index("Typology"), color="#764ba2")

    with c2:
        st.markdown("#### Monthly SAR Volume")
        monthly = pd.DataFrame({
            "Month": ["Oct", "Nov", "Dec", "Jan", "Feb"],
            "SARs Filed": [12, 18, 15, 22, 4],
        })
        st.line_chart(monthly.set_index("Month"), color="#667eea")

    st.markdown("#### 💰 Transaction Volume Under Investigation")
    st.metric("Total Amount Flagged (Feb 2026)", "₹3,09,37,000")
    st.metric("Total Transactions Analyzed", "123")

with tab_alerts:
    st.warning("🚨 **2 CRITICAL alerts** require immediate SAR filing")
    st.error("**CASE-7A3F21** — Rajesh Kumar: 20 unique senders, ₹50L in 5 days → International wire. Structuring pattern detected (94% confidence).")
    st.error("**CASE-B92E44** — Meridian Trading LLC: Shell company round-tripping ₹2.34 Cr through 6 intermediaries. Layering detected (89% confidence).")
    st.warning("**CASE-E4C5A2** — Vikram Malhotra: Unusual wire transfer pattern to high-risk jurisdiction. Medium risk, pending analysis.")
    st.success("**CASE-D1F087** — Anita Chauhan: SAR filed and approved ✓")
