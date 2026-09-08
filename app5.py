import streamlit as st
import pandas as pd
import re
from pathlib import Path


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Skill Gap and Employment Analysis",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# WHITE BACKGROUND + SIMPLE STYLING
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #ffe6f0;
    }

    h1, h2, h3 {
        color: #1f2937 !important;
    }

    p, label {
        color: #222222 !important;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background-color: white !important;
        color: black !important;
        border: 2px solid #42a5f5 !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="select"] {
        background-color: white !important;
    }

    div[data-baseweb="select"] * {
        color: black !important;
    }

    .stButton > button {
        background-color: #2196f3 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
    }

    .stButton > button:hover {
        background-color: #1565c0 !important;
        color: white !important;
    }

    div[data-testid="stMetric"] {
        background-color: white !important;
        border: 2px solid #42a5f5 !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }

    div[data-testid="stMetricLabel"] {
        color: black !important;
    }

    div[data-testid="stMetricLabel"] * {
        color: black !important;
    }

    div[data-testid="stMetricValue"] {
        color: black !important;
    }

    div[data-testid="stMetricValue"] * {
        color: black !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

if "selected_career" not in st.session_state:
    st.session_state.selected_career = None


# =========================================================
# PROJECT DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# FIND RESUME DATASET
# =========================================================

resume_files = [
    BASE_DIR / "AI_Resume_Screening_Cleaned.csv",
    BASE_DIR / "AI_Resume_Screening.csv"
]

RESUME_FILE = None

for file in resume_files:

    if file.exists():

        RESUME_FILE = file
        break


# =========================================================
# FIND JOB DATASET
# =========================================================

job_files = [
    BASE_DIR / "Indian_CSE_Job_Market_Cleaned.xlsx",
    BASE_DIR / "Indian_Job_Market_Cleaned.xlsx"
]

JOB_FILE = None

for file in job_files:

    if file.exists():

        JOB_FILE = file
        break


# =========================================================
# FALLBACK CSV
# =========================================================

if RESUME_FILE is None:

    csv_files = list(BASE_DIR.glob("*.csv"))

    if csv_files:

        RESUME_FILE = csv_files[0]


# =========================================================
# FALLBACK EXCEL
# =========================================================

if JOB_FILE is None:

    excel_files = list(BASE_DIR.glob("*.xlsx"))

    if excel_files:

        JOB_FILE = excel_files[0]


# =========================================================
# CHECK JOB DATASET
# =========================================================

if JOB_FILE is None:

    st.error(
        "❌ Indian job-market dataset was not found."
    )

    st.info(
        "Place the Excel dataset in the same folder as app1.py."
    )

    st.stop()


# =========================================================
# LOAD JOB DATASET
# =========================================================

try:

    job_market_df = pd.read_excel(JOB_FILE)

except Exception as e:

    st.error(
        "❌ Error while reading the job-market dataset."
    )

    st.write(str(e))

    st.stop()


# =========================================================
# LOAD RESUME DATASET
# =========================================================

if RESUME_FILE is not None:

    try:

        resume_df = pd.read_csv(RESUME_FILE)

    except Exception:

        resume_df = pd.DataFrame()

else:

    resume_df = pd.DataFrame()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

job_market_df.columns = (
    job_market_df.columns
    .astype(str)
    .str.strip()
)

if not resume_df.empty:

    resume_df.columns = (
        resume_df.columns
        .astype(str)
        .str.strip()
    )


# =========================================================
# JOB ROLES
# =========================================================

roles = [
    "Software Engineer",
    "Data Scientist",
    "AI Researcher",
    "Cybersecurity Analyst"
]


# =========================================================
# EDUCATION OPTIONS
# =========================================================

education_options = [
    "B.Tech",
    "B.E",
    "BCA",
    "B.Sc",
    "MCA",
    "M.Tech",
    "M.E",
    "M.Sc",
    "Other"
]


# =========================================================
# EDUCATION RELEVANCE
# =========================================================

education_relevance = {

    "Software Engineer": [
        "B.Tech",
        "B.E",
        "BCA",
        "MCA",
        "M.Tech",
        "M.E",
        "B.Sc",
        "M.Sc"
    ],

    "Data Scientist": [
        "B.Tech",
        "B.E",
        "B.Sc",
        "M.Sc",
        "M.Tech",
        "M.E",
        "MCA"
    ],

    "AI Researcher": [
        "B.Tech",
        "B.E",
        "M.Tech",
        "M.E",
        "M.Sc",
        "MCA"
    ],

    "Cybersecurity Analyst": [
        "B.Tech",
        "B.E",
        "BCA",
        "MCA",
        "M.Tech",
        "M.E",
        "B.Sc",
        "M.Sc"
    ]
}


# =========================================================
# FALLBACK SKILLS
# =========================================================

fallback_skills = {

    "Software Engineer": [
        "python",
        "java",
        "c++",
        "sql",
        "javascript",
        "html",
        "css",
        "git",
        "software development",
        "agile"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "pandas",
        "numpy",
        "machine learning",
        "statistics",
        "data analysis",
        "power bi",
        "excel",
        "scikit-learn"
    ],

    "AI Researcher": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas",
        "statistics",
        "research",
        "artificial intelligence"
    ],

    "Cybersecurity Analyst": [
        "cybersecurity",
        "networking",
        "linux",
        "python",
        "sql",
        "computer networks",
        "information security",
        "ethical hacking",
        "firewall",
        "security"
    ]
}


# =========================================================
# NORMALIZE SKILL
# =========================================================

def normalize_skill(skill):

    skill = str(skill).strip().lower()

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    skill = skill.replace(
        "_",
        " "
    )

    aliases = {

        "ml": "machine learning",
        "m.l": "machine learning",
        "machine-learning": "machine learning",
        "machinelearning": "machine learning",

        "ai": "artificial intelligence",
        "a.i": "artificial intelligence",
        "artificial-intelligence":
            "artificial intelligence",
        "artificialintelligence":
            "artificial intelligence",

        "nlp":
            "natural language processing",

        "n.l.p":
            "natural language processing",

        "natural-language-processing":
            "natural language processing",

        "dl":
            "deep learning",

        "d.l":
            "deep learning",

        "deep-learning":
            "deep learning",

        "tf":
            "tensorflow",

        "tensor flow":
            "tensorflow",

        "py":
            "python",

        "js":
            "javascript",

        "java script":
            "javascript",

        "powerbi":
            "power bi",

        "power-bi":
            "power bi",

        "scikit learn":
            "scikit-learn",

        "c plus plus":
            "c++",

        "c sharp":
            "c#"
    }

    return aliases.get(
        skill,
        skill
    )


# =========================================================
# FIND ROLE COLUMN
# =========================================================

if "Common Job Role" in job_market_df.columns:

    role_column = "Common Job Role"

elif "title" in job_market_df.columns:

    role_column = "title"

else:

    st.error(
        "❌ Job dataset must contain 'Common Job Role' or 'title'."
    )

    st.stop()


# =========================================================
# FIND SKILL COLUMN
# =========================================================

if "tagsAndSkills" in job_market_df.columns:

    skill_column = "tagsAndSkills"

elif "Skills" in job_market_df.columns:

    skill_column = "Skills"

else:

    st.error(
        "❌ Job dataset must contain 'tagsAndSkills' or 'Skills'."
    )

    st.stop()


# =========================================================
# GET ROLE DATA
# =========================================================

def get_role_data(role):

    role_data = job_market_df[
        job_market_df[role_column]
        .astype(str)
        .str.lower()
        .str.contains(
            role.lower(),
            na=False
        )
    ]

    return role_data


# =========================================================
# GET ROLE SKILLS
# =========================================================

def get_role_skills(role):

    role_data = get_role_data(role)

    all_skills = []

    for skills in role_data[
        skill_column
    ].dropna():

        skill_list = re.split(
            r",|;|\||/",
            str(skills)
        )

        for skill in skill_list:

            normalized = normalize_skill(skill)

            if normalized:

                all_skills.append(
                    normalized
                )


    if all_skills:

        skill_counts = (
            pd.Series(all_skills)
            .value_counts()
        )

        skills = list(
            skill_counts.head(10).index
        )

    else:

        skills = [
            normalize_skill(skill)
            for skill in fallback_skills[role]
        ]


    if len(skills) < 3:

        skills = [
            normalize_skill(skill)
            for skill in fallback_skills[role]
        ]


    return list(
        dict.fromkeys(skills)
    )


# =========================================================
# CREATE ROLE SKILLS
# =========================================================

role_skills = {}

for role in roles:

    role_skills[role] = get_role_skills(role)


# =========================================================
# GET SKILL FREQUENCY FOR ROLE
# =========================================================

def get_skill_frequency(role, skill):

    role_data = get_role_data(role)

    if role_data.empty:

        return 0


    total_jobs = len(role_data)

    skill_count = 0


    for skills in role_data[
        skill_column
    ].fillna(""):

        skill_list = re.split(
            r",|;|\||/",
            str(skills)
        )


        normalized_skills = [

            normalize_skill(skill_item)

            for skill_item in skill_list

            if str(skill_item).strip()
        ]


        if skill in normalized_skills:

            skill_count += 1


    if total_jobs == 0:

        return 0


    frequency = (
        skill_count
        /
        total_jobs
    ) * 100


    return round(
        frequency,
        1
    )


# =========================================================
# TRAINING RECOMMENDATIONS
# =========================================================

training = {

    "python":
        "Python for Data Analysis",

    "sql":
        "Advanced SQL",

    "java":
        "Java Programming",

    "javascript":
        "JavaScript Development",

    "machine learning":
        "Machine Learning Fundamentals",

    "deep learning":
        "Deep Learning Fundamentals",

    "natural language processing":
        "Natural Language Processing Fundamentals",

    "pandas":
        "Pandas for Data Analysis",

    "numpy":
        "NumPy for Data Science",

    "tensorflow":
        "TensorFlow Fundamentals",

    "pytorch":
        "PyTorch Fundamentals",

    "power bi":
        "Power BI Fundamentals",

    "excel":
        "Advanced Excel",

    "git":
        "Git and GitHub",

    "aws":
        "AWS Cloud Fundamentals",

    "linux":
        "Linux Fundamentals",

    "networking":
        "Computer Networking",

    "computer networks":
        "Computer Networking",

    "cybersecurity":
        "Cybersecurity Fundamentals",

    "information security":
        "Information Security Fundamentals",

    "html":
        "HTML Web Development",

    "css":
        "CSS Web Development",

    "c++":
        "C++ Programming",

    "c#":
        "C# Programming",

    "software development":
        "Software Development Fundamentals",

    "agile":
        "Agile Software Development",

    "statistics":
        "Statistics for Data Science",

    "data analysis":
        "Data Analysis Fundamentals",

    "scikit-learn":
        "Scikit-learn for Machine Learning",

    "ethical hacking":
        "Ethical Hacking Fundamentals",

    "firewall":
        "Network Security Fundamentals",

    "security":
        "Cybersecurity Fundamentals",

    "research":
        "Research Methodology",

    "artificial intelligence":
        "Artificial Intelligence Fundamentals"
}


# =========================================================
# RECOMMEND TRAINING
# =========================================================

def recommend_training(missing_skills):

    recommendations = []

    for skill in missing_skills:

        skill = normalize_skill(skill)

        if skill in training:

            course = training[skill]

            if course not in recommendations:

                recommendations.append(course)


    return recommendations


# =========================================================
# CALCULATE CAREER SCORE
# =========================================================

def calculate_career_score(
    candidate_skills,
    education,
    projects,
    role
):

    required_skills = role_skills.get(
        role,
        fallback_skills[role]
    )


    required_skills = [

        normalize_skill(skill)

        for skill in required_skills
    ]


    required_skills = list(
        dict.fromkeys(
            required_skills
        )
    )


    matching = [

        skill

        for skill in required_skills

        if skill in candidate_skills
    ]


    if len(required_skills) > 0:

        skill_score = (

            len(matching)

            /

            len(required_skills)

        ) * 100

    else:

        skill_score = 0


    if education in education_relevance.get(
        role,
        []
    ):

        education_score = 100

    else:

        education_score = 50


    project_score = min(
        projects * 10,
        100
    )


    final_score = (

        skill_score * 0.70

        +

        education_score * 0.20

        +

        project_score * 0.10
    )


    return round(
        min(
            max(
                final_score,
                0
            ),
            100
        ),
        1
    )


# =========================================================
# GET CAREER DETAILS
# =========================================================

def get_career_details(
    candidate_skills,
    career
):

    required_skills = role_skills.get(
        career,
        fallback_skills[career]
    )


    required_skills = [

        normalize_skill(skill)

        for skill in required_skills
    ]


    required_skills = list(
        dict.fromkeys(
            required_skills
        )
    )


    matching_skills = []

    missing_skills = []


    for skill in required_skills:

        if skill in candidate_skills:

            matching_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )


    if len(required_skills) > 0:

        skill_match = (

            len(matching_skills)

            /

            len(required_skills)

        ) * 100

    else:

        skill_match = 0


    skill_match = round(
        skill_match,
        1
    )


    recommended_training = recommend_training(
        missing_skills
    )


    return (
        matching_skills,
        missing_skills,
        recommended_training,
        skill_match
    )


