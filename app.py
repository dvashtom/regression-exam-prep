"""Regression Exam Prep - Dark Mode RTL Edition - Main Router"""
import streamlit as st
import json

st.set_page_config(page_title="רגרסיה 2026", page_icon="📊", layout="wide")

# ========== STYLES ==========
st.markdown("""<style>
:root{--bg-primary:#0d1117;--bg-secondary:#161b22;--bg-tertiary:#21262d;--text-primary:#e6edf3;--text-secondary:#8b949e;--accent:#58a6ff;--accent-green:#3fb950;--accent-orange:#d29922;--accent-red:#f85149;--accent-purple:#bc8cff;--border:#30363d}
.stApp,[data-testid="stAppViewContainer"],.main{background-color:var(--bg-primary)!important;color:var(--text-primary)!important}
[data-testid="stSidebar"]{background-color:var(--bg-secondary)!important;border-left:1px solid var(--border)!important;direction:rtl;text-align:right}
[data-testid="stSidebar"] *{color:var(--text-primary)!important}
.main .block-container{direction:rtl;text-align:right;max-width:1200px}
code,pre{direction:ltr;text-align:left;color:#1a1a1a!important;background-color:#f0f0f0!important}
h1,h2,h3,h4,h5,h6{color:var(--text-primary)!important}
[data-testid="stMetric"]{background:var(--bg-secondary)!important;border:1px solid var(--border)!important;border-radius:12px!important;padding:1rem!important;direction:rtl;text-align:right}
[data-testid="stMetric"] label{color:var(--text-secondary)!important}
[data-testid="stMetric"] [data-testid="stMetricValue"]{color:var(--accent)!important}
[data-testid="stExpander"]{background:var(--bg-secondary)!important;border:1px solid var(--border)!important;border-radius:8px!important;margin-bottom:8px!important}
[data-testid="stSelectbox"]>div>div{background-color:var(--bg-tertiary)!important;color:var(--text-primary)!important;border-color:var(--border)!important}
.stButton>button{background:linear-gradient(135deg,var(--accent),var(--accent-purple))!important;color:white!important;border:none!important;border-radius:8px!important;font-weight:600!important;transition:all .3s ease!important}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 4px 12px rgba(88,166,255,.4)!important}
[data-testid="stAlert"]{background:var(--bg-tertiary)!important;border-radius:8px!important}
.stProgress>div>div{background:linear-gradient(90deg,var(--accent),var(--accent-purple))!important}
[data-testid="stSidebar"] .stButton>button{background:var(--bg-tertiary)!important;border:1px solid var(--border)!important;color:var(--text-primary)!important;text-align:right!important;justify-content:flex-end!important;transform:none!important}
[data-testid="stSidebar"] .stButton>button:hover{background:var(--accent)!important;color:white!important}
div,span,label,p,li,td,th,summary,.stMarkdown,.stMarkdown p,.stCaption,strong,b,[data-testid="stText"],.element-container,[data-baseweb],[data-testid="stWidgetLabel"] p,[data-testid="stExpanderDetails"] *,[data-testid="stExpander"] summary span,[data-testid="stExpander"] summary p,[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p{color:var(--text-primary)!important}
*{direction:rtl}
.stApp *{text-align:right}
[data-testid="stExpander"] details,[data-testid="stExpanderDetails"],[data-baseweb="select"]>div,[data-testid="stAlert"] div,[data-testid="stMetric"] *,.stSelectbox label,.stMultiSelect label{direction:rtl;text-align:right}
code,pre,[data-testid="stCode"]{direction:ltr!important;text-align:left!important}
[data-testid="stCode"] code,[data-testid="stCode"] pre,[data-testid="stCode"] pre code,[data-testid="stCode"],.stCode,.stCode span,.stCode code,.stCode pre,pre code span{color:#1a1a1a!important;background-color:#f6f8fa!important}
[data-testid="stChatInput"]{direction:rtl!important}
[data-testid="stChatInput"] input{direction:rtl!important;text-align:right!important}
[data-testid="stChatMessage"]{direction:rtl!important;text-align:right!important;background:var(--bg-secondary)!important;border:1px solid var(--border)!important;border-radius:12px!important;margin-bottom:8px!important}
[data-testid="stChatMessage"] p,.stChatMessage{direction:rtl!important;text-align:right!important}
@media(max-width:768px){.main .block-container{padding:1rem .5rem}h1{font-size:1.5rem!important}}
</style>""", unsafe_allow_html=True)

# ========== DATA ==========
@st.cache_data
def ld(): return json.load(open("data/exam_analysis.json","r",encoding="utf-8"))
@st.cache_data
def lc(): return json.load(open("data/classified_questions.json","r",encoding="utf-8"))
@st.cache_data
def lf(): return json.load(open("data/classified_formulas.json","r",encoding="utf-8"))
@st.cache_data
def ls(): return json.load(open("data/topic_summaries.json","r",encoding="utf-8"))

data=ld(); classified=lc(); formulas_db=lf(); summaries=ls()

if "progress" not in st.session_state:
    st.session_state.progress = {t["name"]: False for t in data["topics"]}
if "qa" not in st.session_state:
    st.session_state.qa = 0
if "page" not in st.session_state:
    st.session_state.page = "ראשי"
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("## 📊 רגרסיה 2026")
    st.markdown("---")
    nav = [("🏠","ראשי"),("🔮","חיזוי"),("🗂️","סיווג שאלות"),("📐","נוסחאות"),("📖","סיכום נושאים"),("📈","מעקב"),("🤖","Ask AI")]
    for icon, name in nav:
        if st.button(f"{icon} {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
    st.markdown("---")
    done = sum(1 for v in st.session_state.progress.values() if v)
    st.caption(f"📊 {done}/{len(st.session_state.progress)} נושאים")
    st.progress(done / max(len(st.session_state.progress), 1))

# ========== PAGE ROUTER ==========
from pages_content import (
    render_home, render_prediction, render_classification,
    render_formulas, render_summaries, render_tracking, render_chat
)

page = st.session_state.page

if page == "ראשי":
    render_home(data)
elif page == "חיזוי":
    render_prediction(data)
elif page == "סיווג שאלות":
    render_classification(classified)
elif page == "נוסחאות":
    render_formulas(formulas_db)
elif page == "סיכום נושאים":
    render_summaries(summaries, classified)
elif page == "מעקב":
    render_tracking(data)
elif page == "Ask AI":
    render_chat()