"""
SAR Narrative Generator — Streamlit Frontend (Demo-Ready)
Full working prototype with realistic mock data for video demo.

Owner: Het (P3) — Shubh building demo version
"""
import streamlit as st
import time
import json
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SAR Narrative Generator",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- MOCK DATA (Realistic for demo) ---
MOCK_CASES = [
    {
        "case_id": "CASE-7A3F21",
        "customer_name": "Rajesh Kumar",
        "alert_type": "High Volume Inbound Transfers",
        "risk_level": "🔴 CRITICAL",
        "sar_status": "Draft",
        "total_amount": "₹50,12,000",
        "txn_count": 21,
        "created_at": "2026-02-15 10:30",
    },
    {
        "case_id": "CASE-B92E44",
        "customer_name": "Meridian Trading LLC",
        "alert_type": "Shell Company Round-Tripping",
        "risk_level": "🔴 CRITICAL",
        "sar_status": "Review",
        "total_amount": "₹2,34,00,000",
        "txn_count": 83,
        "created_at": "2026-02-14 16:45",
    },
    {
        "case_id": "CASE-D1F087",
        "customer_name": "Anita Chauhan",
        "alert_type": "Sub-Threshold Cash Deposits",
        "risk_level": "🟠 HIGH",
        "sar_status": "Approved",
        "total_amount": "₹9,85,000",
        "txn_count": 12,
        "created_at": "2026-02-13 09:15",
    },
    {
        "case_id": "CASE-E4C5A2",
        "customer_name": "Vikram Malhotra",
        "alert_type": "Unusual Wire Transfer Pattern",
        "risk_level": "🟡 MEDIUM",
        "sar_status": "Draft",
        "total_amount": "₹15,40,000",
        "txn_count": 7,
        "created_at": "2026-02-16 11:20",
    },
]

MOCK_SAR_NARRATIVE = {
    "introduction": """This Suspicious Activity Report (SAR) is being filed by HDFC Bank Ltd. to report suspicious transaction activity involving account holder Rajesh Kumar, account number XXXX-4521. The activity, observed between January 15–22, 2026, is consistent with structuring/smurfing patterns involving the receipt of funds from multiple unrelated sources followed by immediate international transfer. This is the initial SAR filing on this subject. Internal Investigation Reference: CASE-7A3F21.""",

    "body": """**WHO:** The subject, Rajesh Kumar (PAN: XXXXX1234K), has maintained a Current Account (XXXX-4521) with HDFC Bank, Andheri West Branch, Mumbai, since March 2019. KYC verification status: Verified (last updated: September 2025). The subject's declared occupation is Textile Export with a registered firm "Kumar Textiles" (GST: 27XXXXX1234K1ZF). Historical average monthly transaction volume: ₹3,00,000.

**WHAT:** During the review period, the account received 20 inbound transfers totaling ₹50,12,000 from 20 unique sender accounts across 14 different banks. The individual transfer amounts ranged from ₹76,000 to ₹1,45,000 — predominantly below the ₹10,00,000 reporting threshold when viewed individually. Within 48 hours of the last inbound credit, the subject initiated a single outbound SWIFT transfer of ₹48,00,000 to Deutsche Bank AG, Frankfurt (Account: DB-INTL-9999), with the stated purpose "Trade Settlement — Fabric Import."

**WHEN:** The suspicious inbound activity occurred over a 5-day window from January 15–19, 2026. Transfers were received at regular intervals during banking hours (9:00 AM – 3:00 PM IST). The consolidation and outbound international transfer occurred on January 20, 2026, at 10:00 AM IST — the first business day following the final inbound credit.

**WHERE:** All inbound transfers were processed through the HDFC Bank NEFT/RTGS clearing system, originating from 14 different banks including SBI, ICICI, Axis, PNB, Bank of Baroda, Kotak Mahindra, and others across multiple states (Maharashtra, Gujarat, Delhi, Karnataka, Tamil Nadu). The outbound transfer was routed through HDFC Bank's SWIFT gateway to Deutsche Bank AG, Frankfurt, Germany.

**WHY:** The transaction pattern is highly inconsistent with the subject's declared business profile:
• Monthly volume spike: 16.7x above the declared average (₹50.12L vs. ₹3L/month)
• 20 unique senders with no prior transaction history with the subject
• No corresponding trade documentation or invoices supporting the "Trade Settlement" purpose
• Immediate consolidation and international transfer within 48 hours
• Pattern matches known structuring/smurfing typology: aggregation of sub-threshold amounts from multiple sources to disguise the origin of funds before layering through international channels

**HOW:** Funds were received via NEFT (17 transfers) and RTGS (3 transfers) from 20 distinct accounts held at 14 banks. The sender accounts showed no prior relationship with the subject. After consolidation in account XXXX-4521, ₹48,00,000 was transferred internationally via SWIFT to a Deutsche Bank account in Frankfurt. The remaining ₹2,12,000 was retained in the account. The method of operation is consistent with smurfing — using multiple low-value transfers from different sources to avoid individual transaction reporting thresholds, followed by rapid international transfer to obscure the audit trail.""",

    "conclusion": """Based on the analysis detailed above, HDFC Bank Ltd. has determined that the transaction activity associated with account holder Rajesh Kumar (Account: XXXX-4521) warrants filing of this SAR with FIU-IND. The institution has implemented the following actions: (1) Enhanced transaction monitoring on the subject's account, (2) Placed a temporary hold on international transfer privileges pending investigation, (3) Initiated internal review of the subject's KYC documentation and trade-related records, (4) Flagged all 20 sender accounts for cross-referencing in the bank's AML system. All supporting documentation, including transaction records, KYC files, and SWIFT messages, are maintained at HDFC Bank Compliance Division, BKC Mumbai, and are available upon request. For additional information, contact: AML Compliance Officer, compliance@hdfcbank.com, +91-22-XXXX-XXXX."""
}

