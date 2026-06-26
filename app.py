"""Regression Exam Prep"""
import streamlit as st
import json, random
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="רגרסיה 2026", page_icon="📊", layout="wide")
st.markdown("""<style>
/* Mobile responsive */
@media (max-width: 768px) {
    .main .block-container { padding: 1rem 0.5rem; }
    [data-testid="stMetric"] { padding: 0.5rem; }
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.2rem !important; }
}

.main .block-container{direction:rtl;text-align:right}
code,pre{direction:ltr;text-align:left}
[data-testid="stMetric"]{direction:rtl;text-align:right}
[data-testid="stSidebar"] {direction:rtl;text-align:right}
.nav-link{font-size:1.1em;padding:8px 12px;border-radius:8px;margin:4px 0;display:block;text-decoration:none;color:#333}
.nav-link:hover{background:#f0f2f6}
.nav-link.active{background:#ff4b4b;color:white}
</style>""", unsafe_allow_html=True)

@st.cache_data
def ld(): return json.load(open("data/exam_analysis.json","r",encoding="utf-8"))
@st.cache_data
def lc(): return json.load(open("data/classified_questions.json","r",encoding="utf-8"))
@st.cache_data
def lf(): return json.load(open("data/classified_formulas.json","r",encoding="utf-8"))

data=ld(); classified=lc(); formulas_db=lf()
if "progress" not in st.session_state: st.session_state.progress={t["name"]:False for t in data["topics"]}
if "qa" not in st.session_state: st.session_state.qa=0
if "page" not in st.session_state: st.session_state.page="ראשי"

