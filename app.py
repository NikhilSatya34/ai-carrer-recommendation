import streamlit as st
import pandas as pd

# ---------------- STREAM → DEPARTMENT MAP ----------------
STREAM_DEPT_MAP = {
    "Engineering": ["AIDS", "AIML", "CSE", "ECE", "EEE", "Civil", "Mechanical"],
    "Medical": ["MBBS", "Nursing", "Physiotherapy"],
    "Pharma": ["B.Pharmacy", "M.Pharmacy", "D.Pharmacy"],
    "UG": ["B.A", "B.Sc", "B.Com"],
    "PG": ["M.Sc", "M.Tech", "MBA", "MCA"]
}

# ---------------- DEPARTMENT → ROLE MAP ----------------
DEPT_ROLE_MAP = {
    # Engineering
    "AIDS": ["AI Engineer", "ML Engineer", "Data Scientist"],
    "AIML": ["AI Engineer", "ML Engineer", "Research Scientist"],
    "CSE": ["Software Engineer", "Backend Developer", "Frontend Developer", "Full Stack Developer"],
    "ECE": ["Embedded Engineer", "VLSI Engineer"],
    "EEE": ["Electrical Engineer", "Power Systems Engineer"],
    "Civil": ["Site Engineer", "Structural Engineer"],
    "Mechanical": ["Design Engineer", "Production Engineer"],

    # Medical
    "MBBS": ["Junior Doctor", "Medical Officer"],
    "Nursing": ["Staff Nurse", "ICU Nurse"],
    "Physiotherapy": ["Physiotherapist"],

    # Pharma
    "B.Pharmacy": ["Pharmacist", "Medical Representative"],
    "M.Pharmacy": ["Clinical Research Associate"],
    "D.Pharmacy": ["Retail Pharmacist"],

    # UG
    "B.A": ["Content Writer", "HR Executive"],
    "B.Sc": ["Research Assistant", "Lab Assistant"],
    "B.Com": ["Accountant", "Audit Assistant"],

    # PG
    "M.Sc": ["Data Analyst", "Research Scientist"],
    "M.Tech": ["Senior Engineer", "Solution Architect"],
    "MBA": ["Business Analyst", "Product Manager"],
    "MCA": ["Software Engineer", "System Analyst"]
}

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# -------------------- LOAD DATA --------------------
path_df = pd.read_csv("career_path_master.csv")
company_df = pd.read_csv("Career_Master_Companies.csv")

# -------------------- STYLES --------------------
st.markdown("""
<style>
body { background-color:#020617; }
.card {
    background:#020617;
    border:1px solid #1e293b;
    border-radius:18px;
    padding:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.35);
}
.title { font-size:40px;font-weight:800;color:#e5e7eb; }
.subtitle { color:#94a3b8;font-size:18px; }
.badge {
    display:inline-block;
    padding:6px 14px;
    border-radius:999px;
    font-size:13px;
    border:1px solid #334155;
    color:#38bdf8;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class="card">
  <div class="title">🎓 AI Career Recommendation System</div>
  <div class="subtitle">
    Stream → Department → Role based career guidance
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.form("career_form"):

    st.markdown("### 👤 Student Profile")

    col1, col2, col3 = st.columns(3)

    # ---------- STREAM ----------
    with col1:
        stream = st.selectbox(
            "🎓 Stream",
            list(STREAM_DEPT_MAP.keys()),
            key="stream"
        )

    # ---------- RESET ON STREAM CHANGE ----------
    if "prev_stream" not in st.session_state:
        st.session_state.prev_stream = stream

    if st.session_state.prev_stream != stream:
        st.session_state.department = None
        st.session_state.role = None
        st.session_state.prev_stream = stream

    # ---------- DEPARTMENT ----------
    with col2:
        department = st.selectbox(
            "🏫 Department",
            STREAM_DEPT_MAP.get(stream, []),
            key="department"
        )

    # ---------- RESET ON DEPARTMENT CHANGE ----------
    if "prev_department" not in st.session_state:
        st.session_state.prev_department = department

    if st.session_state.prev_department != department:
        st.session_state.role = None
        st.session_state.prev_department = department

    # ---------- ROLE ----------
    with col3:
        role = st.selectbox(
            "💼 Interested Role",
            DEPT_ROLE_MAP.get(department, []),
            key="role"
        )

    # ---------- CGPA + INTERNSHIP ----------
    col4, col5 = st.columns(2)

    with col4:
        cgpa = st.slider("📊 CGPA / Score", 5.0, 10.0, 7.0, 0.1)

    with col5:
        internship = st.selectbox("🧑‍💻 Internship Experience", ["Yes", "No"])

    submitted = st.form_submit_button("🚀 Get Career Recommendations")

# -------------------- RESULTS --------------------
if submitted:

    st.markdown("<br>", unsafe_allow_html=True)

    # -------- PROFILE CARD --------
    st.markdown(f"""
    <div class="card">
        <h3 style="color:#e5e7eb;">👤 Student Profile</h3>
        <p><b>Stream:</b> {stream}</p>
        <p><b>Department:</b> {department}</p>
        <p><b>Interested Role:</b> {role}</p>
        <p><b>CGPA:</b> {cgpa}</p>
        <p><b>Internship:</b> {internship}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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
                <h3 style="color:#e5e7eb;">🏢 {row.company_name}</h3>
                <span class="badge">{row.company_level} LEVEL</span>
                <p style="margin-top:12px;">💼 <b>Role:</b> {row.job_role}</p>
                <p>📍 <b>Locations:</b> {row.company_locations}</p>
                <p>🎓 <b>Stream:</b> {row.stream}</p>
            </div>
            """, unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown("""
<br><br>
<p style="text-align:center;color:#64748b;">
Built with ❤️ using Streamlit & Data Science
</p>
""", unsafe_allow_html=True)