# =========================================================
# DETERMINE SKILL PRIORITY
# =========================================================

def get_skill_priority(
    career,
    missing_skills
):

    high_priority = []

    medium_priority = []

    optional = []


    for skill in missing_skills:

        frequency = get_skill_frequency(
            career,
            skill
        )


        # ---------------------------------------------
        # HIGH PRIORITY
        # ---------------------------------------------

        if frequency >= 50:

            high_priority.append(
                (skill, frequency)
            )


        # ---------------------------------------------
        # MEDIUM PRIORITY
        # ---------------------------------------------

        elif frequency >= 20:

            medium_priority.append(
                (skill, frequency)
            )


        # ---------------------------------------------
        # OPTIONAL
        # ---------------------------------------------

        else:

            optional.append(
                (skill, frequency)
            )


    # -------------------------------------------------
    # FALLBACK PRIORITY
    # -------------------------------------------------

    # If the dataset does not contain enough
    # frequency information, use the skill order
    # to avoid leaving the sections empty.

    if (
        not high_priority
        and
        not medium_priority
        and
        missing_skills
    ):

        if len(missing_skills) >= 1:

            high_priority = [
                (
                    skill,
                    get_skill_frequency(
                        career,
                        skill
                    )
                )

                for skill in missing_skills[:3]
            ]


        if len(missing_skills) > 3:

            medium_priority = [
                (
                    skill,
                    get_skill_frequency(
                        career,
                        skill
                    )
                )

                for skill in missing_skills[3:6]
            ]


        if len(missing_skills) > 6:

            optional = [
                (
                    skill,
                    get_skill_frequency(
                        career,
                        skill
                    )
                )

                for skill in missing_skills[6:]
            ]


    return (
        high_priority,
        medium_priority,
        optional
    )


