import streamlit as st

st.title("🚀 Career Readiness Navigator")
st.write("Find your skill gaps and build your career roadmap.")

st.header("Let's get started!")

name = st.text_input("Enter your name")

career = st.selectbox(
    "Choose your target career",
    [
        "Data Scientist",
        "Software Developer",
        "Data Analyst",
        "Machine Learning Engineer",
        "Cybersecurity Analyst"
    ]
)

if st.button("Start Assessment"):
    st.session_state.assessment_started = True

if st.session_state.get("assessment_started", False):

    st.subheader(f"🎯 {career} Skill Assessment")

    st.write("Rate your current skill level from 1 to 5.")

    python = st.slider("Python", 1, 5, 1)
    sql = st.slider("SQL", 1, 5, 1)
    statistics = st.slider("Statistics", 1, 5, 1)
    machine_learning = st.slider("Machine Learning", 1, 5, 1)
    communication = st.slider("Communication", 1, 5, 1)

    if st.button("Calculate My Skill Gaps"):

        required = {
            "Python": 5,
            "SQL": 4,
            "Statistics": 5,
            "Machine Learning": 5,
            "Communication": 4
        }

        current = {
            "Python": python,
            "SQL": sql,
            "Statistics": statistics,
            "Machine Learning": machine_learning,
            "Communication": communication
        }

        st.subheader("📊 Your Skill Gap Analysis")

        for skill in required:
            gap = required[skill] - current[skill]

            if gap <= 0:
                st.success(f"✅ {skill}: Strong")
            elif gap == 1:
                st.warning(f"🟡 {skill}: Small gap")
            else:
                st.error(f"🔴 {skill}: Needs improvement")