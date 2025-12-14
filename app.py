import streamlit as st
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Career Recommendation System",
    layout="wide"
)

# ================= LOAD CSVs =================
career_df = pd.read_csv("career_master.csv")
company_df = pd.read_csv("career_companies_master.csvcsv")

# ================= SESSION STATE =================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ================= HEADER =================
st.markdown("""
<h1 style="text-align:center;">🎓 AI Career Recommendation System</h1>
<p style="text-align:center;color:gray;">
Skill-based Career Guidance for Engineering, Medical, Pharmacy, UG & PG Students
</p>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.markdown("## 👤 Student Profile")

# ---- Stream ----
stream = st.sidebar.selectbox(
    "Stream",
    sorted(career_df["stream"].unique())
)

# ---- Department (filtered by stream) ----
dept_df = career_df[career_df["stream"] == stream]
department = st.sidebar.selectbox(
    "Department",
    sorted(dept_df["department"].unique())
)

# ---- Role (filtered by department) ----
role_df = dept_df[dept_df["department"] == department]
role = st.sidebar.selectbox(
    "Interested Role",
    sorted(role_df["role"].unique())
)

cgpa = st.sidebar.slider("CGPA", 5.0, 10.0, 7.0, 0.1)
internship = st.sidebar.selectbox("Internship Completed?", ["Yes", "No"])

# ================= SKILLS =================
st.sidebar.markdown("## 🧠 Skill Self-Assessment")

role_row = career_df[
    (career_df["stream"] == stream) &
    (career_df["department"] == department) &
    (career_df["role"] == role)
].iloc[0]

tech_skills = role_row["technical_skills"].split("|")
core_skills = role_row["core_skills"].split("|")

st.sidebar.markdown("### 🛠️ Technical Skills")
tech_ratings = {}
for s in tech_skills:
    tech_ratings[s] = st.sidebar.slider(s, 1, 5, 3)

st.sidebar.markdown("### 🧩 Core Skills")
core_ratings = {}
for s in core_skills:
    core_ratings[s] = st.sidebar.slider(s, 1, 5, 3)

submit = st.sidebar.button("🔍 Get Recommendations")

# ================= PROCESS =================
if submit:
    st.session_state.submitted = True

if not st.session_state.submitted:
    st.info("👈 Fill profile and click **Get Recommendations**")
    st.stop()

# ================= SCORE LOGIC =================
avg_tech = sum(tech_ratings.values()) / len(tech_ratings)
avg_core = sum(core_ratings.values()) / len(core_ratings)

final_score = (
    (cgpa / 10) * 0.30 +
    (avg_tech / 5) * 0.35 +
    (avg_core / 5) * 0.25 +
    (0.10 if internship == "Yes" else 0)
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
    (company_df["stream"] == stream) &
    (company_df["department"] == department) &
    (company_df["role"] == role) &
    (company_df["company_level"].isin(levels))
]

if filtered.empty:
    st.warning("No companies found for this profile. Showing general options.")
    filtered = company_df[
        (company_df["stream"] == stream) &
        (company_df["department"] == department) &
        (company_df["role"] == role)
    ].head(5)

# ================= COMPANY TABLE =================
st.subheader("🏢 Company Recommendations")

st.dataframe(
    filtered[["company_name", "company_level", "locations"]],
    use_container_width=True,
    hide_index=True
)

# ================= MARKET INSIGHTS =================
st.subheader("🚀 Role-Based Market Insights")

cols = st.columns(2)
for i, (_, r) in enumerate(filtered.iterrows()):
    with cols[i % 2]:
        st.markdown(f"""
        <div style="
            background:#020617;
            border:1px solid #1e293b;
            border-radius:16px;
            padding:16px;
            margin-bottom:16px;
        ">
            <h4 style="color:#38bdf8;">🏢 {r.company_name}</h4>
            <p>👨‍💻 <b>Role:</b> {r.role}</p>
            <p>🎓 <b>Department:</b> {department}</p>
            <p>⭐ <b>Level:</b> {r.company_level}</p>
            <p>📍 <b>Locations:</b> {r.locations}</p>
            <p>🛠️ <b>Skills:</b> {", ".join(tech_skills)}</p>
        </div>
        """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(
    "<p style='text-align:center;color:gray;'>Built with ❤️ using Data Science & AI</p>",
    unsafe_allow_html=True
)