MOCK_AUDIT_TRAIL = [
    {
        "step": 1,
        "agent": "🔍 Data Analyst Agent",
        "action": "Analyzed 21 transactions for account XXXX-4521",
        "data_points": ["20 inbound transfers from 20 unique senders", "Total inbound: ₹50,12,000", "1 outbound SWIFT: ₹48,00,000", "Time window: 5 days (Jan 15-19)", "Outbound within 48 hrs of last credit"],
        "output": "HIGH-RISK PATTERN DETECTED: Multiple sub-threshold inbound transfers from unrelated senders, followed by immediate international consolidation transfer. Volume 16.7x above declared average.",
        "confidence": 0.96,
    },
    {
        "step": 2,
        "agent": "📋 Compliance Mapper Agent",
        "action": "Matched transaction patterns to regulatory typologies",
        "data_points": ["FinCEN Advisory FIN-2024-A003 (Structuring)", "RBI Master Direction Sec 14.2 (Suspicious Patterns)", "FATF Typology: ML/TF Red Flag Indicator #23"],
        "output": "PRIMARY TYPOLOGY: Structuring/Smurfing (Confidence: 94%). SECONDARY: Layering via international wire (Confidence: 87%). Matched 3 regulatory references.",
        "confidence": 0.94,
    },
    {
        "step": 3,
        "agent": "📖 RAG Context Retriever",
        "action": "Retrieved regulatory templates and similar past SARs",
        "data_points": ["SAR Template T-005 (Structuring)", "FinCEN Narrative Guidance (5Ws+How)", "Similar SAR: CASE-2025-8821 (89% similarity)"],
        "output": "Retrieved 3 relevant documents. Template T-005 selected as primary narrative framework. Past SAR CASE-2025-8821 used as reference for language patterns.",
        "confidence": 0.91,
    },
    {
        "step": 4,
        "agent": "✍️ Narrator Agent",
        "action": "Generated FinCEN-compliant SAR narrative",
        "data_points": ["Structure: Introduction → Body (5Ws+How) → Conclusion", "Word count: 847 words", "All 5Ws addressed", "Evidence-linked throughout"],
        "output": "Draft SAR narrative generated in FinCEN format. All six elements (Who, What, When, Where, Why, How) addressed with specific data point citations. Three-part structure maintained.",
        "confidence": 0.93,
    },
    {
        "step": 5,
        "agent": "✅ QA Validator Agent",
        "action": "Validated narrative completeness, compliance, and quality",
        "data_points": ["Completeness: 95% (all required elements present)", "Compliance: 98% (FinCEN format met)", "Readability: Flesch-Kincaid Grade 12.1", "Evidence Linkage: 91% (43/47 claims backed)"],
        "output": "PASSED: Narrative meets quality thresholds. Minor suggestion: Add sender geographic distribution detail in WHERE section. Overall quality score: 93/100.",
        "confidence": 0.95,
    },
]

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #8b949e;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #58a6ff;
    }
    .metric-value-green { color: #34d399; }
    .metric-value-yellow { color: #fbbf24; }
    .metric-value-red { color: #f87171; }
    .metric-label {
        font-size: 0.85rem;
        color: #8b949e;
        margin-top: 0.3rem;
    }
    .case-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        transition: border-color 0.2s;
    }
    .case-card:hover {
        border-color: #667eea;
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-draft { background: #1f2937; color: #fbbf24; border: 1px solid #fbbf24; }
    .badge-review { background: #1e3a5f; color: #60a5fa; border: 1px solid #60a5fa; }
    .badge-approved { background: #064e3b; color: #34d399; border: 1px solid #34d399; }
    .audit-step {
        background: #161b22;
        border-left: 3px solid #667eea;
        border-radius: 0 8px 8px 0;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .confidence-bar {
        height: 6px;
        border-radius: 3px;
        background: #21262d;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 3px;
        background: linear-gradient(90deg, #667eea, #34d399);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🏦 SAR Generator")
    st.markdown("*AI-Powered Compliance*")
    st.markdown("---")

    st.markdown("### ⚙️ System Status")
    st.markdown("🟢 Backend API: `Online`")
    st.markdown("🟢 Ollama LLM: `Running`")
    st.markdown("🟢 ChromaDB: `Connected`")
    st.markdown("🟢 PostgreSQL: `Connected`")
    st.markdown("---")
    st.markdown("**Model:** Llama 3.1 8B Instruct")
    st.markdown("**RAG Docs:** 47 indexed")
    st.markdown("**Avg Gen Time:** ~45 sec")
    st.markdown("---")
    st.markdown("👤 **Analyst:** Shubh")
    st.markdown("🔑 **Role:** Admin")

# --- MAIN PAGE ---
st.markdown('<p class="main-header">🏦 SAR Narrative Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered Suspicious Activity Report drafting with complete audit trail & regulatory compliance</p>', unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""<div class="metric-card">
        <div class="metric-value">4</div>
        <div class="metric-label">Total Cases</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="metric-card">
        <div class="metric-value metric-value-yellow">3</div>
        <div class="metric-label">SARs Drafted</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="metric-card">
        <div class="metric-value metric-value-red">1</div>
        <div class="metric-label">Pending Review</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class="metric-card">
        <div class="metric-value metric-value-green">1</div>
        <div class="metric-label">Approved</div>
    </div>""", unsafe_allow_html=True)
with col5:
    st.markdown("""<div class="metric-card">
        <div class="metric-value">~45s</div>
        <div class="metric-label">Avg Gen Time</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# Two-column layout
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 📥 Upload Transaction Data")
    uploaded_file = st.file_uploader(
        "Upload CSV or JSON file with transaction alerts + KYC data",
        type=["csv", "json"],
        help="Expected columns: txn_id, sender, receiver, amount, currency, timestamp, type",
    )

    if uploaded_file:
        st.success(f"✅ **{uploaded_file.name}** uploaded ({uploaded_file.size / 1024:.1f} KB)")
        
        # Show preview
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            st.markdown("#### 📊 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            st.markdown(f"*{len(df)} transactions loaded*")

        if st.button("🤖 Generate SAR Narrative", type="primary", use_container_width=True):
            progress = st.progress(0, text="Initializing AI pipeline...")
            
            steps = [
                (10, "📥 Ingesting transaction data..."),
                (25, "🔍 Data Analyst Agent: Analyzing patterns..."),
                (40, "📋 Compliance Agent: Matching typologies..."),
                (55, "📖 RAG: Retrieving regulatory templates..."),
                (70, "✍️ Narrator Agent: Generating SAR narrative..."),
                (85, "✅ QA Agent: Validating completeness..."),
                (95, "💾 Saving to database..."),
                (100, "✨ SAR narrative generated!"),
            ]
            
            for pct, msg in steps:
                progress.progress(pct, text=msg)
                time.sleep(0.8)
            
            st.success("🎉 **SAR Narrative Generated!** Navigate to the **SAR Editor** page to review.")
            st.balloons()

with col_right:
    st.markdown("### 🚨 Active Cases")
    
    for case in MOCK_CASES:
        badge_class = {
            "Draft": "badge-draft",
            "Review": "badge-review",
            "Approved": "badge-approved",
        }.get(case["sar_status"], "badge-draft")

        st.markdown(f"""
        <div class="case-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color:#c9d1d9;">{case['customer_name']}</strong>
                <span class="badge {badge_class}">{case['sar_status']}</span>
            </div>
            <div style="color:#8b949e; font-size:0.8rem; margin-top:4px;">
                {case['case_id']} · {case['alert_type']}
            </div>
            <div style="display:flex; gap:1.5rem; margin-top:8px; font-size:0.85rem;">
                <span style="color:#f87171;">{case['risk_level']}</span>
                <span style="color:#8b949e;">💰 {case['total_amount']}</span>
                <span style="color:#8b949e;">📊 {case['txn_count']} txns</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Quick stats
st.markdown("### 📈 System Analytics")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### Risk Distribution")
    risk_data = pd.DataFrame({
        "Risk Level": ["Critical", "High", "Medium", "Low"],
        "Cases": [2, 1, 1, 0],
    })
    st.bar_chart(risk_data.set_index("Risk Level"), color="#667eea")

with c2:
    st.markdown("#### SAR Status Overview")
    status_data = pd.DataFrame({
        "Status": ["Draft", "Review", "Approved"],
        "Count": [2, 1, 1],
    })
    st.bar_chart(status_data.set_index("Status"), color="#34d399")

with c3:
    st.markdown("#### Recent Activity")
    st.markdown("""
    - 🟢 **10:30** — CASE-7A3F21 created
    - 🔵 **16:45** — CASE-B92E44 → Review  
    - ✅ **09:15** — CASE-D1F087 Approved
    - 🟡 **11:20** — CASE-E4C5A2 created
    """)

st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#484f58; font-size:0.8rem;">SAR Narrative Generator v0.1.0 · Powered by Llama 3.1 8B + LangChain + ChromaDB · Hack-O-Hire 2026</p>',
    unsafe_allow_html=True,
)