# =========================================================
# CAREER DETAILS PAGE
# =========================================================

if st.session_state.page == "career_details":

    data = st.session_state.analysis_data

    career = st.session_state.selected_career


    # =====================================================
    # BACK BUTTON
    # =====================================================

    if st.button(
        "← Back to Analysis Results"
    ):

        st.session_state.page = "results"

        st.rerun()


    st.divider()


    # =====================================================
    # CAREER TITLE
    # =====================================================

    st.title(
        f"💼 {career}"
    )


    st.write(
        f"Career analysis for **{data['name']}**"
    )


    st.write(
        f"🎓 Education: **{data['education']}**"
    )


    st.divider()


    # =====================================================
    # CAREER MATCH
    # =====================================================

    (
        matching_skills,
        missing_skills,
        recommended_training,
        career_skill_match
    ) = get_career_details(
        data["candidate_skills"],
        career
    )


    st.header(
        "📊 Career Match"
    )


    st.metric(
        "Skill Match",
        f"{career_skill_match:.1f}%"
    )


    # =====================================================
    # MATCHING SKILLS
    # =====================================================

    st.divider()

    st.subheader(
        "✅ Matching Skills"
    )


    if matching_skills:

        for skill in matching_skills:

            st.success(
                "✓ " + skill.title()
            )

    else:

        st.info(
            "No matching skills found."
        )


    # =====================================================
    # MISSING SKILLS
    # =====================================================

    st.divider()

    st.subheader(
        "⚠️ Missing Skills"
    )


    if missing_skills:

        for skill in missing_skills:

            st.warning(
                "• " + skill.title()
            )

    else:

        st.success(
            "🎉 No major skill gaps found!"
        )


    # =====================================================
    # SKILL PRIORITY
    # =====================================================

    st.divider()

    st.header(
        "🎯 Skill Priority"
    )


    st.write(
        "Not all missing skills are equally important. "
        "Priority is based on how frequently each skill "
        "appears in the job-market dataset for this career."
    )


    if missing_skills:

        (
            high_priority,
            medium_priority,
            optional
        ) = get_skill_priority(
            career,
            missing_skills
        )


        # =================================================
        # HIGH PRIORITY
        # =================================================

        st.subheader(
            "🚨 High Priority"
        )


        if high_priority:

            for skill, frequency in high_priority:

                st.error(
                    f"🔴 {skill.title()}  "
                    f"— Job demand: {frequency:.1f}%"
                )

        else:

            st.info(
                "No high-priority missing skills."
            )


        # =================================================
        # MEDIUM PRIORITY
        # =================================================

        st.subheader(
            "⚠️ Medium Priority"
        )


        if medium_priority:

            for skill, frequency in medium_priority:

                st.warning(
                    f"🟡 {skill.title()}  "
                    f"— Job demand: {frequency:.1f}%"
                )

        else:

            st.info(
                "No medium-priority missing skills."
            )


        # =================================================
        # OPTIONAL
        # =================================================

        st.subheader(
            "📚 Optional"
        )


        if optional:

            for skill, frequency in optional:

                st.info(
                    f"🔵 {skill.title()}  "
                    f"— Job demand: {frequency:.1f}%"
                )

        else:

            st.info(
                "No optional missing skills."
            )


    else:

        st.success(
            "🎉 No skill gaps found, so no priority "
            "training is required."
        )


    # =====================================================
    # RECOMMENDED TRAINING
    # =====================================================

    st.divider()

    st.subheader(
        "📚 Recommended Training"
    )


    if recommended_training:

        for course in recommended_training:

            st.info(
                "📘 " + course
            )

    else:

        st.success(
            "🎉 No additional training required."
        )


    # =====================================================
    # CAREER SUMMARY
    # =====================================================

    st.divider()

    st.subheader(
        "📌 Career Summary"
    )


    if career in education_relevance.get(
        career,
        []
    ):

        education_status = (
            "Your education is well aligned "
            "with this career."
        )

    else:

        education_status = (
            "Your education has moderate alignment "
            "with this career."
        )


    st.write(
        education_status
    )


    if missing_skills:

        st.write(
            "Focus first on the high-priority skills, "
            "followed by medium-priority skills. "
            "Optional skills can be learned later."
        )

    else:

        st.write(
            "You already have the identified skills "
            "required for this career."
        )


    st.caption(
        "Skill priority is estimated from the frequency "
        "of skills in the available job-market dataset."
    )


