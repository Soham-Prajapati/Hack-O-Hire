"""
Dashboard — Case overview with analytics + live API integration.
Owner: SIDDH ONLY
"""
import streamlit as st
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from api_client import is_backend_available, list_cases

st.set_page_config(page_title="Dashboard | SAR Generator", page_icon="📊", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .dash-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        animation: fadeInUp 0.5s ease-out both;
    }
    .live-tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .live-tag-on { background: #064e3b; color: #34d399; border: 1px solid #34d399; }
    .live-tag-off { background: #1f2937; color: #fbbf24; border: 1px solid #fbbf24; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📊 Case Dashboard")

# Show data source indicator
backend_online = is_backend_available()
if backend_online:
    st.markdown('<span class="live-tag live-tag-on">● LIVE DATA</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="live-tag live-tag-off">◌ DEMO DATA</span>', unsafe_allow_html=True)

st.markdown("Overview of all suspicious activity cases and SAR generation pipeline status.")
st.markdown("---")

# --- Build case data: live or mock ---
MOCK_CASES_DF = pd.DataFrame([
    {"Case ID": "CASE-7A3F21", "Customer": "Rajesh Kumar", "Alert": "High Volume Inbound", "Risk": "🔴 CRITICAL", "Status": "Draft", "Amount": "₹50,12,000", "Txns": 21, "Date": "Feb 15"},
    {"Case ID": "CASE-B92E44", "Customer": "Meridian Trading LLC", "Alert": "Shell Company Round-Trip", "Risk": "🔴 CRITICAL", "Status": "Review", "Amount": "₹2,34,00,000", "Txns": 83, "Date": "Feb 14"},
    {"Case ID": "CASE-D1F087", "Customer": "Anita Chauhan", "Alert": "Sub-Threshold Deposits", "Risk": "🟠 HIGH", "Status": "Approved", "Amount": "₹9,85,000", "Txns": 12, "Date": "Feb 13"},
    {"Case ID": "CASE-E4C5A2", "Customer": "Vikram Malhotra", "Alert": "Unusual Wire Pattern", "Risk": "🟡 MEDIUM", "Status": "Draft", "Amount": "₹15,40,000", "Txns": 7, "Date": "Feb 16"},
])

cases_df = MOCK_CASES_DF  # default

if backend_online:
    live_cases, err = list_cases()
    if live_cases and not err:
        risk_map = {"critical": "🔴 CRITICAL", "high": "🟠 HIGH", "medium": "🟡 MEDIUM", "low": "🟢 LOW"}
        rows = []
        for lc in live_cases:
            rows.append({
                "Case ID": lc.get("case_id", ""),
                "Customer": lc.get("customer_name", "Unknown"),
                "Alert": lc.get("alert_type", "Suspicious Transaction"),
                "Risk": risk_map.get(lc.get("risk_level", "medium"), "🟡 MEDIUM"),
                "Status": lc.get("sar_status", "draft").capitalize(),
                "Amount": "—",
                "Txns": "—",
                "Date": lc.get("created_at", "")[:10],
            })
        if rows:
            live_df = pd.DataFrame(rows)
            # Merge: live first, then mock cases not already in live
            live_ids = set(live_df["Case ID"])
            mock_extra = MOCK_CASES_DF[~MOCK_CASES_DF["Case ID"].isin(live_ids)]
            cases_df = pd.concat([live_df, mock_extra], ignore_index=True)

# Tabs
tab_cases, tab_analytics, tab_alerts = st.tabs(["🗂️ All Cases", "📈 Analytics", "🚨 Alerts"])

with tab_cases:
    st.dataframe(cases_df, use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🏷️ Status Breakdown")
        # Compute from actual data
        status_counts = cases_df["Status"].value_counts()
        for status_name in ["Draft", "Review", "Approved", "Rejected"]:
            count = status_counts.get(status_name, 0)
            icon = {"Draft": "📝", "Review": "🔍", "Approved": "✅", "Rejected": "❌"}.get(status_name, "•")
            st.markdown(f"- {icon} **{status_name}:** {count} case(s)")

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
