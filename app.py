import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# ---------------- LOAD CSV ----------------
@st.cache_data
def load_data():
    return pd.read_csv("Career_Master_Companies.csv")

df = load_data()

# ---------------- BASIC VALIDATION ----------------
required_cols = ["stream", "department", "job_role",
                 "company_name", "company_level", "company_locations"]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"CSV missing columns: {missing}")
    st.stop()

# ---------------- STYLES ----------------
st.markdown("""
<style>
body { background:#020617; }
.card {
    background:#020617;
    border:1px solid #1e293b;
    border-radius:18px;
    padding:20px;
    margin-bottom:16px;
}
.title { font-size:38px;font-weight:800;color:#e5e7eb; }
.subtitle { color:#94a3b8;font-size:16px; }
.badge {
    padding:4px 12px;
    border-radius:999px;
    border:1px solid #334155;
    color:#38bdf8;
    font-size:12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="card">
  <div class="title">🎓 AI Career Recommendation System</div>
  <div class="subtitle">Stream → Department → Role based career guidance</div>
</div>
""", unsafe_allow_html=True)

# ---------------- FORM ----------------
with st.form("career_form"):
    st.markdown("### 👤 Student Profile")

    c1, c2, c3 = st.columns(3)

    # STREAM
    with c1:
        stream = st.selectbox(
            "🎓 Stream",
            sorted(df["stream"].dropna().unique())
        )

    # DEPARTMENT (FILTERED BY STREAM)
    with c2:
        dept_options = (
            df[df["stream"] == stream]["department"]
            .dropna()
            .unique()
        )
        department = st.selectbox(
            "🏫 Department",
            sorted(dept_options)
        )

    # ROLE (FILTERED BY STREAM + DEPARTMENT)
    with c3:
        role_options = (
            df[
                (df["stream"] == stream) &
                (df["department"] == department)
            ]["job_role"]
            .dropna()
            .unique()
        )
        role = st.selectbox(
            "💼 Interested Role",
            sorted(role_options)
        )

    c4, c5 = st.columns(2)

    with c4:
        cgpa = st.slider("📊 CGPA / Score", 5.0, 10.0, 7.0, 0.1)

    with c5:
        internship = st.selectbox("🧑‍💻 Internship Experience", ["Yes", "No"])

    submitted = st.form_submit_button("🚀 Get Career Recommendations")

# ---------------- RESULTS ----------------
if submitted:

    # PROFILE SUMMARY
    st.markdown(f"""
    <div class="card">
        <h3>👤 Student Profile</h3>
        <p><b>Stream:</b> {stream}</p>
        <p><b>Department:</b> {department}</p>
        <p><b>Role:</b> {role}</p>
        <p><b>CGPA:</b> {cgpa}</p>
        <p><b>Internship:</b> {internship}</p>
    </div>
    """, unsafe_allow_html=True)

    # FILTER COMPANIES
    result_df = df[
        (df["stream"] == stream) &
        (df["department"] == department) &
        (df["job_role"] == role)
    ]

    if result_df.empty:
        st.warning("⚠️ No exact matches found. Showing related companies.")
        result_df = df[
            (df["stream"] == stream) &
            (df["department"] == department)
        ].head(6)
    else:
        result_df = result_df.head(9)

    # COMPANY CARDS
    st.markdown("## 🏢 Recommended Companies")

    cols = st.columns(3)
    for i, (_, row) in enumerate(result_df.iterrows()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <h3>🏢 {row.company_name}</h3>
                <span class="badge">{row.company_level} LEVEL</span>
                <p style="margin-top:10px;">💼 <b>Role:</b> {row.job_role}</p>
                <p>📍 <b>Locations:</b> {row.company_locations}</p>
                <p>🎓 <b>Stream:</b> {row.stream}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<br>
<p style="text-align:center;color:#64748b;">
Built with ❤️ using Streamlit & Data Science
</p>
""", unsafe_allow_html=True)
