import streamlit as st
import pandas as pd

# Page config (Professional look)
st.set_page_config(
    page_title="Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# Load CSV (DO NOT MODIFY)
df = pd.read_csv("Master_Comapnies_Technologies.csv")

st.title("🎓 Career Recommendation System")
st.write("Fill the form below to get company recommendations based on your profile.")

st.divider()

# ---------------- FORM SECTION ----------------
with st.form("career_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        stream = st.selectbox(
            "Stream",
            options=["Select Stream", "Engineering"]
        )

    with col2:
        departments = sorted(df["eligible_departments"].dropna().unique())
        department = st.selectbox(
            "Department",
            options=["Select Department"] + departments
        )

    with col3:
        if department != "Select Department":
            roles = sorted(
                df[df["eligible_departments"] == department]["job_role"].dropna().unique()
            )
        else:
            roles = []

        role = st.selectbox(
            "Interested Role",
            options=["Select Role"] + roles
        )

    submit = st.form_submit_button("Find Companies")

# ---------------- RESULT SECTION ----------------
if submit:
    if department == "Select Department" or role == "Select Role":
        st.warning("⚠️ Please select Department and Role")
    else:
        result_df = df[
            (df["eligible_departments"] == department) &
            (df["job_role"] == role)
        ].copy()

        if result_df.empty:
            st.info("No companies found for your selection.")
        else:
            # Handle missing technologies
            result_df["technologies"] = result_df["technologies"].fillna("Not specified")

            st.subheader("📊 Recommended Companies")

            st.dataframe(
                result_df[[
                    "company_name",
                    "job_role",
                    "package_lpa",
                    "company_locations",
                    "technologies"
                ]],
                use_container_width=True
            )
