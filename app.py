import streamlit as st
import fitz  # PyMuPDF
import os
from asrs_checker import check_asrs_compliance, map_ngfs_scenarios

st.set_page_config(page_title="ASRS & AASB S2 Disclosure Screener", layout="wide")

st.title("📄 ASRS & AASB S2 Disclosure Screener (Australia)")

uploaded_file = st.file_uploader("Upload Sustainability or Annual Report (PDF)", type=["pdf"])

scenario_choice = st.selectbox(
    "Select NGFS Scenario for Analysis",
    ["Below 2°C Orderly", "Divergent Net Zero", "Delayed Transition", "Current Policies"]
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

    os.remove("temp.pdf")
