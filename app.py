import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("Career_Master_Companies.csv")

df = load_data()

# ---------------- SESSION STATE ----------------
if "stream_loaded" not in st.session_state:
    st.session_state.stream_loaded = False
if "dept_loaded" not in st.session_state:
    st.session_state.dept_loaded = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ---------------- STYLES ----------------
st.markdown("""
<style>
body { background:#020617; }
.card {
    background:#020617;
    border:1px solid #1e293b;
    border-radius:16px;
    padding:20px;
    margin-bottom:18px;
    box-shadow:0 10px 25px rgba(0,0,0,0.4);
}
.title { font-size:38px; font-weight:800; color:#e5e7eb; }
.subtitle { color:#94a3b8; font-size:16px; }
.badge {
    display:inline-block;
    padding:6px 14px;
    border-radius:999px;
    font-size:13px;
    border:1px solid #334155;
    color:#38bdf8;
}
.tech {
    background:#020617;
    border:1px solid #334155;
    border-radius:12px;
    padding:10px;
    margin-top:8px;
    color:#e5e7eb;
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

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- STUDENT FORM ----------------
with st.form("career_form"):

    st.markdown("## 👤 Student Profile")

    # ---------- STREAM ----------
    stream = st.selectbox(
        "🎓 Select Stream",
        sorted(df["stream"].unique())
    )

    load_dept = st.form_submit_button("➡️ Load Departments")

    if load_dept:
        st.session_state.stream_loaded = True
        st.session_state.dept_loaded = False
        st.session_state.submitted = False

    # ---------- DEPARTMENT ----------
    if st.session_state.stream_loaded:
        departments = sorted(df[df["stream"] == stream]["department"].unique())

        department = st.selectbox(
            "🏫 Select Department",
            departments
        )

        load_roles = st.form_submit_button("➡️ Load Roles")

        if load_roles:
            st.session_state.dept_loaded = True
            st.session_state.submitted = False

    # ---------- ROLE ----------
    if st.session_state.stream_loaded and st.session_state.dept_loaded:
        roles = sorted(
            df[
                (df["stream"] == stream) &
                (df["department"] == department)
            ]["job_role"].unique()
        )

        role = st.selectbox(
            "💼 Select Interested Role",
            roles
        )

        cgpa = st.slider("📊 CGPA / Score", 5.0, 10.0, 7.0, 0.1)
        internship = st.selectbox("🧑‍💻 Internship Experience", ["Yes", "No"])

        submit = st.form_submit_button("🚀 Get Career Recommendations")

        if submit:
            st.session_state.submitted = True

# ---------------- RESULTS ----------------
if st.session_state.submitted:

    st.markdown("<br>", unsafe_allow_html=True)

    # -------- PROFILE CARD --------
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

    # -------- FILTER COMPANIES --------
    result_df = df[
        (df["stream"] == stream) &
        (df["department"] == department) &
        (df["job_role"] == role)
    ]

    if result_df.empty:
        st.warning("⚠️ No exact matches found. Showing similar companies.")
        result_df = df[df["stream"] == stream].head(6)
    else:
        result_df = result_df.head(9)

    # -------- COMPANY CARDS --------
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
                <div class="tech">
                    🛠️ <b>Technologies to Learn:</b><br>
                    {row.technologies}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<br><br>
<p style="text-align:center;color:#64748b;">
Built with ❤️ using Streamlit & Data Science
</p>
""", unsafe_allow_html=True)
