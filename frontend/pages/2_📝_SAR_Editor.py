"""
SAR Editor — Review, edit, and approve AI-generated SAR narratives.
Owner: Het
"""
import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="SAR Editor | SAR Generator", page_icon="📝", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    .score-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
    }
    .score-value { font-size: 1.5rem; font-weight: 700; }
    .score-label { font-size: 0.75rem; color: #8b949e; }
</style>
""", unsafe_allow_html=True)

# --- Pre-filled SAR narrative (realistic) ---
SAR_INTRO = """This Suspicious Activity Report (SAR) is being filed by HDFC Bank Ltd. to report suspicious transaction activity involving account holder Rajesh Kumar, account number XXXX-4521. The activity, observed between January 15–22, 2026, is consistent with structuring/smurfing patterns involving the receipt of funds from multiple unrelated sources followed by immediate international transfer. This is the initial SAR filing on this subject. Internal Investigation Reference: CASE-7A3F21."""

SAR_BODY = """WHO: The subject, Rajesh Kumar (PAN: XXXXX1234K), has maintained a Current Account (XXXX-4521) with HDFC Bank, Andheri West Branch, Mumbai, since March 2019. KYC verification status: Verified (last updated: September 2025). The subject's declared occupation is Textile Export with a registered firm "Kumar Textiles" (GST: 27XXXXX1234K1ZF). Historical average monthly transaction volume: ₹3,00,000.

WHAT: During the review period, the account received 20 inbound transfers totaling ₹50,12,000 from 20 unique sender accounts across 14 different banks. The individual transfer amounts ranged from ₹76,000 to ₹1,45,000 — predominantly below the ₹10,00,000 reporting threshold when viewed individually. Within 48 hours of the last inbound credit, the subject initiated a single outbound SWIFT transfer of ₹48,00,000 to Deutsche Bank AG, Frankfurt (Account: DB-INTL-9999), with the stated purpose "Trade Settlement — Fabric Import."

WHEN: The suspicious inbound activity occurred over a 5-day window from January 15–19, 2026. Transfers were received at regular intervals during banking hours (9:00 AM – 3:00 PM IST). The consolidation and outbound international transfer occurred on January 20, 2026, at 10:00 AM IST.

WHERE: All inbound transfers were processed through the HDFC Bank NEFT/RTGS clearing system, originating from 14 different banks across multiple states (Maharashtra, Gujarat, Delhi, Karnataka, Tamil Nadu). The outbound transfer was routed through HDFC Bank's SWIFT gateway to Deutsche Bank AG, Frankfurt, Germany.

WHY: The transaction pattern is highly inconsistent with the subject's declared business profile. Monthly volume spike: 16.7x above declared average (₹50.12L vs. ₹3L/month). 20 unique senders with no prior history. No supporting trade documentation. Pattern matches known structuring/smurfing typology.

HOW: Funds were received via NEFT (17 transfers) and RTGS (3 transfers) from 20 distinct accounts at 14 banks. After consolidation, ₹48,00,000 was transferred internationally via SWIFT to Frankfurt. The remaining ₹2,12,000 retained."""

SAR_CONCLUSION = """Based on the analysis above, HDFC Bank Ltd. has determined that the transaction activity warrants reporting to FIU-IND. Actions taken: (1) Enhanced monitoring on subject's account, (2) Temporary hold on international transfers, (3) Internal KYC review initiated, (4) All 20 sender accounts flagged for cross-referencing. Supporting documentation maintained at HDFC Bank Compliance Division, BKC Mumbai. Contact: AML Compliance Officer, compliance@hdfcbank.com."""

# --- Transaction data ---
TXN_DATA = pd.DataFrame([
    {"ID": "TXN-001", "Sender": "Amit Sharma", "Receiver": "Rajesh Kumar", "Amount (₹)": "1,20,000", "Bank": "HDFC", "Type": "NEFT", "Date": "Jan 15"},
    {"ID": "TXN-002", "Sender": "Priya Patel", "Receiver": "Rajesh Kumar", "Amount (₹)": "95,000", "Bank": "SBI", "Type": "NEFT", "Date": "Jan 15"},
    {"ID": "TXN-003", "Sender": "Suresh Reddy", "Receiver": "Rajesh Kumar", "Amount (₹)": "1,10,000", "Bank": "BOB", "Type": "RTGS", "Date": "Jan 15"},
    {"ID": "TXN-004", "Sender": "Kavita Desai", "Receiver": "Rajesh Kumar", "Amount (₹)": "88,000", "Bank": "PNB", "Type": "NEFT", "Date": "Jan 15"},
    {"ID": "TXN-005", "Sender": "Ravi Verma", "Receiver": "Rajesh Kumar", "Amount (₹)": "1,45,000", "Bank": "ICICI", "Type": "NEFT", "Date": "Jan 16"},
    {"ID": "TXN-006", "Sender": "Neha Gupta", "Receiver": "Rajesh Kumar", "Amount (₹)": "92,000", "Bank": "Axis", "Type": "NEFT", "Date": "Jan 16"},
    {"ID": "TXN-007", "Sender": "Arun Joshi", "Receiver": "Rajesh Kumar", "Amount (₹)": "1,30,000", "Bank": "UCO", "Type": "RTGS", "Date": "Jan 16"},
    {"ID": "TXN-021", "Sender": "Rajesh Kumar", "Receiver": "Deutsche Bank Frankfurt", "Amount (₹)": "48,00,000", "Bank": "SWIFT", "Type": "Wire", "Date": "Jan 20"},
])

# --- PAGE ---
st.markdown("# 📝 SAR Narrative Editor")

# Case selector
case_id = st.selectbox(
    "Select Case",
    ["CASE-7A3F21 — Rajesh Kumar (Smurfing)", "CASE-B92E44 — Meridian Trading (Layering)", "CASE-D1F087 — Anita Chauhan (Structuring)"],
)

st.markdown("---")

# Quality scores row
sc1, sc2, sc3, sc4, sc5 = st.columns(5)
with sc1:
    st.markdown('<div class="score-card"><div class="score-value" style="color:#34d399;">93</div><div class="score-label">Overall Score</div></div>', unsafe_allow_html=True)
with sc2:
    st.markdown('<div class="score-card"><div class="score-value" style="color:#667eea;">95%</div><div class="score-label">Completeness</div></div>', unsafe_allow_html=True)
with sc3:
    st.markdown('<div class="score-card"><div class="score-value" style="color:#a78bfa;">98%</div><div class="score-label">Compliance</div></div>', unsafe_allow_html=True)
with sc4:
    st.markdown('<div class="score-card"><div class="score-value" style="color:#fbbf24;">88%</div><div class="score-label">Readability</div></div>', unsafe_allow_html=True)
with sc5:
    st.markdown('<div class="score-card"><div class="score-value" style="color:#f87171;">91%</div><div class="score-label">Evidence Link</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Split-screen layout
col_data, col_editor = st.columns([1, 1.3])

with col_data:
    st.markdown("### 📋 Case Data — CASE-7A3F21")
    
    # Customer info
    st.markdown("#### 👤 Customer Profile")
    cust_col1, cust_col2 = st.columns(2)
    with cust_col1:
        st.markdown("**Name:** Rajesh Kumar")
        st.markdown("**Account:** XXXX-4521")
        st.markdown("**KYC:** ✅ Verified")
    with cust_col2:
        st.markdown("**Business:** Textile Export")
        st.markdown("**Avg Monthly:** ₹3,00,000")
        st.markdown("**Risk:** 🔴 CRITICAL")

    # Typology prediction
    st.markdown("---")
    st.markdown("#### 🤖 ML Typology Prediction")
    st.markdown("**Predicted:** `Structuring / Smurfing`")
    st.progress(0.94, text="Confidence: 94%")
    
    st.markdown("**Feature Importance (SHAP):**")
    shap_df = pd.DataFrame({
        "Feature": ["Unique Senders", "Total Amount", "Time Window", "Amount Variance", "International Wire"],
        "Importance": [0.35, 0.28, 0.22, 0.10, 0.05],
    })
    st.bar_chart(shap_df.set_index("Feature"), color="#764ba2")

    # Transaction table
    st.markdown("---")
    st.markdown("#### 💳 Transactions (showing 8 of 21)")
    st.dataframe(TXN_DATA, use_container_width=True, hide_index=True)

with col_editor:
    st.markdown("### ✍️ SAR Narrative")
    st.info("**Typology:** Structuring/Smurfing | **Status:** 📝 Draft | **Generated:** Feb 15, 10:45 AM")

    # Editable narrative
    st.markdown("**INTRODUCTION**")
    intro = st.text_area("Introduction", value=SAR_INTRO, height=120, label_visibility="collapsed")

    st.markdown("**BODY (5Ws + How)**")
    body = st.text_area("Body", value=SAR_BODY, height=350, label_visibility="collapsed")

    st.markdown("**CONCLUSION**")
    conclusion = st.text_area("Conclusion", value=SAR_CONCLUSION, height=120, label_visibility="collapsed")

    # Action buttons
    st.markdown("---")
    btn1, btn2, btn3, btn4 = st.columns(4)
    with btn1:
        if st.button("🔄 Regenerate", use_container_width=True):
            with st.spinner("Regenerating with Llama 3.1..."):
                time.sleep(2)
            st.success("Narrative regenerated!")
    with btn2:
        if st.button("✅ Approve", type="primary", use_container_width=True):
            st.success("✅ SAR approved and sent to FIU-IND!")
            st.balloons()
    with btn3:
        if st.button("❌ Reject", use_container_width=True):
            st.warning("SAR sent back for revision.")
    with btn4:
        if st.button("📄 Export PDF", use_container_width=True):
            st.info("PDF export will be available soon.")

    # Word count
    total_words = len(intro.split()) + len(body.split()) + len(conclusion.split())
    st.caption(f"📊 Word count: {total_words} | Estimated read time: {total_words // 200} min")