# =========================================================
# RESULTS PAGE
# =========================================================

elif st.session_state.page == "results":

    data = st.session_state.analysis_data


    # =====================================================
    # TITLE
    # =====================================================

    st.title(
        "📊 Candidate Analysis Results"
    )


    st.write(
        f"**Candidate Name:** {data['name']}"
    )


    st.write(
        f"**Education:** {data['education']}"
    )


    st.write(
        f"**Selected Role:** {data['selected_role']}"
    )


    st.write(
        f"**Number of Projects:** {data['projects']}"
    )


    # =====================================================
    # MAIN RESULTS
    # =====================================================

    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "📊 Skill Match",
            f"{data['skill_match']:.1f}%"
        )


    with col2:

        st.metric(
            "💼 Job Probability",
            f"{data['job_probability']:.1f}%"
        )


    # =====================================================
    # AI RECOMMENDED CAREERS
    # =====================================================

    st.divider()

    st.header(
        "🤖 AI Recommended Careers"
    )


    st.write(
        "Based on your skills, education and project experience:"
    )


    medals = [
        "🥇",
        "🥈",
        "🥉",
        "4️⃣"
    ]


    # =====================================================
    # CLICKABLE CAREERS
    # =====================================================

    for index, career_data in enumerate(
        data["career_scores"]
    ):

        career = career_data["role"]

        score = career_data["score"]


        button_text = (

            f"{medals[index]}  "
            f"{career}  —  {score:.1f}%  "
            f"➜ View Details"
        )


        if st.button(
            button_text,
            key=f"career_{index}",
            use_container_width=True
        ):

            st.session_state.selected_career = career

            st.session_state.page = "career_details"

            st.rerun()


    # =====================================================
    # JOB SUITABILITY
    # =====================================================

    st.divider()

    st.subheader(
        "💼 Job Suitability"
    )


    job_probability = data[
        "job_probability"
    ]


    if job_probability >= 80:

        st.success(
            "🟢 High job suitability. "
            "The candidate has a strong skill match."
        )

    elif job_probability >= 60:

        st.info(
            "🔵 Moderate to high job suitability. "
            "The candidate can improve further "
            "by developing missing skills."
        )

    elif job_probability >= 40:

        st.warning(
            "🟡 Moderate job suitability. "
            "Additional training is recommended."
        )

    else:

        st.error(
            "🔴 Low job suitability. "
            "The candidate has significant skill gaps."
        )


    # =====================================================
    # SUMMARY
    # =====================================================

    st.divider()

    st.subheader(
        "📌 Candidate Summary"
    )


    best_career = data[
        "career_scores"
    ][0]


    st.write(
        f"**{data['name']}** has a "
        f"**{data['skill_match']:.1f}%** skill match "
        f"for the **{data['selected_role']}** role."
    )


    st.write(
        f"The estimated job suitability is "
        f"**{data['job_probability']:.1f}%**."
    )


    st.write(
        f"The most suitable recommended career "
        f"is **{best_career['role']}** with a "
        f"score of **{best_career['score']:.1f}%**."
    )


    st.info(
        "💡 Click any recommended career above to view "
        "matching skills, missing skills, skill priority "
        "and recommended training on a separate page."
    )


