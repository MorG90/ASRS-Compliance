import streamlit as st
import fitz
import os
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from datetime import datetime
from asrs_checker import (
    check_asrs_compliance, map_ngfs_scenarios,
    suggest_scenario, assess_value_at_risk,
    aasb_s2_disclosure_table, generate_qualitative_analysis
)

st.set_page_config(page_title="ASRS & AASB S2 Disclosure Screener", layout="wide")

st.title("📄 ASRS & AASB S2 Disclosure Screener (Australia)")

sust_file = st.file_uploader("Upload Sustainability Report (PDF)", type=["pdf"])
fin_file = st.file_uploader("Upload Annual Financial Report (PDF)", type=["pdf"])
industry = st.selectbox("Select Company Industry", [
    "Banking", "Insurance", "Mining", "Energy", "Utilities", "Real Estate", "Retail", "Technology"
])

auto_scenario = suggest_scenario(industry)
scenario_choice = st.selectbox(
    "Select or Override NGFS Scenario for Analysis",
    ["Below 2°C Orderly", "Divergent Net Zero", "Delayed Transition", "Current Policies", "Hot House World"],
    index=["Below 2°C Orderly", "Divergent Net Zero", "Delayed Transition", "Current Policies", "Hot House World"].index(auto_scenario)
)

st.markdown("""
### 🌍 NGFS Scenario Descriptions
- **Below 2°C Orderly**: Immediate strong action, minimal disruption.
- **Divergent Net Zero**: Rapid transition, delayed globally, costly.
- **Delayed Transition**: Late, abrupt action increases transition risk.
- **Current Policies**: No additional climate policy—high physical risk.
- **Hot House World**: No mitigation—extreme warming & catastrophic physical risk.
""")

if sust_file and fin_file:
    st.success("Both reports uploaded. Processing...")
    with open("sustainability.pdf", "wb") as f:
        f.write(sust_file.read())
    with open("financials.pdf", "wb") as f:
        f.write(fin_file.read())

    def extract_text(path):
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    sust_text = extract_text("sustainability.pdf")
    fin_text = extract_text("financials.pdf")

    score, gaps, summary = check_asrs_compliance(sust_text)
    ngfs_result = map_ngfs_scenarios(sust_text, scenario_choice)
    risk_metrics = assess_value_at_risk(fin_text, scenario_choice)
    table_data = aasb_s2_disclosure_table(sust_text)
    qualitative_notes = generate_qualitative_analysis(table_data, scenario_choice)

    st.header("✅ AASB S2 Disclosure Table & Score")
    st.dataframe(table_data)
    st.metric("Compliance Score", f"{score}%")

    st.subheader("📌 Gaps & Recommendations")
    for gap in gaps:
        st.warning(gap)
    for line in summary:
        st.info(line)

    st.subheader("🌡️ NGFS Scenario Mapping")
    for line in ngfs_result:
        st.success(line)

    st.subheader("📊 Estimated Financial Risk Exposure")
    st.write(risk_metrics)

    st.subheader("🧠 Qualitative Scenario Analysis Commentary")
    for line in qualitative_notes:
        st.markdown(f"- {line}")

    st.subheader("📥 Export Report")
    if st.button("Generate PDF Report"):
        filename = "asrs_full_report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"
        pdf_path = os.path.join(".", filename)
        c = canvas.Canvas(pdf_path)
        width, height = 595, 842
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, "ASRS/AASB S2 Full Disclosure Report")
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
        c.drawString(50, y, "Qualitative Scenario Commentary:")
        y -= 20
        c.setFont("Helvetica", 11)
        for line in qualitative_notes:
            if y < 80:
                c.showPage()
                y = height - 50
            c.drawString(60, y, f"- {line}")
            y -= 20

        c.save()
        with open(pdf_path, "rb") as f:
            st.download_button("📤 Download Report", f, file_name=filename, mime="application/pdf")
        os.remove(pdf_path)

    os.remove("sustainability.pdf")
    os.remove("financials.pdf")
else:
    st.warning("Please upload both Sustainability and Financial reports to proceed.")
