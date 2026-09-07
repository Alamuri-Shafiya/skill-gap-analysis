import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Skill Gap Analysis",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background-color: #eef7ff;
}

h1 {
    color: #163172;
    text-align: center;
    font-size: 38px;
}

h2, h3 {
    color: #1e3a5f;
}

.subtitle {
    text-align: center;
    color: #5c677d;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.skill-match {
    background-color: #d9f2e6;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

.missing {
    background-color: #fff0d9;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.training {
    background-color: #dceeff;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    "<h1>🎓 AI-Based Skill Gap and Training Recommendation System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze candidate skills, identify skill gaps, and recommend suitable training.</div>',
    unsafe_allow_html=True
)


df = pd.read_excel("Skill_Gap_Training_Recommendations.xlsx")


st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🔍 Select Job Role")

roles = df["Job Role"].dropna().unique()

selected_role = st.selectbox(
    "Choose a Job Role",
    roles
)

st.markdown('</div>', unsafe_allow_html=True)


role_data = df[df["Job Role"] == selected_role]


st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("👤 Select Candidate")

candidate_ids = role_data["Resume_ID"].tolist()

selected_candidate = st.selectbox(
    "Choose Candidate",
    candidate_ids
)

st.markdown('</div>', unsafe_allow_html=True)


candidate = role_data[
    role_data["Resume_ID"] == selected_candidate
].iloc[0]


st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("👤 Candidate Details")

col1, col2 = st.columns(2)

with col1:
    st.write("**Resume ID:**", candidate["Resume_ID"])

with col2:
    st.write("**Job Role:**", candidate["Job Role"])

st.write("**Candidate Skills:**")
st.write(candidate["Candidate Skills"])

st.markdown('</div>', unsafe_allow_html=True)


st.subheader("📊 Skill Match")

st.markdown(
    f"""
    <div class="skill-match">
        <h3>Overall Skill Match</h3>
        <h1>{candidate["Skill Match %"]}%</h1>
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="card">
            <h3>✅ Matching Skills</h3>
            <p>{candidate["Matching Skills"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="missing">
            <h3>⚠️ Missing Skills</h3>
            <p>{candidate["Missing Skills"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    f"""
    <div class="training">
        <h3>📚 Recommended Training</h3>
        <p>{candidate["Recommended Training"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)