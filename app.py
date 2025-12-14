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

# ---------------- VALIDATE CSV ----------------
required_cols = ["stream", "department", "job_role",
                 "company_name", "company_level", "company_locations"]

for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing column in CSV: {col}")
        st.stop()

# ---------------- SESSION STATE ----------------
for key in ["stream", "department", "role",
            "show_dept", "show_role"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ---------------- STYLES ----------------
st.markdown("""
<style>
.card {
    background:#020617;
    border:1px solid #1e293b;
    border-radius:16px;
    padding:20px;
    margin-bottom:16px;
}
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
  <h1>🎓 AI Career Recommendation System</h1>
  <p>Stream → Department → Role (Button Controlled)</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FORM ----------------
with st.form("career_form"):

    st.markdown("### 👤 Student Profile")

    # -------- STREAM --------
    stream = st.selectbox(
        "🎓 Select Stream",
        sorted(df["stream"].unique())
    )

    load_dept = st.form_submit_button("➡️ Load Departments")

    if load_dept:
        st.session_state.stream = stream
        st.session_state.show_dept = True
        st.session_state.show_role = False

    # -------- DEPARTMENT --------
    if st.session_state.show_dept:

        dept_list = sorted(
            df[df["stream"] == st.session_state.stream]["department"].unique()
        )

        department = st.selectbox("🏫 Select Department", dept_list)

        load_role = st.form_submit_button("➡️ Load Roles")

        if load_role:
            st.session_state.department = department
            st.session_state.show_role = True

    # -------- ROLE --------
    if st.session_state.show_role:

        role_list = sorted(
            df[
                (df["stream"] == st.session_state.stream) &
                (df["department"] == st.session_state.department)
            ]["job_role"].unique()
        )

        role = st.selectbox("💼 Select Interested Role", role_list)

        cgpa = st.slider("📊 CGPA / Score", 5.0, 10.0, 7.0, 0.1)
        internship = st.selectbox("🧑‍💻 Internship Experience", ["Yes", "No"])

        final_submit = st.form_submit_button("🚀 Get Career Recommendations")

    else:
        final_submit = False

# ---------------- RESULTS ----------------
if final_submit:

    st.markdown("## 👤 Student Profile")
    st.write({
        "Stream": st.session_state.stream,
        "Department": st.session_state.department,
        "Role": role,
        "CGPA": cgpa,
        "Internship": internship
    })

    result_df = df[
        (df["stream"] == st.session_state.stream) &
        (df["department"] == st.session_state.department) &
        (df["job_role"] == role)
    ].head(9)

    if result_df.empty:
        st.warning("No exact matches found.")
    else:
        st.markdown("## 🏢 Recommended Companies")
        cols = st.columns(3)
        for i, (_, row) in enumerate(result_df.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="card">
                    <h3>{row.company_name}</h3>
                    <span class="badge">{row.company_level}</span>
                    <p><b>Role:</b> {row.job_role}</p>
                    <p><b>Locations:</b> {row.company_locations}</p>
                </div>
                """, unsafe_allow_html=True)
