import streamlit as st
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Career Recommendation System",
    layout="wide"
)

# ================= LOAD DATA =================
career_df = pd.read_csv("career_master.csv")
company_df = pd.read_csv("career_companies_master.csv")

# ================= SESSION STATE =================
for key, val in {
    "submitted": False,
    "department": None,
    "role": None,
    "cgpa": 7.0,
    "internship": "No",
    "tech_ratings": {},
    "core_ratings": {}
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ================= CUSTOM CSS =================
st.markdown("""
<style>
body {
    background-color: #020617;
}
.block {
    background:#020617;
    border:1px solid #1e293b;
    border-radius:16px;
    padding:18px;
    margin-bottom:18px;
}
.card-title {
    color:#38bdf8;
    font-size:18px;
    font-weight:600;
}
.sub {
    color:#cbd5f5;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
col1, col2 = st.columns([3, 7])

with col2:
    st.markdown("""
    <h1 style="color:white;">🎓 AI Career Recommendation System</h1>
    <p style="color:#94a3b8;">
    Department-aware • Role-based • Skill-driven
    </p>
    """, unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.markdown("## 👤 Student Profile")

# Department
departments = sorted(career_df["department"].unique())
st.session_state.department = st.sidebar.selectbox(
    "Department", departments
)

# Role (filtered by department)
roles = career_df[
    career_df["department"] == st.session_state.department
]["role"].unique()

st.session_state.role = st.sidebar.selectbox(
    "Interested Role", sorted(roles)
)

st.session_state.cgpa = st.sidebar.slider("CGPA", 5.0, 10.0, 7.0, 0.1)
st.session_state.internship = st.sidebar.selectbox(
    "Internship Completed?", ["Yes", "No"]
)

# ================= SKILLS =================
st.sidebar.markdown("## 🧠 Skill Self-Assessment")

role_row = career_df[
    (career_df["department"] == st.session_state.department) &
    (career_df["role"] == st.session_state.role)
].iloc[0]

tech_skills = role_row["technical_skills"].split("|")
core_skills = role_row["core_skills"].split("|")

st.sidebar.markdown("### 🛠️ Technical Skills")
st.session_state.tech_ratings = {}
for s in tech_skills:
    st.session_state.tech_ratings[s] = st.sidebar.slider(s, 1, 5, 3)

st.sidebar.markdown("### 🧩 Core Skills")
st.session_state.core_ratings = {}
for s in core_skills:
    st.session_state.core_ratings[s] = st.sidebar.slider(s, 1, 5, 3)

submit = st.sidebar.button("🔍 Get Recommendations")

# ================= PROCESS =================
if submit:
    st.session_state.submitted = True

if not st.session_state.submitted:
    st.info("👉 Fill profile and click **Get Recommendations**")
    st.stop()

# ================= SCORE =================
avg_tech = sum(st.session_state.tech_ratings.values()) / len(st.session_state.tech_ratings)
avg_core = sum(st.session_state.core_ratings.values()) / len(st.session_state.core_ratings)

final_score = (
    (st.session_state.cgpa / 10) * 0.30 +
    (avg_tech / 5) * 0.35 +
    (avg_core / 5) * 0.25 +
    (0.10 if st.session_state.internship == "Yes" else 0)
)

if final_score >= 0.70:
    profile = "🔵 Advanced Profile"
    levels = ["HIGH", "MID", "LOW"]
elif final_score >= 0.45:
    profile = "🟡 Intermediate Profile"
    levels = ["MID", "LOW"]
else:
    profile = "🟢 Beginner Profile"
    levels = ["LOW"]

st.success(profile)

# ================= COMPANY FILTER =================
filtered = company_df[
    (company_df["role"] == st.session_state.role) &
    (company_df["department"] == st.session_state.department) &
    (company_df["company_level"].isin(levels))
]

# ================= TABLE =================
st.subheader("🏢 Company Recommendations")
st.dataframe(
    filtered[["company_name", "role", "company_level"]],
    use_container_width=True,
    hide_index=True
)

# ================= MARKET INSIGHTS =================
st.subheader("🚀 Role-Based Market Insights")

cols = st.columns(2)
for i, (_, r) in enumerate(filtered.iterrows()):
    with cols[i % 2]:
        st.markdown(f"""
        <div class="block">
            <div class="card-title">🏢 {r.company_name}</div>
            <p class="sub">👨‍💻 Role: {r.role}</p>
            <p class="sub">🎓 Stream: {r.department}</p>
            <p class="sub">📍 Branches: {r.locations}</p>
            <p class="sub">🛠️ Technologies: {", ".join(tech_skills)}</p>
        </div>
        """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(
    "<p style='text-align:center;color:#94a3b8;'>Built with ❤️ using Data Science & AI</p>",
    unsafe_allow_html=True
)
