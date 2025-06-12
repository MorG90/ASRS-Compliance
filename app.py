import streamlit as st
import fitz
import os
import matplotlib.pyplot as plt
from asrs_checker import check_asrs_compliance, map_ngfs_scenarios, suggest_scenario

st.set_page_config(page_title="ASRS & AASB S2 Disclosure Screener", layout="wide")

st.title("📄 ASRS & AASB S2 Disclosure Screener (Australia)")

uploaded_file = st.file_uploader("Upload Sustainability or Annual Report (PDF)", type=["pdf"])
industry = st.selectbox("Select Company Industry", [
    "Banking", "Insurance", "Mining", "Energy", "Utilities", "Real Estate", "Retail", "Technology"
])

auto_scenario = suggest_scenario(industry)
scenario_choice = st.selectbox(
    "Select or Override NGFS Scenario for Analysis",
    ["Below 2°C Orderly", "Divergent Net Zero", "Delayed Transition", "Current Policies"],
    index=["Below 2°C Orderly", "Divergent Net Zero", "Delayed Transition", "Current Policies"].index(auto_scenario)
)

if uploaded_file:
    st.success("File uploaded. Processing...")
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    text = ""
    with fitz.open("temp.pdf") as doc:
        for page in doc:
            text += page.get_text()

    score, gaps, summary = check_asrs_compliance(text)
    ngfs_result = map_ngfs_scenarios(text, scenario_choice)

    st.header("✅ Compliance Summary")
    st.metric("ASRS/AASB Compliance Score", f"{score}%")

    st.subheader("📌 Disclosure Gaps")
    for gap in gaps:
        st.warning(gap)

    st.subheader("📝 Recommendations")
    for line in summary:
        st.info(line)

    st.subheader("🌡️ NGFS Scenario Mapping")
    st.write(f"**Scenario Selected:** {scenario_choice}")
    for line in ngfs_result:
        st.success(line)

    st.subheader("📊 Risk Visualization")
    risk_data = {"Transition Risk": 100 - score, "Physical Risk": score}
    fig, ax = plt.subplots()
    ax.bar(risk_data.keys(), risk_data.values())
    ax.set_ylabel("Estimated Risk Proportion (%)")
    st.pyplot(fig)

        from reportlab.pdfgen import canvas
    from datetime import datetime

    st.subheader("📥 Export Report as PDF")
    if st.button("Generate PDF Report"):
        filename = "asrs_report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"
        pdf_path = os.path.join(".", filename)
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, "ASRS & AASB S2 Disclosure Screener Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Industry: {industry}")
        c.drawString(50, height - 100, f"Scenario: {scenario_choice}")
        c.drawString(50, height - 120, f"Compliance Score: {score}%")

        y = height - 160
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Disclosure Gaps:")
        y -= 20
        c.setFont("Helvetica", 11)
        for gap in gaps:
            if y < 100:
                c.showPage()
                y = height - 50
            c.drawString(60, y, f"- {gap}")
            y -= 20

        c.setFont("Helvetica-Bold", 12)
        if y < 120:
            c.showPage()
            y = height - 50
        c.drawString(50, y, "Recommendations:")
        y -= 20
        c.setFont("Helvetica", 11)
        for line in summary:
            if y < 100:
                c.showPage()
                y = height - 50
            c.drawString(60, y, f"- {line}")
            y -= 20

        c.setFont("Helvetica-Bold", 12)
        if y < 100:
            c.showPage()
            y = height - 50
        c.drawString(50, y, "Scenario Mapping:")
        y -= 20
        c.setFont("Helvetica", 11)
        for line in ngfs_result:
            if y < 80:
                c.showPage()
                y = height - 50
            c.drawString(60, y, f"- {line}")
            y -= 20

        c.save()
        with open(pdf_path, "rb") as f:
            st.download_button("📤 Download Report", f, file_name=filename, mime="application/pdf")
        os.remove(pdf_path)
    os.remove("temp.pdf")