# --- SIDEBAR MENU ---
with st.sidebar:
    st.markdown("## 📊 רגרסיה 2026")
    st.markdown("---")
    
    menu_items = [
        ("🏠", "ראשי"),
        ("🔮", "חיזוי"),
        ("🗂️", "סיווג שאלות"),
        ("📐", "נוסחאות"),
        ("✍️", "תרגול"),
        ("📈", "מעקב"),
    ]
    
    for icon, name in menu_items:
        if st.button(f"{icon} {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
    
    st.markdown("---")
    done = sum(1 for v in st.session_state.progress.values() if v)
    st.caption(f"📊 {done}/{len(st.session_state.progress)} נושאים")
    st.progress(done/max(len(st.session_state.progress),1))

page = st.session_state.page

# ========== HOME ==========
if page=="ראשי":
    st.title("🎓 הכנה למבחן ברגרסיה – ב' 2026")
    st.markdown("---")
    c1,c2,c3=st.columns(3)
    c1.metric("מבחנים שנותחו","15+");c1.caption("מבחני עבר שנותחו לבניית המודל")
    c2.metric("נושאים","12");c2.caption("נושאים שזוהו במבחנים")
    c3.metric("ביטחון בחיזוי","גבוה-בינוני");c3.caption("עקביות הדפוסים שנמצאו")
    st.markdown("---")
    c1,c2,c3=st.columns(3)
    c1.error("🔴 פלט R (100%)");c1.caption("הופיע בכל מבחן")
    c2.error("🔴 מבחן F (95%)");c2.caption("השוואת מודלים מקוננים")
    c3.warning("🟠 רווחי סמך (90%)");c3.caption("CI לפרמטר/חיזוי/תצפית")
    tips=["בדוק df לפני טבלה","OVB=beta2*Cov/Var","Prediction>Confidence","pi=0.5 at x=-b0/b1","F partial: (SSE_R-SSE_F)/dp/MSE_F"]
    st.info(f"💡 {random.choice(tips)}")

# ========== PREDICTION ==========
elif page=="חיזוי":
    st.title("🔮 מודל חיזוי")
    st.caption("מבוסס על 15+ מבחנים")
    topics_df=pd.DataFrame(data["topics"]).sort_values("probability",ascending=True)
    colors=["#d32f2f" if p>=.8 else "#f57c00" if p>=.6 else "#fbc02d" for p in topics_df["probability"]]
    fig=go.Figure(go.Bar(y=topics_df["name"],x=topics_df["probability"]*100,orientation="h",marker_color=colors,text=[f"{p*100:.0f}%" for p in topics_df["probability"]],textposition="outside"))
    fig.update_layout(height=500,xaxis=dict(range=[0,110]))
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("---")
    for p in data["prediction_2026B"]["predicted_structure"]:
        topics_str = ", ".join(p["predicted_topics"])
        st.info(f"**שאלה {p['question']}** ({p['predicted_points']} נק') — {topics_str} [{p['probability']*100:.0f}%]")

# ========== CLASSIFICATION ==========
elif page=="סיווג שאלות":
    st.title("🗂️ סיווג שאלות לפי נושא")
    st.caption("מצא שאלות ממבחני עבר לפי נושא על ותת-נושא")
    st.markdown("---")
    
    qs = classified["exam_questions"]
    
    # Get unique values
    main_topics = sorted(set(q["main_topic"] for q in qs))
    
    # FILTER: Main topic
    sel_main = st.selectbox("🔍 נושא על (ראשי):", ["הכל"] + main_topics)
    
    # Filter by main
    if sel_main != "הכל":
        qs_filtered = [q for q in qs if q["main_topic"] == sel_main]
    else:
        qs_filtered = qs
    
    # FILTER: Specific topic (depends on main selection)
    specific_topics = sorted(set(q["specific_topic"] for q in qs_filtered))
    sel_spec = st.selectbox("🔍 תת-נושא (ספציפי):", ["הכל"] + specific_topics)
    
    if sel_spec != "הכל":
        qs_filtered = [q for q in qs_filtered if q["specific_topic"] == sel_spec]
    
    st.markdown(f"### {len(qs_filtered)} שאלות נמצאו")
    st.markdown("---")
    
    # Display results
    for q in qs_filtered:
        with st.expander(f"{q['exam']} | שאלה {q['question']}{q['sub']} ({q['points']} נק') — {q['specific_topic']}"):
            st.write(f"**תיאור:** {q['description']}")
            st.write(f"**נושא ראשי:** {q['main_topic']}")
            st.write(f"**נושא ספציפי:** {q['specific_topic']}")
            st.write(f"**מבחן:** {q['exam']}")
    
    # Stats
    if qs_filtered:
        st.markdown("---")
        df = pd.DataFrame(qs_filtered)
        tc = df["main_topic"].value_counts()
        fig = go.Figure(go.Pie(labels=tc.index.tolist(), values=tc.values.tolist()))
        fig.update_layout(height=300, title="התפלגות נושאים ראשיים")
        st.plotly_chart(fig, use_container_width=True)

# ========== FORMULAS ==========
elif page=="נוסחאות":
    st.title("📐 נוסחאות מסווגות")
    st.caption("כל נוסחה מסווגת לנושא ראשי ותת-נושא")
    st.markdown("---")
    
    main_topics = sorted(set(f["main_topic"] for f in formulas_db))
    sel = st.selectbox("🔍 סנן לפי נושא ראשי:", ["הכל"] + main_topics)
    filtered = formulas_db if sel=="הכל" else [f for f in formulas_db if f["main_topic"]==sel]
    
    # Sub-filter
    specs = sorted(set(f["specific_topic"] for f in filtered))
    sel2 = st.selectbox("🔍 סנן לפי תת-נושא:", ["הכל"] + specs)
    if sel2 != "הכל":
        filtered = [f for f in filtered if f["specific_topic"]==sel2]
    
    st.markdown(f"**{len(filtered)} נוסחאות**")
    st.markdown("---")
    for f in filtered:
        st.code(f["formula"], language=None)
        st.caption(f"📌 **{f['main_topic']}** → {f['specific_topic']}")
        if 'usage' in f:
            st.markdown(f"💬 _{f['usage']}_")

# ========== PRACTICE ==========
elif page=="תרגול":
    st.title("✍️ תרגול")
    st.caption("שאלות בסגנון המבחן")
    st.markdown("---")
    QS=[{"t":"F","q":"n=80,k=3,RSE=5.2,R2=0.82,F=115.3\nA.significant 5%?\nB.R2adj?\nC.SSE,SST?","a":"A.Yes(115>2.7)\nB.0.813\nC.2055,11417"},{"t":"CI","q":"n=25,b1=3.5,SE=1.2\nA.CI95%\nB.significant?","a":"A.[1.02,5.98]\nB.Yes(t=2.92)"},{"t":"OVB","q":"b2=3,Cov=4,Var=8\nA.Unbiased?\nB.Bias?","a":"A.No\nB.1.5"},{"t":"Logistic","q":"b0=-2,b1=0.5\nA.pi(x)?\nB.OR?\nC.x(pi=0.5)?","a":"A.1/(1+e^{2-0.5x})\nB.1.65\nC.4"}]
    for i,q in enumerate(QS):
        with st.expander(f"שאלה {i+1}: {q['t']}"):
            st.text(q["q"])
            if st.button("📖 פתרון",key=f"s{i}"): st.success(q["a"]); st.session_state.qa+=1

# ========== TRACKING ==========
elif page=="מעקב":
    st.title("📈 מעקב התקדמות")
    st.caption("סמן נושאים שלמדת")
    st.markdown("---")
    for topic,v in st.session_state.progress.items():
        c1,c2=st.columns([5,1])
        icon = chr(9989) if v else chr(11036)
        c1.write(f"{icon} {topic}")
        if not v and c2.button(chr(10003),key=f"m_{topic}"):
            st.session_state.progress[topic]=True; st.rerun()
    st.markdown("---")
    done=sum(1 for v in st.session_state.progress.values() if v)
    st.write(f"**{done}/{len(st.session_state.progress)}** נושאים | **{st.session_state.qa}** שאלות")
    if st.button("🔄 אפס"):
        st.session_state.progress={t["name"]:False for t in data["topics"]}; st.session_state.qa=0; st.rerun()
