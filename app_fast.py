import asyncio
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import streamlit as st
import random
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Career Readiness Navigator", page_icon="🚀", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {background: radial-gradient(circle at top left,#21124d 0%,#090b18 45%,#05060c 100%); color:#fff;}
.block-container {padding-top:1.5rem; max-width:1200px;}
.hero {padding:28px;border-radius:24px;background:linear-gradient(135deg,rgba(113,62,255,.35),rgba(0,220,255,.12));border:1px solid rgba(255,255,255,.12);box-shadow:0 0 40px rgba(113,62,255,.12);}
.card {padding:20px;border-radius:20px;background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.09);margin:8px 0;}
.big {font-size:42px;font-weight:800;}
.pill {display:inline-block;padding:6px 12px;border-radius:999px;background:rgba(0,220,255,.12);margin:4px;}
div.stButton > button {border-radius:14px;font-weight:700;}
</style>
""", unsafe_allow_html=True)

CAREERS = {
    "AI / ML Engineer":["Python","Machine Learning","Statistics","SQL","Problem Solving"],
    "Data Scientist":["Python","SQL","Statistics","Machine Learning","Communication"],
    "Software Developer":["Python","DSA","Git/GitHub","Problem Solving","Communication"],
    "Data Analyst":["Python","SQL","Statistics","Power BI","Communication"],
    "Cybersecurity Analyst":["Python","Linux","Networking","Problem Solving","Security"],
    "Cloud / DevOps Engineer":["Linux","Git/GitHub","Cloud","Python","Problem Solving"],
}
RESOURCES = {
    "Python":"Build 3 small automation/data projects.",
    "Machine Learning":"Learn regression, classification and model evaluation.",
    "Statistics":"Practice probability, distributions and hypothesis testing.",
    "SQL":"Practice SELECT, JOIN, GROUP BY and subqueries.",
    "DSA":"Solve easy arrays, strings, hash-map and linked-list problems.",
    "Git/GitHub":"Create repositories and make meaningful commits.",
    "Communication":"Practice 2-minute technical explanations daily.",
    "Power BI":"Build one interactive dashboard from a public dataset.",
    "Linux":"Learn files, processes, permissions and shell commands.",
    "Networking":"Learn TCP/IP, DNS, HTTP and basic troubleshooting.",
    "Security":"Learn authentication, common vulnerabilities and safe labs.",
    "Cloud":"Learn compute, storage, networking and deployment basics.",
    "Problem Solving":"Solve one small coding problem every day."
}

if "xp" not in st.session_state: st.session_state.xp = 0
if "completed" not in st.session_state: st.session_state.completed = set()
if "messages" not in st.session_state: st.session_state.messages = []

st.markdown('<div class="hero"><div class="big">🚀 Career Readiness Navigator</div><p style="font-size:19px">Turn your current skills into a career-ready roadmap.</p><span class="pill">🤖 AI Agents</span><span class="pill">⚡ XP</span><span class="pill">🏆 Badges</span><span class="pill">🎯 Personalized</span></div>', unsafe_allow_html=True)

# ---------- PROFILE ----------
st.subheader("👤 1. Build Your Student Profile")
c1,c2,c3 = st.columns(3)
with c1: name = st.text_input("Your name", placeholder="Enter your name")
with c2: age = st.number_input("Age", min_value=13, max_value=60, value=19)
with c3: career = st.selectbox("Target career", list(CAREERS))

if age <= 17:
    persona = "🌱 Young Explorer"
elif age <= 20:
    persona = "🔥 Campus Builder"
elif age <= 23:
    persona = "🚀 Career Launcher"
else:
    persona = "💼 Career Accelerator"

st.info(f"{persona} mode activated for age {age}. Your challenges and encouragement are personalized.")

# ---------- SKILLS ----------
st.subheader("🧠 2. Skill Assessment")
skills = {}
cols = st.columns(2)
for i, skill in enumerate(CAREERS[career]):
    with cols[i % 2]:
        skills[skill] = st.slider(skill, 0, 10, 5, key=f"skill_{skill}")

if st.button("⚡ Analyze My Career Readiness", type="primary", use_container_width=True):
    st.session_state.xp += 25
    st.session_state.analysis_done = True
    st.balloons()

if st.session_state.get("analysis_done"):
    required = CAREERS[career]
    readiness = int(sum(skills.values()) / (len(required)*10) * 100)
    gaps = sorted([(s,10-skills[s]) for s in required], key=lambda x:x[1], reverse=True)

    st.subheader("📊 Your Readiness")
    a,b,c = st.columns(3)
    with a:
        st.metric("Career Readiness", f"{readiness}%")
    with b:
        st.metric("XP", st.session_state.xp)
    with c:
        level = st.session_state.xp//100 + 1
        st.metric("Level", level)

    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=readiness,
        title={"text":"Readiness Score"},
        gauge={"axis":{"range":[0,100]}}
    ))
    fig.update_layout(height=280, margin=dict(l=20,r=20,t=60,b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🎯 Skill Gaps")
    for skill,gap in gaps:
        if gap:
            st.markdown(f'<div class="card"><b>{skill}</b> — {skills[skill]}/10<br><small>Next quest: {RESOURCES.get(skill,"Practice this skill with a small project.")}</small></div>', unsafe_allow_html=True)
        else:
            st.success(f"🔥 {skill}: MAXED OUT!")

    # ---------- QUESTS ----------
    st.subheader("🎮 3. Daily Career Quests")
    for skill,gap in gaps[:3]:
        if gap == 0: continue
        key = f"{career}:{skill}"
        if st.button(f"✅ Complete quest: {skill}", key=f"quest_{skill}"):
            if key not in st.session_state.completed:
                st.session_state.completed.add(key)
                st.session_state.xp += 20
                st.success("🎉 Quest complete! +20 XP")
                st.balloons()
                time.sleep(.2)
                st.rerun()

    # ---------- BADGES ----------
    st.subheader("🏆 Your Progress")
    xp = st.session_state.xp
    badges = []
    if xp >= 25: badges.append("⚡ First Analysis")
    if xp >= 50: badges.append("🔥 Momentum Builder")
    if xp >= 100: badges.append("🚀 Career Climber")
    if readiness >= 70: badges.append("🎯 Career Ready")
    if not badges: badges = ["🔒 Complete your first quest"]
    st.markdown(" ".join(f'<span class="pill">{b}</span>' for b in badges), unsafe_allow_html=True)

# ---------- AGENTS ----------
st.subheader("🤖 4. AI Career Agents")
agent = st.selectbox("Choose your agent", ["🎯 Career Coach","🧑‍💼 Interview Coach","📚 Study Planner","📄 Resume Coach"])

def agent_reply(q):
    q=q.lower()
    if "interview" in agent.lower():
        return "🎤 Interview Agent: Start with your target role, prepare 10 core questions, then practice explaining one project using Problem → Solution → Tech → Result."
    if "study" in agent.lower():
        return "📚 Study Agent: Use a 45-minute cycle: 25 min concept → 15 min coding/practice → 5 min recall. Prioritize your biggest skill gap first."
    if "resume" in agent.lower():
        return "📄 Resume Agent: Convert work into evidence: Action + Technology + Result. Example: “Built a Streamlit career-readiness dashboard using Python and Plotly.”"
    return f"🎯 Career Coach: For {career}, focus first on {', '.join(CAREERS[career][:3])}. Your next move should be one small project that proves those skills."

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

prompt = st.chat_input("Ask your selected agent anything...")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    answer = agent_reply(prompt)
    st.session_state.messages.append({"role":"assistant","content":answer})
    st.rerun()

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🏆 Hackathon Demo • Personalized career readiness • Gamification • Agent-style coaching")
cd