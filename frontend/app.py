"""
SAR Narrative Generator — Streamlit Frontend (Demo-Ready + API Wired)
Full working prototype with realistic mock data fallback + live backend integration.

Owner: SIDDH ONLY
"""
import streamlit as st
import time
import json
import pandas as pd
from datetime import datetime
import sys, os

# Ensure frontend directory is on path for api_client import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_client import is_backend_available, get_system_status, upload_file, generate_sar, list_cases

# Page config
st.set_page_config(
    page_title="SAR Narrative Generator",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Initialize session state ---
if "generated_sar" not in st.session_state:
    st.session_state.generated_sar = None
if "uploaded_case_id" not in st.session_state:
    st.session_state.uploaded_case_id = None
if "sar_id" not in st.session_state:
    st.session_state.sar_id = None

# --- MOCK DATA (Realistic fallback for demo) ---
# --- MOCK DATA (Fallback ONLY when backend is offline) ---
MOCK_CASES = [
    {
        "case_id": "DEMO-7A3F21",
        "customer_name": "Rajesh Kumar (Offline Demo)",
        "alert_type": "High Volume Inbound Transfers",
        "risk_level": "🔴 CRITICAL",
        "sar_status": "Draft",
        "total_amount": "₹50,12,000",
        "txn_count": 21,
        "created_at": "2026-02-15 10:30",
    },
]

# Custom CSS with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Fade-in animation */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        animation: fadeInUp 0.6s ease-out;
    }
    .sub-header {
        font-size: 1rem;
        color: #8b949e;
        margin-top: 0;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.7s ease-out;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.5s ease-out both;
    }
    .metric-card:nth-child(1) { animation-delay: 0.1s; }
    .metric-card:nth-child(2) { animation-delay: 0.2s; }
    .metric-card:nth-child(3) { animation-delay: 0.3s; }
    .metric-card:nth-child(4) { animation-delay: 0.4s; }
    .metric-card:nth-child(5) { animation-delay: 0.5s; }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
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
        transition: border-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.5s ease-out both;
    }
    .case-card:hover {
        border-color: #667eea;
        transform: translateX(4px);
        box-shadow: -4px 0 15px rgba(102, 126, 234, 0.1);
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        transition: transform 0.2s ease;
    }
    .badge:hover { transform: scale(1.05); }
    .badge-draft { background: #1f2937; color: #fbbf24; border: 1px solid #fbbf24; }
    .badge-review { background: #1e3a5f; color: #60a5fa; border: 1px solid #60a5fa; }
    .badge-approved { background: #064e3b; color: #34d399; border: 1px solid #34d399; }
    .risk-critical { animation: pulse 2s infinite; }
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    .status-online { background: #34d399; }
    .status-offline { background: #f87171; animation: none; }
    .api-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 4px;
    }
    .api-badge-live { background: #064e3b; color: #34d399; border: 1px solid #34d399; }
    .api-badge-mock { background: #1f2937; color: #fbbf24; border: 1px solid #fbbf24; }
</style>
""", unsafe_allow_html=True)

# --- Check backend status ---
backend_online = is_backend_available()
status = get_system_status()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🏦 SAR Generator")
    st.markdown("*AI-Powered Compliance*")
    st.markdown("---")

    st.markdown("### ⚙️ System Status")
    for label, key in [("Backend API", "backend"), ("Ollama LLM", "ollama"), ("ChromaDB", "chromadb"), ("PostgreSQL", "postgres")]:
        is_up = status.get(key, False)
        dot_class = "status-online" if is_up else "status-offline"
        status_text = "Online" if is_up else "Offline"
        st.markdown(f'<span class="status-dot {dot_class}"></span> {label}: `{status_text}`', unsafe_allow_html=True)
    
    st.markdown("---")
    if backend_online:
        st.markdown('<span class="api-badge api-badge-live">● LIVE MODE</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="api-badge api-badge-mock">◌ DEMO MODE</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Model:** Llama 3.1 8B Instruct")
    st.markdown("**RAG Docs:** 47 indexed")
    st.markdown("**Avg Gen Time:** ~45 sec")
    st.markdown("---")
    st.markdown("👤 **Analyst:** Siddh")
    st.markdown("🔑 **Role:** Admin")

# --- MAIN PAGE ---
st.markdown('<p class="main-header">🏦 SAR Narrative Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered Suspicious Activity Report drafting with complete audit trail & regulatory compliance</p>', unsafe_allow_html=True)

# --- FETCH DATA ---
display_cases = []
if backend_online:
    live_cases, err = list_cases()
    if live_cases:
        for lc in live_cases:
            risk_map = {"critical": "🔴 CRITICAL", "high": "🟠 HIGH", "medium": "🟡 MEDIUM", "low": "🟢 LOW"}
            display_cases.append({
                "case_id": lc.get("case_id", ""),
                "customer_name": lc.get("customer_name", "Unknown"),
                "alert_type": lc.get("alert_type", "Suspicious Transaction"),
                "risk_level": risk_map.get(lc.get("risk_level", "medium"), "🟡 MEDIUM"),
                "sar_status": lc.get("sar_status", "draft").capitalize(),
                "total_amount": "—", # API doesn't return this yet in list view
                "txn_count": "—",
                "created_at": lc.get("created_at", datetime.now().isoformat()),
            })
else:
    display_cases = MOCK_CASES

# Calculate Metrics
total_cases = len(display_cases)
status_counts = {"Draft": 0, "Review": 0, "Approved": 0}
risk_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

for c in display_cases:
    s = c.get("sar_status", "Draft")
    status_counts[s] = status_counts.get(s, 0) + 1
    
    r = c.get("risk_level", "").split(" ")[-1].capitalize() # Extract "CRITICAL" from "🔴 CRITICAL"
    if r in risk_counts:
        risk_counts[r] += 1

# Metrics row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{total_cases}</div>
        <div class="metric-label">Total Cases</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value metric-value-yellow">{status_counts['Draft']}</div>
        <div class="metric-label">SARs Drafted</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value metric-value-red">{status_counts['Review']}</div>
        <div class="metric-label">Pending Review</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value metric-value-green">{status_counts['Approved']}</div>
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
            uploaded_file.seek(0)  # Reset for API upload

        if st.button("🤖 Generate SAR Narrative", type="primary", use_container_width=True):
            if backend_online:
                # --- LIVE MODE: Call real API ---
                with st.spinner("📤 Uploading to backend..."):
                    upload_data, upload_err = upload_file(uploaded_file)
                
                if upload_err:
                    st.error(f"Upload failed: {upload_err}")
                else:
                    case_id = upload_data["case_id"]
                    st.session_state.uploaded_case_id = case_id
                    st.toast(f"✅ Data uploaded — {upload_data.get('transaction_count', 0)} transactions parsed", icon="📤")
                    
                    progress = st.progress(0, text="🤖 Generating SAR narrative via AI pipeline...")
                    steps = [
                        (15, "🔍 Data Analyst Agent: Analyzing patterns..."),
                        (35, "📋 Compliance Agent: Matching typologies..."),
                        (55, "📖 RAG: Retrieving regulatory templates..."),
                        (75, "✍️ Narrator Agent: Generating narrative..."),
                        (90, "✅ QA Agent: Validating completeness..."),
                    ]
                    for pct, msg in steps:
                        progress.progress(pct, text=msg)
                        time.sleep(0.5)
                    
                    sar_data, sar_err = generate_sar(case_id)
                    progress.progress(100, text="✨ Complete!")
                    
                    if sar_err:
                        st.warning(f"⚠️ Generation issue: {sar_err}. Showing demo narrative.")
                    else:
                        st.session_state.generated_sar = sar_data
                        st.session_state.sar_id = sar_data.get("sar_id")
                        st.success(f"🎉 **SAR Generated!** (ID: `{sar_data.get('sar_id')}`) → Navigate to **SAR Editor** to review.")
                        st.balloons()
            else:
                # --- DEMO MODE: Simulate with mock animation ---
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
                st.toast("Demo mode — backend not connected", icon="ℹ️")
                st.balloons()

with col_right:
    st.markdown("### 🚨 Active Cases")
    
    # Display cases (already fetched above)
    if not display_cases:
        st.info("No active cases found. Upload data to get started.")

    for i, case in enumerate(display_cases):
        badge_class = {
            "Draft": "badge-draft",
            "Review": "badge-review",
            "Approved": "badge-approved",
        }.get(case["sar_status"], "badge-draft")
        
        risk_extra = ' class="risk-critical"' if "CRITICAL" in str(case.get("risk_level", "")) else ""

        st.markdown(f"""
        <div class="case-card" style="animation-delay: {i * 0.1}s;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color:#c9d1d9;">{case['customer_name']}</strong>
                <span class="badge {badge_class}">{case['sar_status']}</span>
            </div>
            <div style="color:#8b949e; font-size:0.8rem; margin-top:4px;">
                {case['case_id']} · {case['alert_type']}
            </div>
            <div style="display:flex; gap:1.5rem; margin-top:8px; font-size:0.85rem;">
                <span{risk_extra} style="color:#f87171;">{case['risk_level']}</span>
                <span style="color:#8b949e;">💰 {case.get('total_amount', '—')}</span>
                <span style="color:#8b949e;">📊 {case.get('txn_count', '—')} txns</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Quick stats
st.markdown("### 📈 System Analytics")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### Risk Distribution")
    risk_df = pd.DataFrame(list(risk_counts.items()), columns=["Risk Level", "Cases"])
    st.bar_chart(risk_df.set_index("Risk Level"), color="#667eea")

with c2:
    st.markdown("#### SAR Status Overview")
    status_df = pd.DataFrame(list(status_counts.items()), columns=["Status", "Count"])
    st.bar_chart(status_df.set_index("Status"), color="#34d399")

with c3:
    st.markdown("#### Recent Activity")
    # Sort by created_at desc
    sorted_cases = sorted(display_cases, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
    
    activity_html = ""
    for c in sorted_cases:
        ts = c.get("created_at", "").split("T")[-1][:5] # Extract HH:MM
        status_icon = "🟢"
        if c['sar_status'] == "Review": status_icon = "🔵"
        if c['sar_status'] == "Approved": status_icon = "✅"
        
        activity_html += f"- {status_icon} **{ts}** — {c['case_id']} ({c['sar_status']})\n"
        
    if not activity_html:
        activity_html = "*No recent activity*"
        
    st.markdown(activity_html)

st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#484f58; font-size:0.8rem;">SAR Narrative Generator v0.1.0 · Powered by Llama 3.1 8B + LangChain + ChromaDB · Hack-O-Hire 2026</p>',
    unsafe_allow_html=True,
)