# =========================================================
# HOME / CANDIDATE INPUT PAGE
# =========================================================

else:

    # =====================================================
    # TITLE
    # =====================================================

    st.title(
        "🎓 Skill Gap and Employment Analysis System"
    )


    st.write(
        "Analyze candidate skills, education, "
        "employment suitability and recommended careers."
    )


    st.divider()


    # =====================================================
    # CANDIDATE INFORMATION
    # =====================================================

    st.header(
        "👤 Candidate Information"
    )


    # =====================================================
    # NAME
    # =====================================================

    candidate_name = st.text_input(
        "Candidate Name",
        placeholder="Enter candidate name"
    )


    # =====================================================
    # EDUCATION
    # =====================================================

    education = st.selectbox(
        "🎓 Education",
        education_options
    )


    # =====================================================
    # SELECTED ROLE
    # =====================================================

    selected_role = st.selectbox(
        "Select Job Role",
        roles
    )


    # =====================================================
    # SKILLS
    # =====================================================

    candidate_skills_input = st.text_area(
        "Enter Candidate Skills",
        placeholder=(
            "Example: Python, ML, AI, SQL, Pandas"
        ),
        height=120
    )


    # =====================================================
    # PROJECTS
    # =====================================================

    projects_count = st.number_input(
        "Number of Projects",
        min_value=0,
        max_value=50,
        value=0,
        step=1
    )


    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

    analyze = st.button(
        "🔍 Analyze Candidate",
        use_container_width=True
    )


    # =====================================================
    # ANALYZE CANDIDATE
    # =====================================================

    if analyze:

        # -------------------------------------------------
        # VALIDATE NAME
        # -------------------------------------------------

        if candidate_name.strip() == "":

            st.warning(
                "⚠️ Please enter the candidate name."
            )

            st.stop()


        # -------------------------------------------------
        # VALIDATE SKILLS
        # -------------------------------------------------

        if candidate_skills_input.strip() == "":

            st.warning(
                "⚠️ Please enter at least one skill."
            )

            st.stop()


        # -------------------------------------------------
        # CANDIDATE SKILLS
        # -------------------------------------------------

        candidate_skills = [

            normalize_skill(skill)

            for skill in re.split(
                r",|;|\n",
                candidate_skills_input
            )

            if skill.strip()
        ]


        candidate_skills = list(
            dict.fromkeys(
                candidate_skills
            )
        )


        # -------------------------------------------------
        # REQUIRED SKILLS
        # -------------------------------------------------

        required_skills = role_skills.get(
            selected_role,
            fallback_skills[selected_role]
        )


        required_skills = [

            normalize_skill(skill)

            for skill in required_skills
        ]


        required_skills = list(
            dict.fromkeys(
                required_skills
            )
        )


        # -------------------------------------------------
        # MATCHING + MISSING SKILLS
        # -------------------------------------------------

        matching_skills = []

        missing_skills = []


        for required_skill in required_skills:

            if required_skill in candidate_skills:

                matching_skills.append(
                    required_skill
                )

            else:

                missing_skills.append(
                    required_skill
                )


        # -------------------------------------------------
        # SKILL MATCH
        # -------------------------------------------------

        if len(required_skills) > 0:

            skill_match = (

                len(matching_skills)
                /
                len(required_skills)

            ) * 100

        else:

            skill_match = 0


        skill_match = round(
            skill_match,
            2
        )


        # -------------------------------------------------
        # JOB PROBABILITY
        # -------------------------------------------------

        project_score = min(
            projects_count * 2,
            10
        )


        job_probability = (

            skill_match * 0.90

            +

            project_score
        )


        job_probability = min(
            max(
                job_probability,
                0
            ),
            100
        )


        job_probability = round(
            job_probability,
            2
        )


        # -------------------------------------------------
        # RECOMMENDED CAREERS
        # -------------------------------------------------

        career_scores = []


        for role in roles:

            score = calculate_career_score(

                candidate_skills,

                education,

                projects_count,

                role
            )


            career_scores.append({

                "role": role,

                "score": score

            })


        # -------------------------------------------------
        # SORT CAREERS
        # -------------------------------------------------

        career_scores = sorted(

            career_scores,

            key=lambda x: x["score"],

            reverse=True
        )


        # -------------------------------------------------
        # SAVE DATA
        # -------------------------------------------------

        st.session_state.analysis_data = {

            "name":
                candidate_name,

            "education":
                education,

            "selected_role":
                selected_role,

            "candidate_skills":
                candidate_skills,

            "projects":
                projects_count,

            "skill_match":
                skill_match,

            "job_probability":
                job_probability,

            "career_scores":
                career_scores
        }


        # -------------------------------------------------
        # OPEN RESULTS
        # -------------------------------------------------

        st.session_state.page = "results"

        st.rerun()