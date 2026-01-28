"""
🦙 Enterprise AI Knowledge Assistant - Frontend
Powered by Meta Llama 3 8B Instruct
Run: streamlit run app.py
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time
import base64
from PIL import Image

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
try:
    company_logo = Image.open("assets/icon.jpg")
except FileNotFoundError:
    # Fallback if the file path is still tricky
    company_logo = "💜"
# Convert image to base64
img_base64 = get_base64_image("assets/background.jpg")

# PAGE CONFIG
st.set_page_config(
    page_title="Tips Hindawi",
    page_icon=company_logo,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS
st.markdown(f"""
<style>
   .example-btn button {{
        height: 2rem !important;
        font-size: 0.75rem !important;
        border-radius: 6px !important;
        background: #F3E5FF !important;
        color: #5A189A !important;
        border: 1px solid #D0B7FF !important;
        margin-bottom: 0.1rem !important;
        width: 100% !important;
   }}

   .example-btn div {{
        margin-bottom: 0.1rem !important;
   }}

   .example-btn button:hover {{
        background: #E0AAFF !important;
   }}

   div[data-baseweb="textarea"] {{
        border-color: #9D4EDD !important;
        box-shadow: none !important;
   }}
   
   div[data-baseweb="textarea"]:focus-within {{
        border-color: #9D4EDD !important;
        box-shadow: 0 0 0 2px rgba(157, 78, 221, 0.35) !important;
   }}

   div[data-baseweb="textarea"] textarea {{
        outline: none !important;
        box-shadow: none !important;
        caret-color: #9D4EDD;
   }}
    
    .stApp {{
        background-color: #f5f5f5;
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: scroll;
    }}

    .main-header {{
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #E0AAFF  0%, #560BAD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: left;
        margin-bottom: 0.5rem;
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, #9D4EDD, #7209B7);
        color: white;
        border-radius: 10px;
        height: 2rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }}

   .stButton>button:hover {{
        background: linear-gradient(135deg, #B517FF, #560BAD);
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(157, 78, 221, 0.4);
    }}

    .model-badge {{
        text-align: left;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }}

    .answer-box {{
        background: linear-gradient(135deg, #9D4EDD 0%, #7209B7 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(157, 78, 221, 0.3);
        animation: fadeIn 0.5s;
        width:50%;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .answer-text {{
        font-size: 1rem;
        line-height: 1.6;
    }}
    
    html {{
        scroll-behavior: smooth;
    }}
    

    section.main > div {{
        max-width: 10% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}
    
    [data-testid="stHorizontalBlock"] {{
        gap: 0 !important;
    }}
    
    [data-testid="column"]:last-child {{
        position: fixed !important;
        right: 0 !important;
        top: 2rem !important;
        width: 80px !important;
        padding: 0 0.2rem 0 0 !important;
        z-index: 100 !important;
    }}
    
    [data-testid="column"]:first-child {{
        width: calc(100% - 320px) !important;
        padding-right: 0.5rem !important;
    }}
</style>

<script>
    setTimeout(function() {{
        window.scrollTo({{
            top: document.body.scrollHeight,
            behavior: 'smooth'
        }});
    }}, 100);
</script>
""", unsafe_allow_html=True)

# SESSION STATE
if 'history' not in st.session_state:
    st.session_state.history = []

if 'total_queries' not in st.session_state:
    st.session_state.total_queries = 0

if 'total_time' not in st.session_state:
    st.session_state.total_time = 0

if 'current_answer' not in st.session_state:
    st.session_state.current_answer = None

# HARDCODED CONFIGURATION
API_URL = "https://thigmotropic-geraldine-nonelliptically.ngrok-free.dev"
API_KEY = "secret226"

# SIDEBAR
with st.sidebar:
    st.markdown("### 🦙 Llama 3 Assistant")
    st.markdown("---")

    # API Configuration
    st.markdown("## ⚙️ Configuration")

    max_length = st.slider(
        "📏 Max Answer Length",
        min_value=128,
        max_value=2000,
        value=500,
        step=64,
        help="Maximum length for generated answer"
    )

    st.markdown("---")

    # Connection Status
    st.markdown("### 📊 Connection Status")

    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            st.success("✅ API Connected")
            st.info(f"🦙 Model: {health_data.get('model', 'Unknown')}")
            st.session_state.api_connected = True
        else:
            st.error("❌ API Error")
            st.session_state.api_connected = False
    except:
        st.error("❌ Cannot Connect")
        st.caption("Make sure:")
        st.caption("• Kaggle notebook is running")
        st.caption("• ngrok tunnel is active")
        st.session_state.api_connected = False

    st.markdown("---")

    # Actions
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.session_state.total_queries = 0
        st.session_state.total_time = 0
        st.session_state.current_answer = None
        st.rerun()

    if st.button("🔄 Refresh"):
        st.rerun()

# MAIN HEADER
# Assuming your purple icon is saved as 'assets/icon.png' (PNG is better for transparency)
# If the file is in the same folder as app.py and named 'unnamed-removebg-preview.png'
st.markdown(
    f"""
    <div class="main-header" style="display: flex; align-items: center; gap: 15px;">
        <img src="data:image/png;base64,{get_base64_image('assets\icon.jpg')}" width="50">
        <span style="font-size: 2.5rem; font-weight: bold;">Enterprise AI Assistant | Tips Hindawi</span>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown('<div class="model-badge"><strong>Your Smart Assistant | Online </strong></div>', unsafe_allow_html=True)

# MAIN CONTENT
def set_question(q):
    st.session_state["question_input"] = q
    st.session_state.current_answer = None

col_left, col_right = st.columns([3, 1])

with col_left:
    st.markdown("### Hello 👋 How can I help you today?")

    if "question_input" not in st.session_state:
        st.session_state.question_input = ""

    question = st.text_area(
        "",
        height=80,
        placeholder="Ask your question...",
        key="question_input",
        width=610
    )

    # Ask button
    ask_button = st.button("🔍 Ask", type="primary")
    
    # Answer section - appears here AFTER Ask button
    if st.session_state.current_answer:
        result = st.session_state.current_answer
        
        st.markdown("### ✨ Answer")

        st.markdown(f'''
        <div class="answer-box">
            <div class="answer-text">{result["answer"]}</div>
        </div>
        ''', unsafe_allow_html=True)

        # Display Sources
        if result.get("sources"):
            st.markdown("### 📚 Source Documents")
            st.caption(f"Retrieved {len(result['sources'])} relevant document(s)")

            for idx, source in enumerate(result["sources"], 1):
                with st.expander(f"📄 Source {idx}", expanded=False):
                    st.markdown(f'<div class="source-box">{source["content"]}</div>',
                              unsafe_allow_html=True)

                    if source.get("metadata"):
                        st.caption("🔎 Metadata:")
                        for key, value in source["metadata"].items():
                            st.text(f"{key}: {value}")

        st.success(f"✅ Answer generated successfully in {result['response_time']:.2f}s!")

# Example Questions - العمود اليمين
with col_right:
   st.markdown("### 📝 Examples")

   examples = [
    ("🏢", "What is Tips Hindawi company?"),
    ("📚", "What do students learn during internship?"),
    ("📅", "How many annual leave days?"),
    ("🏠", "What is the remote work policy?"),
    ("🤒", "When can I take sick leave?"),
   ]

   for idx, (emoji, text) in enumerate(examples):
    st.markdown('<div class="example-btn">', unsafe_allow_html=True)
    st.button(
        f"{emoji} {text}",
        on_click=set_question,
        args=(text,),
        key=f"example_{idx}"
       )
    st.markdown('</div>', unsafe_allow_html=True)

# ASK FUNCTIONALITY
if ask_button and question:
    if not st.session_state.get('api_connected', False):
        st.error("❌ Please connect to the API first! Make sure the Kaggle notebook is running.")
    else:
        progress_text = st.empty()
        progress_bar = st.progress(0)

        try:
            progress_text.text("📝 Preparing request...")
            progress_bar.progress(20)
            time.sleep(0.3)

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "question": question,
                "max_length": max_length
            }

            

            progress_text.text("🦙 Llama 3 is thinking...")
            progress_bar.progress(25)

            start_time = time.time()
            response = requests.post(
                f"{API_URL}/ask",
                headers=headers,
                json=payload,
                timeout=120
            )
            response_time = time.time() - start_time

            progress_bar.progress(50)
            progress_text.empty()
            progress_bar.empty()

            if response.status_code == 200:
                result = response.json()

                st.session_state.total_queries += 1
                st.session_state.total_time += response_time
                st.session_state.history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "question": question,
                    "answer": result["answer"],
                    "response_time": response_time
                })

                st.session_state.current_answer = {
                    "answer": result["answer"],
                    "response_time": response_time,
                
                }
                st.rerun()

            elif response.status_code == 401:
                st.error("🔒 Invalid API key! Please check your credentials.")

            elif response.status_code == 500:
                st.error(f"⚠️ Server error: {response.text}")

            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            progress_text.empty()
            progress_bar.empty()
            st.error("⏱️ Request timeout. The model is taking too long. Try again or reduce max_length.")

        except requests.exceptions.ConnectionError:
            progress_text.empty()
            progress_bar.empty()
            st.error("🔌 Connection error. Make sure:\n- Kaggle notebook is running\n- ngrok URL is correct\n- Internet connection is stable")

        except Exception as e:
            progress_text.empty()
            progress_bar.empty()
            st.error(f"❌ Unexpected error: {str(e)}")

elif ask_button and not question:
    st.warning("⚠️ Please enter a question first")

# HISTORY SECTION
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 📜 Recent Conversation History")

    for idx, item in enumerate(reversed(st.session_state.history[-5:]), 1):
        with st.expander(
            f"🕐 {item['timestamp']} • {item['question'][:60]}{'...' if len(item['question']) > 60 else ''}",
            expanded=(idx == 1)
        ):
            st.markdown(f"**❓ Question:**")
            st.info(item['question'])

            st.markdown(f"**💡 Answer:**")
            st.success(item['answer'])

            st.caption(f"⚡ Response time: {item['response_time']:.2f}s")

# FOOTER
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <div style='font-size: 2rem; margin-bottom: 1rem;'>
        🦙
    </div>
    <p style='font-size: 1.3rem; font-weight: bold; color: #9D4EDD;'>
        Enterprise AI Knowledge Assistant
    </p>
    <p style='color: #666; margin-top: 0.5rem; font-size: 1.1rem;'>
        Powered by <strong>Meta Llama 3 8B Instruct</strong>
    </p>
    <p style='font-size: 0.9rem; color: #888; margin-top: 1rem;'>
        LangChain • FastAPI • FAISS • Sentence Transformers
    </p>
    <p style='font-size: 0.85rem; color: #aaa; margin-top: 1.5rem;'>
        💡 Tip: Keep your Kaggle notebook running for continuous access
    </p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR FOOTER
with st.sidebar:
    st.markdown("---")
    st.caption("🦙 Meta Llama 3 8B Instruct")
    st.caption("Version 2.0.0")
    st.caption("Made with 💜 for Enterprises")
    