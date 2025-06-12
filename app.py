import streamlit as st
import fitz
import os
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from datetime import datetime
from asrs_checker import (
    check_asrs_compliance, map_ngfs_scenarios,
    suggest_scenario, assess_value_at_risk,
    generate_qualitative_analysis, compare_scenarios, extract_locations
)

st.set_page_config(page_title="ASRS & AASB S2 Disclosure Screener", layout="wide")
st.title("📄 ASRS & AASB S2 Disclosure Screener (Australia)")

sust_file = st.file_uploader("Upload Sustainability Report (PDF)", type=["pdf"])
fin_file = st.file_uploader("Upload Annual Financial Report (PDF)", type=["pdf"])
industry = st.selectbox("Select Company Industry", [
    "Banking", "Insurance", "Mining", "Energy", "Utilities", "Real Estate", "Retail", "Technology"
])

auto_scenario = suggest_scenario(industry)
scenario1 = st.selectbox("Select First NGFS Scenario", [
    "Below 2°C Orderly", "Divergent Net Zero", "Delayed Transition", "Current Policies", "Hot House World"
], index=0)
scenario2 = st.selectbox("Select Second NGFS Scenario", [
    "Below 2°C Orderly", "Divergent Net Zero", "Delayed Transition", "Current Policies", "Hot House World"
], index=4)

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

    score, gaps, summary, disclosure_table = check_asrs_compliance(sust_text)
    qual_notes = generate_qualitative_analysis(disclosure_table, scenario1)

    st.header("✅ AASB S2 Disclosure Table")
    st.dataframe(disclosure_table)
    st.metric("Compliance Score", f"{score}%")

    st.subheader("📌 Disclosure Gaps")
    for gap in gaps:
        st.warning(gap)

    st.subheader("📝 Recommendations")
    for line in summary:
        st.info(line)

    st.subheader("🌡️ Scenario Comparison")
    result1, result2 = compare_scenarios(sust_text, scenario1, scenario2)
    st.write(f"**{scenario1}:** {result1}")
    st.write(f"**{scenario2}:** {result2}")

    st.subheader("💰 Physical vs Transition Risk")
    risk_data = assess_value_at_risk(fin_text, scenario1)
    fig, ax = plt.subplots()
    ax.bar(["Transition Risk", "Physical Risk"], [risk_data["Transition %"], risk_data["Physical %"]])
    ax.set_ylabel("Risk Percentage (of Revenue)")
    st.pyplot(fig)

    st.subheader("📍 Physical Risk by Office Location")
    locations = extract_locations(sust_text + fin_text)
    for loc in locations:
        st.warning(loc)

    os.remove("sustainability.pdf")
    os.remove("financials.pdf")
else:
    st.warning("Please upload both Sustainability and Financial reports to proceed.")
