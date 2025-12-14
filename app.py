import streamlit as st
import pandas as pd

def filter_companies_by_cgpa(df, stream, department, role, cgpa, mode="recommended"):
    base_df = df[
        (df["stream"] == stream) &
        (df["department"] == department)
    ]

    if mode == "recommended":
        role_df = base_df[base_df["job_role"] == role]
    else:
        role_df = base_df[base_df["job_role"] != role]

    if cgpa < 6.5:
        result = role_df[role_df["company_level"] == "STARTUP"].head(5)

    elif 6.5 <= cgpa < 8.5:
        mid = role_df[role_df["company_level"] == "MID"].head(5)
        startup = role_df[role_df["company_level"] == "STARTUP"].head(4)
        result = pd.concat([mid, startup])

    else:
        high = role_df[role_df["company_level"] == "HIGH"].head(5)
        mid = role_df[role_df["company_level"] == "MID"].head(4)
        startup = role_df[role_df["company_level"] == "STARTUP"].head(3)
        result = pd.concat([high, mid, startup])

    if result.empty:
        result = base_df.head(6)

    return result.drop_duplicates("company_name")

st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("Master_Companies_Technologies.csv")

df = load_data()

# --------------------------------------------------
# STYLES
# --------------------------------------------------
st.markdown("""
<style>
body { background-color:#020617; }

.card {
    background: linear-gradient(145deg,#020617,#020617);
    border:1px solid #1e293b;
    border-radius:18px;
    padding:20px;
    margin-bottom:20px;
    box-shadow:0 15px 40px rgba(0,0,0,0.4);
}

.title {
    font-size:42px;
    font-weight:800;
    color:#e5e7eb;
}

.subtitle {
    color:#94a3b8;
    font-size:17px;
}

.badge {
    display:inline-block;
    padding:6px 14px;
    border-radius:999px;
    font-size:13px;
    margin-top:6px;
    border:1px solid #334155;
    color:#38bdf8;
}

.company-title {
    font-size:20px;
    font-weight:700;
    color:#e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="card">
  <div class="title">🎓 AI Career Recommendation System</div>
  <div class="subtitle">
    Stream → Department → Role based smart career guidance
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "load_dept" not in st.session_state:
    st.session_state.load_dept = False
if "load_role" not in st.session_state:
    st.session_state.load_role = False

# --------------------------------------------------
# FORM
# --------------------------------------------------
with st.form("career_form"):
    st.markdown("## 👤 Student Profile")

    col1, col2, col3 = st.columns(3)

    # -------- STREAM --------
    with col1:
        stream = st.selectbox(
            "🎓 Select Stream",
            sorted(df["stream"].unique())
        )

        if st.form_submit_button("📂 Load Departments"):
            st.session_state.load_dept = True
            st.session_state.load_role = False

    # -------- DEPARTMENT --------
    with col2:
        if st.session_state.load_dept:
            dept_list = sorted(df[df["stream"] == stream]["department"].unique())
            department = st.selectbox("🏫 Select Department", dept_list)
        else:
            department = None
            st.info("Select stream & click Load Departments")

        if department and st.form_submit_button("🧭 Load Roles"):
            st.session_state.load_role = True

    # -------- ROLE --------
    with col3:
        if st.session_state.load_role:
            role_list = sorted(
                df[
                    (df["stream"] == stream) &
                    (df["department"] == department)
                ]["job_role"].unique()
            )
            role = st.selectbox("💼 Interested Role", role_list)
        else:
            role = None
            st.info("Select department & click Load Roles")

    col4, col5 = st.columns(2)

    with col4:
        cgpa = st.slider("📊 CGPA / Score", 5.0, 10.0, 7.0, 0.1)

    with col5:
        internship = st.selectbox("🧑‍💻 Internship Experience", ["Yes", "No"])

    submit = st.form_submit_button("🚀 Get Career Recommendations")

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
if submit and role:

    # -------- PROFILE CARD --------
    st.markdown(f"""
    <div class="card">
        <h3 style="color:#e5e7eb;">👤 Student Profile</h3>
        <p><b>Stream:</b> {stream}</p>
        <p><b>Department:</b> {department}</p>
        <p><b>Role:</b> {role}</p>
        <p><b>CGPA:</b> {cgpa}</p>
        <p><b>Internship:</b> {internship}</p>
    </div>
    """, unsafe_allow_html=True)

    
    result_df = filter_companies_by_cgpa(
        df, stream, department, role, cgpa, mode="recommended"
    )

    st.markdown("## 🏢 Recommended Companies")

    cols = st.columns(3)
    for i, (_, row) in enumerate(result_df.iterrows()):
        with cols[i % 3]:
            techs = row["technologies"] if pd.notna(row["technologies"]) else "Not specified"
            st.markdown(f"""
            <div class="card">
                <div class="company-title">🏢 {row.company_name}</div>
                <span class="badge">{row.company_level}</span>
                <p><b>Role:</b> {row.job_role}</p>
                <p><b>Location:</b> {row.company_locations}</p>
                <p><b>Technologies:</b><br>{techs}</p>
            </div>
            """, unsafe_allow_html=True)

    # -------------------- ALTERNATE COMPANIES --------------------

alternate_df = filter_companies_by_cgpa(
    df, stream, department, role, cgpa, mode="alternate"
)

st.markdown("## 🔁 Alternate Companies (Same Department)")

cols = st.columns(3)
for i, (_, row) in enumerate(alternate_df.iterrows()):
    with cols[i % 3]:
        techs = row["technologies"] if pd.notna(row["technologies"]) else "Not specified"
        st.markdown(f"""
        <div class="card">
            <div class="company-title">🏢 {row.company_name}</div>
            <span class="badge">{row.company_level}</span>
            <p><b>Alternate Role:</b> {row.job_role}</p>
            <p><b>Location:</b> {row.company_locations}</p>
            <p><b>Technologies:</b><br>{techs}</p>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<br><br>
<p style="text-align:center;color:#64748b;">
Built with ❤️ using Streamlit & Data Science
</p>
""", unsafe_allow_html=True)






