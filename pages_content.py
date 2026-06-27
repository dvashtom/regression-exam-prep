"""Page content renderers for the Regression Exam Prep app."""
import streamlit as st
import json, random, re
import plotly.graph_objects as go
import pandas as pd


def extract_year(exam_name):
    m = re.search(r'(20\d{2})', exam_name)
    return m.group(1) if m else "לא ידוע"


def render_home(data):
    """Render the home page."""
    st.markdown('<h1 style="color:#58a6ff;text-align:center;font-size:3em;margin-bottom:0;text-shadow:0 0 30px rgba(88,166,255,0.4);">Regression</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8b949e;text-align:center;font-size:1.2em;margin-top:0;">הכנה למבחן ברגרסיה - ב׳ 2026</p>', unsafe_allow_html=True)
    
    canvas_html = '<div style="position:relative;overflow:hidden;width:100%;height:500px;border-radius:16px;"><canvas id="mc" style="width:100%;height:100%;display:block;position:absolute;top:0;left:0;"></canvas><div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;z-index:10;pointer-events:none"><h2 style="color:#58a6ff;font-size:2.5em;margin:0;text-shadow:0 0 30px rgba(88,166,255,.6);font-family:sans-serif">Regression</h2><p style="color:#e6edf3;margin-top:12px;font-family:sans-serif;font-size:1.1em;">מטריצת נושאים דינמית</p></div></div>'
    canvas_js = '<script>!function(){const c=document.getElementById("mc");if(!c)return;const x=c.getContext("2d");function resize(){c.width=c.parentElement.offsetWidth||900;c.height=500}resize();window.addEventListener("resize",resize);const t=["F-test","OLS","CI","R2","WLS","Logistic","OVB","Residuals","Dummy","VIF","SSE","MSE","t-test","BLUE","B-hat","s2","Sxy","Hat Matrix"],p=[];for(let i=0;i<80;i++)p.push({x:Math.random()*c.width,y:Math.random()*c.height,vx:(Math.random()-.5)*.5,vy:(Math.random()-.5)*.5,s:Math.random()*3+1.5,a:Math.random()*.5+.2,t:t[Math.floor(Math.random()*t.length)],st:Math.random()>.4});function draw(){x.fillStyle="rgba(13,17,23,.12)";x.fillRect(0,0,c.width,c.height);p.forEach((a,i)=>{a.x+=a.vx;a.y+=a.vy;if(a.x<0||a.x>c.width)a.vx*=-1;if(a.y<0||a.y>c.height)a.vy*=-1;p.forEach((b,j)=>{if(i===j)return;const d=Math.sqrt((a.x-b.x)**2+(a.y-b.y)**2);if(d<130){x.strokeStyle="rgba(88,166,255,"+(0.15*(1-d/130))+")";x.lineWidth=.6;x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke()}});x.beginPath();x.arc(a.x,a.y,a.s,0,Math.PI*2);x.fillStyle="rgba(88,166,255,"+a.a+")";x.fill();if(a.st){x.font="10px monospace";x.fillStyle="rgba(188,140,255,"+(a.a*.8)+")";x.fillText(a.t,a.x+6,a.y-6)}});requestAnimationFrame(draw)}draw()}()</script>'
    st.components.v1.html(canvas_html + canvas_js, height=510)
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("מבחנים שנותחו", "15+")
    c2.metric("נושאים", "12")
    c3.metric("ביטחון", "גבוה-בינוני")
    st.markdown("---")
    st.subheader("🎯 נושאים בעדיפות גבוהה")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div style="background:linear-gradient(135deg,#f85149,#da3633);padding:1rem;border-radius:12px;text-align:center"><h3 style="color:white;margin:0">פלט R</h3><p style="color:rgba(255,255,255,.8);margin:4px 0 0">100%</p></div>', unsafe_allow_html=True)
    c2.markdown('<div style="background:linear-gradient(135deg,#f85149,#da3633);padding:1rem;border-radius:12px;text-align:center"><h3 style="color:white;margin:0">מבחן F</h3><p style="color:rgba(255,255,255,.8);margin:4px 0 0">95%</p></div>', unsafe_allow_html=True)
    c3.markdown('<div style="background:linear-gradient(135deg,#d29922,#bb8009);padding:1rem;border-radius:12px;text-align:center"><h3 style="color:white;margin:0">רווחי סמך</h3><p style="color:rgba(255,255,255,.8);margin:4px 0 0">90%</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    tips = ["בדוק df לפני טבלה", "OVB=beta2*Cov/Var", "Prediction>Confidence", "pi=0.5 at x=-b0/b1", "F partial: (SSE_R-SSE_F)/dp/MSE_F"]
    st.info(f"💡 {random.choice(tips)}")


def render_prediction(data):
    """Render the prediction page."""
    st.title("🔮 מודל חיזוי")
    st.caption("מבוסס על 15+ מבחנים")
    topics_df = pd.DataFrame(data["topics"]).sort_values("probability", ascending=True)
    colors = ["#f85149" if p >= .8 else "#d29922" if p >= .6 else "#3fb950" for p in topics_df["probability"]]
    fig = go.Figure(go.Bar(y=topics_df["name"], x=topics_df["probability"]*100, orientation="h", marker_color=colors, text=[f"{p*100:.0f}%" for p in topics_df["probability"]], textposition="outside"))
    fig.update_layout(height=500, xaxis=dict(range=[0, 110]), paper_bgcolor="#161b22", plot_bgcolor="#161b22", font=dict(color="#e6edf3"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    for p in data["prediction_2026B"]["predicted_structure"]:
        st.info(f"**שאלה {p['question']}** ({p['predicted_points']} נק') — {', '.join(p['predicted_topics'])} [{p['probability']*100:.0f}%]")


def render_classification(classified):
    """Render the classification page."""
    st.title("🗂️ סיווג שאלות לפי נושא")
    st.caption("מצא שאלות ממבחני עבר לפי נושא, תת-נושא ושנה")
    st.markdown("---")
    qs = classified["exam_questions"]
    
    all_years = sorted(set(extract_year(q["exam"]) for q in qs), reverse=True)
    
    fc1, fc2 = st.columns(2)
    with fc1:
        sel_main = st.selectbox("🔍 נושא ראשי:", ["הכל"] + sorted(set(q["main_topic"] for q in qs)))
    with fc2:
        sel_year = st.selectbox("📅 סנן לפי שנה:", ["הכל"] + all_years)
    
    if sel_year != "הכל":
        qs_filtered = [q for q in qs if extract_year(q["exam"]) == sel_year]
    else:
        qs_filtered = qs
    
    if sel_main != "הכל":
        qs_filtered = [q for q in qs_filtered if q["main_topic"] == sel_main]
    
    specific_topics = sorted(set(q["specific_topic"] for q in qs_filtered))
    sel_spec = st.selectbox("🔍 תת-נושא:", ["הכל"] + specific_topics)
    if sel_spec != "הכל":
        qs_filtered = [q for q in qs_filtered if q["specific_topic"] == sel_spec]
    
    sel_diff = st.selectbox("🔍 רמת קושי:", ["הכל", "קל", "בינוני", "קשה"])
    if sel_diff != "הכל":
        qs_filtered = [q for q in qs_filtered if q.get("difficulty") == sel_diff]
    
    if qs_filtered:
        df = pd.DataFrame(qs_filtered)
        tc = df["main_topic"].value_counts()
        fig = go.Figure(go.Pie(labels=tc.index.tolist(), values=tc.values.tolist(), hole=0.4))
        fig.update_layout(height=280, title="התפלגות נושאים ראשיים", paper_bgcolor="#161b22", plot_bgcolor="#161b22", font=dict(color="#e6edf3"))
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"### 📋 {len(qs_filtered)} שאלות נמצאו")
    st.markdown("---")
    
    for q in qs_filtered:
        with st.expander(f"{q['exam']} | ש{q['question']}{q['sub']} ({q['points']}נק') — {q['specific_topic']} [{q.get('difficulty','?')}]"):
            st.write(f"**{q['description']}**")
            st.write(f"נושא: {q['main_topic']} -> {q['specific_topic']} | קושי: {q.get('difficulty','?')}")
            if q.get('solution'):
                st.success(f"💡 {q['solution']}")


def render_formulas(formulas_db):
    """Render the formulas page."""
    st.title("📐 נוסחאות מסווגות")
    st.caption("כל נוסחה מסווגת לנושא ראשי ותת-נושא")
    st.markdown("---")
    main_topics = sorted(set(f["main_topic"] for f in formulas_db))
    sel = st.selectbox("🔍 סנן לפי נושא ראשי:", ["הכל"] + main_topics)
    filtered = formulas_db if sel == "הכל" else [f for f in formulas_db if f["main_topic"] == sel]
    specs = sorted(set(f["specific_topic"] for f in filtered))
    sel2 = st.selectbox("🔍 סנן לפי תת-נושא:", ["הכל"] + specs)
    if sel2 != "הכל":
        filtered = [f for f in filtered if f["specific_topic"] == sel2]
    st.markdown(f"**{len(filtered)} נוסחאות**")
    st.markdown("---")
    for f in filtered:
        st.code(f["formula"], language=None)
        st.caption(f"📌 **{f['main_topic']}** -> {f['specific_topic']}")
        if 'usage' in f:
            st.markdown(f"💬 _{f['usage']}_")


def render_summaries(summaries, classified):
    """Render the topic summaries page."""
    st.title("📖 סיכום לפי נושא")
    st.caption("לכל נושא: נוסחאות, טיפים, ומלכודות נפוצות")
    st.markdown("---")
    sel_topic = st.selectbox("בחר נושא:", list(summaries.keys()))
    s = summaries[sel_topic]
    st.subheader(f"📐 נוסחאות - {sel_topic}")
    for f in s["formulas"]:
        st.code(f, language=None)
    st.subheader("💡 טיפים")
    for t in s["tips"]:
        st.success(t)
    st.subheader("⚠️ מלכודות נפוצות")
    for t in s["traps"]:
        st.error(t)
    st.markdown("---")
    st.subheader("📝 שאלות לדוגמה מהמבחנים")
    related = [q for q in classified["exam_questions"] if q["main_topic"] == sel_topic][:5]
    for q in related:
        st.write(f"• **{q['exam']}** ש{q['question']}{q['sub']}: {q['description']}")
        if q.get("solution"):
            st.caption(f"   💡 {q['solution']}")


def render_tracking(data):
    """Render the progress tracking page."""
    st.title("📈 מעקב התקדמות")
    st.caption("סמן נושאים שלמדת")
    st.markdown("---")
    for topic, v in st.session_state.progress.items():
        c1, c2 = st.columns([5, 1])
        icon = chr(9989) if v else chr(11036)
        c1.write(f"{icon} {topic}")
        if not v and c2.button(chr(10003), key=f"m_{topic}"):
            st.session_state.progress[topic] = True
            st.rerun()
    st.markdown("---")
    done = sum(1 for v in st.session_state.progress.values() if v)
    st.write(f"**{done}/{len(st.session_state.progress)}** נושאים | **{st.session_state.qa}** שאלות")
    if st.button("🔄 אפס"):
        st.session_state.progress = {t["name"]: False for t in data["topics"]}
        st.session_state.qa = 0
        st.rerun()


def render_chat():
    """Render the AI Chat page."""
    st.title("🤖 Ask AI - עוזר לרגרסיה")
    st.caption("שאל שאלות בנושאי הקורס וקבל תשובות מבוססות על חומרי הלימוד")
    st.markdown("---")
    
    # Check if AI service is available
    try:
        from ai_assistant import get_assistant
        assistant = get_assistant()
        
        if not assistant.is_vector_store_ready():
            st.warning("⚠️ בסיס הנתונים הווקטורי לא נבנה עדיין. הרץ את הפקודה הבאה:")
            st.code("cd data && python build_vector_store.py", language="bash")
            st.info("לאחר הרצת הפקודה, רענן את הדף.")
            return
    except ImportError as e:
        st.error(f"❌ חסרות ספריות נדרשות. הרץ: pip install -r requirements.txt")
        st.code(f"Error: {e}", language=None)
        return
    
    # Display chat history
    for msg in st.session_state.chat_messages:
        role = msg["role"]
        avatar = "🧑‍🎓" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("שאל שאלה בנושא רגרסיה לינארית..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("חושב..."):
                response = assistant.chat(
                    user_message=prompt,
                    chat_history=st.session_state.chat_messages[:-1]
                )
                st.markdown(response)
        
        # Add assistant message
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.session_state.qa += 1
    
    # Clear chat button
    if st.session_state.chat_messages:
        st.markdown("---")
        if st.button("🗑️ נקה שיחה"):
            st.session_state.chat_messages = []
            st.rerun()
