"""
Dashboard Page — Overview of cases, alerts, and SAR statuses.

Owner: P3
"""
import streamlit as st

st.set_page_config(page_title="Dashboard | SAR Generator", page_icon="📊", layout="wide")

st.markdown("# 📊 Dashboard")
st.markdown("Overview of all cases, alerts, and SAR generation statuses.")
st.markdown("---")

# Placeholder content
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚨 Active Alerts")
    st.info("No alerts yet. Upload transaction data to generate alerts.")

with col2:
    st.markdown("### 📄 SARs by Status")
    st.info("No SARs generated yet.")

st.markdown("---")
st.markdown("### 📈 Analytics")
st.info("Analytics will be populated once cases are processed.")
