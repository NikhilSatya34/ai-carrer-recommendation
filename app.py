import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Master_Comapnies_Technologies.csv")
    except FileNotFoundError:
        st.error("❌ CSV file not found. Please check file name and location.")
        st.stop()

    df["company_level"] = df["company_level"].str.upper().str.strip()
    return df

df = load_data()

# --------------------------------------------------
# STYLES
# --------------------------------------------------
st.markdown("""
<style>
body { background-color:#020617; }

.card {
    background:#020617;
    border:1px solid #1e293b;
    border-radius:16px;
    padding:18px;
    margin-bottom:18px;
    box-shadow:0 12px 30px rgba(0,0,0,0.35);
}

.title {
    font-size:38px;
    font-weight:800;
    color:#e5e7eb;
}

.subtitle {
    color:#94a3b8;
    font-size:16px;
}

.badge {
    display:inline-block;
    padding:5px 12px;
    border-radius:999px;
    font-size:12px;
    border:1px solid #334155;
    color:#38bdf8;
    margin-top:6px;
}

.company-title {
    font-size:18px;
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
        stream = st.selectbox("🎓 Select Stream", sorted(df["stream"].unique()))
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
# COMPANY SELECTION LOGIC
# --------------------------------------------------
def get_companies_by_cgpa(df, stream, department, role, cgpa):
    base_df = df[
        (df["stream"] == stream) &
        (df["department"] == department)
    ]

    role_df = base_df[base_df["job_role"] == role]

    if cgpa < 6.5:
        result = role_df[role_df["company_level"] == "STARTUP"]

    elif cgpa < 8.5:
        mid = role_df[role_df["company_level"] == "MID"]
        startup = role_df[role_df["company_level"] == "STARTUP"]
        result = pd.concat([mid, startup])

    else:
        high = role_df[role_df["company_level"] == "HIGH"]
        if high.empty:
            high = base_df[base_df["company_level"] == "HIGH"]

        mid = base_df[base_df["company_level"] == "MID"]
        startup = base_df[base_df["company_level"] == "STARTUP"]

        result = pd.concat([high, mid, startup])

    if cgpa < 6.5:
        result = result.head(5)
    elif cgpa < 8.5:
        result = result.head(9)
    else:
        result = result.head(12)

    return result.drop_duplicates("company_name")

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
if submit and role:

    # PROFILE CARD
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

    # RECOMMENDED COMPANIES
    result_df = get_companies_by_cgpa(df, stream, department, role, cgpa)

    st.markdown("## 🏢 Recommended Companies")
    cols = st.columns(3)

    for i, (_, row) in enumerate(result_df.iterrows()):
        with cols[i % 3]:
            techs = row["technologies"] if pd.notna(row["technologies"]) else "Not specified"
            st.markdown(f"""
            <div class="card">
                <div class="company-title">🏢 {row.company_name}</div>
                <span class="badge">{row.company_level}</span>
                <p>💼 <b>Role:</b> {row.job_role}</p>
                <p>📍 <b>Location:</b> {row.company_locations}</p>
                <p>🛠️ <b>Required Technologies:</b><br>{techs}</p>
            </div>
            """, unsafe_allow_html=True)

    # ALTERNATE COMPANIES
    st.markdown("## 🔁 Alternate Companies (Same Department)")

    alt_df = df[
        (df["stream"] == stream) &
        (df["department"] == department) &
        (~df["company_name"].isin(result_df["company_name"]))
    ]

    if alt_df.empty:
        st.info("No alternate companies available.")
    else:
        cols = st.columns(3)
        for i, (_, row) in enumerate(alt_df.iterrows()):
            with cols[i % 3]:
                techs = row["technologies"] if pd.notna(row["technologies"]) else "Not specified"
                st.markdown(f"""
                <div class="card">
                    <div class="company-title">🏢 {row.company_name}</div>
                    <span class="badge">{row.company_level}</span>
                    <p>💼 <b>Role:</b> {row.job_role}</p>
                    <p>📍 <b>Location:</b> {row.company_locations}</p>
                    <p>🛠️ <b>Technologies:</b><br>{techs}</p>
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



