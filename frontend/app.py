"""
SAR Narrative Generator — Streamlit Frontend

Owner: P3
"""
import streamlit as st

# Page config
st.set_page_config(
    page_title="SAR Narrative Generator",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #8b949e;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #58a6ff;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8b949e;
        margin-top: 0.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-draft { background: #1f2937; color: #fbbf24; border: 1px solid #fbbf24; }
    .badge-review { background: #1e3a5f; color: #60a5fa; border: 1px solid #60a5fa; }
    .badge-approved { background: #064e3b; color: #34d399; border: 1px solid #34d399; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank-building.png", width=60)
    st.markdown("## SAR Generator")
    st.markdown("---")
    st.markdown("### Navigation")
    st.markdown("Use the pages in the sidebar to navigate:")
    st.markdown("- 📊 **Dashboard** — Overview")
    st.markdown("- 📝 **SAR Editor** — Draft & edit")
    st.markdown("- 🔍 **Audit Trail** — Explainability")
    st.markdown("---")
    st.markdown("### System Status")
    st.success("🟢 Backend: Connected")
    st.success("🟢 Ollama: Running")
    st.info("🔵 Model: Llama 3.1 8B")

# Main content
st.markdown('<p class="main-header">SAR Narrative Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered Suspicious Activity Report drafting with complete audit trail</p>', unsafe_allow_html=True)

st.markdown("---")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">0</div>
        <div class="metric-label">Total Cases</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">0</div>
        <div class="metric-label">SARs Drafted</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">0</div>
        <div class="metric-label">Pending Review</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">0</div>
        <div class="metric-label">Approved</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick actions
st.markdown("### 🚀 Quick Actions")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### 📥 Upload Data")
    uploaded_file = st.file_uploader(
        "Upload transaction alerts (CSV or JSON)",
        type=["csv", "json"],
        help="Upload transaction data with customer KYC information",
    )
    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        if st.button("🤖 Generate SAR Narrative", type="primary"):
            with st.spinner("Generating SAR narrative with AI..."):
                st.info("SAR generation will be available once the LLM engine is connected.")

with col_b:
    st.markdown("#### 📋 Recent Activity")
    st.info("No cases uploaded yet. Upload transaction data to get started.")


# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #484f58;">SAR Narrative Generator v0.1.0 | Hack-O-Hire 2026</p>',
    unsafe_allow_html=True,
)
