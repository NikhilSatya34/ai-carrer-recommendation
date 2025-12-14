import pandas as pd

# Load your existing CSV
df = pd.read_csv("Career_Master_Companies.csv")

# ROLE → TECHNOLOGIES MAP
ROLE_TECH_MAP = {
    "AI Engineer": "Python,Machine Learning,Deep Learning,TensorFlow,PyTorch",
    "ML Engineer": "Python,Scikit-learn,TensorFlow,Model Deployment",
    "Data Scientist": "Python,Statistics,Pandas,Machine Learning,SQL",
    "Data Analyst": "Python,SQL,Excel,Power BI,Tableau",
    "Software Engineer": "DSA,OOPS,Python,Java,Git",
    "Backend Developer": "Python,Java,APIs,Databases,Microservices",
    "Frontend Developer": "HTML,CSS,JavaScript,React",
    "Full Stack Developer": "HTML,CSS,JavaScript,Python,SQL",
    "Software Architect": "System Design,Microservices,Cloud Architecture,AWS,Java",

    "Embedded Engineer": "C,Embedded Systems,RTOS,Microcontrollers",
    "VLSI Engineer": "Verilog,VHDL,FPGA,ASIC Design",
    "Electrical Engineer": "Power Systems,PLC,SCADA,MATLAB",
    "Site Engineer": "AutoCAD,Construction Planning,Surveying",
    "Structural Engineer": "AutoCAD,ETABS,STAAD Pro",
    "Design Engineer": "SolidWorks,CATIA,ANSYS",

    "Junior Doctor": "Clinical Diagnosis,Patient Care,Medical Ethics",
    "Medical Officer": "Healthcare Management,Clinical Practice",
    "ICU Nurse": "Critical Care,Ventilator Handling,Patient Monitoring",
    "Staff Nurse": "Patient Care,Medication Administration",
    "Physiotherapist": "Rehabilitation,Therapy,Exercise Planning",

    "Pharmacist": "Pharmacology,Dispensing,Drug Safety",
    "Medical Representative": "Product Knowledge,Sales,Communication",
    "Clinical Research Associate": "Clinical Trials,Data Management",

    "Accountant": "Accounting,Tally,Taxation,Excel",
    "Audit Assistant": "Auditing,Compliance,Excel",
    "Business Analyst": "Business Analysis,SQL,Power BI",
    "Product Manager": "Product Strategy,Agile,Market Research",
    "System Analyst": "System Design,Requirement Analysis"
}

# Fill missing technologies
def add_technologies(row):
    if pd.isna(row["technologies"]) or row["technologies"] == "":
        return ROLE_TECH_MAP.get(row["job_role"], "Not specified")
    return row["technologies"]

df["technologies"] = df.apply(add_technologies, axis=1)

# Save new CSV
df.to_csv("Career_Master_Companies_FINAL.csv", index=False)

print("✅ Technologies added successfully!")
