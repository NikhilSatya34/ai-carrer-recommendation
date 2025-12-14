import streamlit as st
import pandas as pd

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# -------------------- LOAD DATA --------------------
df = pd.read_csv("Career_Master_Companies.csv")

# -------------------- GLOBAL STYLES --------------------
st.markdown("""
<style>
body {
    background-color: #020617;
}
.card {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.title {
    font-size: 42px;
    font-weight: 800;
    color: #e5e7eb;
}
.subtitle {
    color: #94a3b8;
    font-size: 18px;
}
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
    Stream • Department • Role • Company Insights
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------- FORM INPUTS --------------------
with st.form("career_form"):

    st.markdown("### 👤 Student Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        stream = st.selectbox(
            "🎓 Stream",
            sorted(df["stream"].unique())
        )

    with col2:
        department = st.selectbox(
            "🏫 Department",
            sorted(df[df["stream"] == stream]["department"].unique())
        )

    with col3:
        role = st.selectbox(
            "💼 Interested Role",
            sorted(
                df[
                    (df["stream"] == stream) &
                    (df["department"] == department)
                ]["job_role"].unique()
            )
        )

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
        <p><b>Role:</b> {role}</p>
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
        st.warning("⚠️ No exact matches found. Showing related companies.")
        result_df = df[df["stream"] == stream].head(6)
    else:
        result_df = result_df.head(9)

    # -------- COMPANY RESULTS --------
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
Built with ❤️ using Data Science & Streamlit
</p>
""", unsafe_allow_html=True)
