"""
SAR Editor — Review, edit, and export SAR narratives.
Owner: SIDDH ONLY
"""
import streamlit as st
import sys, os
import requests
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from api_client import (
    is_backend_available,
    list_cases,
    get_sar,
    update_sar,
    generate_sar,
    approve_sar,
    API_BASE
)

st.set_page_config(page_title="Editor | SAR Generator", page_icon="📝", layout="wide")

# --- CSS Injection ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    .stApp { background-color: #050505; font-family: 'Outfit', sans-serif; color: #e0e0e0; }
    .stTextArea textarea { background-color: #101018; color: #e0e0e0; border: 1px solid #303040; }
    .stButton > button { background: linear-gradient(45deg, #00f2ff, #7000ff); border: none; color: white; }
    .chat-msg { padding: 10px; border-radius: 8px; margin-bottom: 8px; }
    .chat-user { background: #16213e; text-align: right; border-left: 4px solid #00f2ff; }
    .chat-ai { background: #1a1a2e; border-left: 4px solid #7000ff; }
</style>
""", unsafe_allow_html=True)

st.title("📝 SAR Editor")

backend_online = is_backend_available()

# --- Select Case ---
cases, _ = list_cases()
case_options = {f"{c['case_id']} - {c['customer_name']}": c['case_id'] for c in cases} if cases else {}

if not case_options:
    st.warning("No cases found or backend offline.")
    # Mock for UI testing
    case_options = {"CASE-MOCK-001 - Test User": "CASE-MOCK-001"}

selected_label = st.selectbox("Select Case", list(case_options.keys()))
selected_case_id = case_options[selected_label]

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Main Layout ---
col_editor, col_sidebar = st.columns([2, 1])

with col_editor:
    st.subheader("Narrative Editor")
    
    # Fetch SAR Data
    sar_data = None
    if backend_online and selected_case_id:
        # Check if SAR exists in session or fetch
        # Simplified logic for demo
        pass
    
    # Check if we have data to show, otherwise show generation button
    # Check if we have data to show, otherwise show generation button
    col_gen_btn, col_roi = st.columns([1, 2])
    
    start_gen = False
    with col_gen_btn:
        if st.button("Generate / Refresh Narrative"):
            start_gen = True
            
    with col_roi:
        if not sar_data and not start_gen:
             st.markdown("⚡ **Expected Time Savings:** ~5 hours vs manual drafting")

    if start_gen:
        with st.spinner("Generating SAR..."):
            sar_data = generate_sar(selected_case_id)
    else:
         sar_data, _ = get_sar(selected_case_id) if backend_online else (None, "Offline")
    
    if sar_data:
        narrative = sar_data.get("narrative", {})
        
        # Tabs for sections
        t1, t2, t3 = st.tabs(["Introduction", "Body (Analysis)", "Conclusion"])
        
        with t1:
            intro_edit = st.text_area("Introduction", narrative.get("introduction", ""), height=150)
        with t2:
            body_edit = st.text_area("Body", narrative.get("body", ""), height=400)
        with t3:
            conc_edit = st.text_area("Conclusion", narrative.get("conclusion", ""), height=150)
            
        # Actions
        c_act1, c_act2, c_act3 = st.columns(3)
        if c_act1.button("💾 Save Draft"):
            # Update logic
            new_narrative = {"introduction": intro_edit, "body": body_edit, "conclusion": conc_edit}
            update_sar(sar_data["sar_id"], intro_edit, body_edit, conc_edit)
            st.success("Draft saved!")
            
        if c_act2.button("✅ Approve & File"):
            approve_sar(sar_data["sar_id"])
            st.success("SAR Approved and Filed!")
            st.balloons()
            
        if c_act3.button("📥 Export PDF"):
            # Call PDF Export API
            with st.spinner("Generating PDF..."):
                try:
                    r = requests.post(f"{API_BASE}/export-pdf", json={"case_id": selected_case_id})
                    if r.status_code == 200:
                        st.download_button(
                            label="Download PDF",
                            data=r.content,
                            file_name=f"SAR_{selected_case_id}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error(f"Export failed: {r.text}")
                except Exception as e:
                    st.error(f"Export error: {e}")
    else:
        st.info("Click 'Generate' to create the SAR for this case.")

with col_sidebar:
    st.subheader("💬 AI Copilot")
    
    # Chat Interface
    chat_container = st.container()
    user_input = st.text_input("Ask about this case...", key="chat_input")
    
    if st.button("Send", key="send_chat") and user_input:
        # Add user msg
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get response
        try:
            payload = {
                "case_id": selected_case_id,
                "query": user_input,
                "history": st.session_state.chat_history[-5:] # Send recent history
            }
            r = requests.post(f"{API_BASE}/chat", json=payload)
            if r.status_code == 200:
                ai_msg = r.json().get("response", "No response")
            else:
                ai_msg = f"Error: {r.text}"
        except Exception as e:
            ai_msg = f"Connection error: {e}"
            
        # Add AI msg
        st.session_state.chat_history.append({"role": "assistant", "content": ai_msg})
        
    # Display Chat
    with chat_container:
        for msg in st.session_state.chat_history:
            role_class = "chat-user" if msg["role"] == "user" else "chat-ai"
            st.markdown(f'<div class="chat-msg {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# --- Quality Score (Floating or Bottom) ---
if sar_data:
    q = sar_data.get("quality_score") or {}
    st.markdown("---")
    st.markdown("#### 🏆 Quality Assurance")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Completeness", f"{q.get('completeness', 0):.0%}")
    c2.metric("Compliance", f"{q.get('compliance', 0):.0%}")
    c3.metric("Readability", f"{q.get('readability', 0):.0%}")
    c4.metric("Evidence Link", f"{q.get('evidence_linkage', 0):.0%}")
