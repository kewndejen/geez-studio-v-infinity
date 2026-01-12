import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import time
import datetime
import random

# ---------------------------------------------------------
# 1. IMPERIAL PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="GE'EZ STUDIO | v-Infinity Sovereign",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# World-Class Sovereign UI (Emerald & Gold Perfection)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Montserrat:wght@400;700&family=Abyssinica+SIL&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #003311 0%, #001a0d 100%); 
        color: #ffffff; 
        font-family: 'Montserrat', sans-serif; 
    }
    
    h1, h2, h3 { 
        font-family: 'Cinzel Decorative', serif; 
        color: #FFD700 !important; 
        text-align: center;
        text-shadow: 0px 0px 20px rgba(255, 215, 0, 0.5);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001a0d 0%, #000000 100%) !important;
        border-right: 4px solid #FFD700;
    }
    
    .sovereign-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-left: 10px solid #FFD700;
        margin-bottom: 25px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.6);
    }

    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important; font-weight: 900 !important;
        border-radius: 12px !important; border: 2px solid #FFFFFF !important;
        height: 3.8em; width: 100%; transition: 0.5s ease;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 35px #FFD700; color: #fff !important; }

    [data-testid="stChatInput"] { 
        border: 3px solid #FFD700 !important; 
        background-color: #ffffff !important; 
        border-radius: 20px !important; 
        padding: 10px !important;
    }
    [data-testid="stChatInput"] textarea { color: #000000 !important; font-weight: bold; font-size: 1.1rem; }
    
    .citation { font-size: 0.85rem; color: #FFD700; border-top: 1px solid #ffffff33; margin-top: 25px; padding-top: 15px; font-family: monospace; }
    .wait-msg { color: #FFD700; font-style: italic; font-size: 1rem; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DOCUMENT & FILE HELPERS
# ---------------------------------------------------------
def extract_text(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    text = ""
    try:
        if ext == 'pdf':
            reader = PdfReader(uploaded_file)
            for page in reader.pages: text += page.extract_text()
        elif ext in ['docx', 'doc']:
            doc = Document(uploaded_file)
            for p in doc.paragraphs: text += p.text + "\n"
        return text
    except: return ""

# ---------------------------------------------------------
# 3. INDESTRUCTIBLE ENGINE (Discovery & Failover)
# ---------------------------------------------------------
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ API Key አልተገኘም! እባክዎ በ Streamlit Secrets ውስጥ ያስገቡ።")
    st.stop()

@st.cache_resource
def get_best_engine():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        priority = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        for target in priority:
            for m in available:
                if target in m: return m
        return available[0]
    except: return "models/gemini-1.5-flash"

SELECTED_ENGINE = get_best_engine()

def ask_sovereign_ai(prompt, product_context, doc_memory="", image=None):
    product_instructions = {
        "Product 1: Sovereign AI Translator": "You are a world-class Ge'ez Translator. Focus on Sem-na-Worq and scholarly context.",
        "Product 2: Neural Transcriber": "You are an expert Paleographer. Transcribe handwritten Ethiopic manuscripts from images.",
        "Product 3: History AI": "You are a Chronicler of Ethiopian History. Provide deep analysis of 3,000 years of heritage.",
        "Product 4: Ge'ez Learning Hub": "You are a Master Teacher. Explain Ge'ez grammar and syntax clearly for students.",
        "Product 5: Qene Analyzer": "You are a Qene Master. Break down poetic meanings into Wax and Gold."
    }
    
    role = product_instructions.get(product_context, "You are a scholarly Ge'ez AI.")
    sys_instr = f"{role} Grand Architect: Deacon Kewn Dejen. Knowledge Base: {doc_memory[:20000]}"
    
    status_placeholder = st.empty()
    try:
        model = genai.GenerativeModel(model_name=SELECTED_ENGINE, system_instruction=sys_instr)
        content = [prompt, image] if image else prompt
        
        for attempt in range(1, 4):
            try:
                response = model.generate_content(content)
                return response.text, SELECTED_ENGINE
            except Exception as e:
                if "429" in str(e):
                    wait = attempt * 7
                    status_placeholder.markdown(f"<div class='wait-msg'>⏳ ሊቁ በጥልቅ ምርምር ላይ ናቸው... ({attempt}/3)</div>", unsafe_allow_html=True)
                    time.sleep(wait)
                    continue
                raise e
    except Exception as e: return f"❌ Error: {str(e)}", "None"

# ---------------------------------------------------------
# 4. SIDEBAR: THE SOVEREIGN CONTROL CENTER
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h1>🔱 GE'EZ STUDIO</h1>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='background:linear-gradient(45deg, #FFD700, #B8860B); padding:15px; border-radius:12px; text-align:center; color:#000; font-weight:900; border: 2px solid #fff;'>
            GRAND ARCHITECT:<br>DEACON KEWN DEJEN
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    product = st.selectbox("የጥበብ ምርቶች (Select Product)", [
        "Product 1: Sovereign AI Translator", "Product 2: Neural Transcriber",
        "Product 3: History AI", "Product 4: Ge'ez Learning Hub", "Product 5: Qene Analyzer"
    ])

    st.markdown("---")
    doc_memory = ""
    uploaded_img = None
    
    if product == "Product 2: Neural Transcriber":
        uploaded_img = st.file_uploader("📸 የብራና ምስል ይጫኑ", type=['jpg', 'png', 'jpeg'])
    else:
        uploaded_files = st.file_uploader("📂 ሰነድ ይጫኑ (PDF/Word)", type=['pdf', 'docx'], accept_multiple_files=True)
        if uploaded_files:
            for f in uploaded_files: doc_memory += f"\n[FILE: {f.name}]\n" + extract_text(f)
            st.success(f"✅ {len(uploaded_files)} ሰነዶች ተነበዋል!")

    if st.button("🔄 REBOOT v-INFINITY"):
        st.cache_resource.clear()
        st.rerun()

# ---------------------------------------------------------
# 5. MAIN WORKSPACE
# ---------------------------------------------------------
st.markdown(f"<h1>{product}</h1>", unsafe_allow_html=True)

if product == "Product 2: Neural Transcriber" and uploaded_img:
    img = Image.open(uploaded_img)
    col1, col2 = st.columns(2)
    with col1: st.image(img, caption="Artifact", use_column_width=True)
    with col2:
        if st.button("🔱 INITIATE NEURAL SCAN"):
            with st.spinner("Decoding..."):
                res, eng = ask_sovereign_ai("Transcribe and analyze this Ethiopic script.", product, image=img)
                st.markdown(f"<div class='sovereign-card'>{res}</div>", unsafe_allow_html=True)

if product != "Product 2: Neural Transcriber":
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Consult the expert..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(f"<b>{prompt}</b>", unsafe_allow_html=True)
        with st.chat_message("assistant"):
            with st.spinner("ሊቁ መዛግብቱን እያመሳከረ ነው..."):
                answer, engine = ask_sovereign_ai(prompt, product, doc_memory)
                full_res = f"<div>{answer}</div><div class='citation'>Source: {engine} | v-Infinity Sovereign</div>"
                st.markdown(full_res, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": full_res})

st.markdown("<br><hr><p style='text-align:center; color:#FFD700;'><b>GE'EZ SCHOLAR AI STUDIO | Grand Architect Deacon Kewn Dejen</b></p>", unsafe_allow_html=True)
