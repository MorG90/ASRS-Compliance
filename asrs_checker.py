import pandas as pd

def check_asrs_compliance(text):
    sections = {
        "Governance": ["board oversight", "management's role"],
        "Strategy": ["climate-related risks", "resilience"],
        "Risk Management": ["risk identification", "processes"],
        "Metrics & Targets": ["emissions", "scope 1", "scope 2", "scope 3", "targets"]
    }

    score = 0
    gaps = []
    summary = []
    total_sections = len(sections)

    for section, keywords in sections.items():
        found = any(k.lower() in text.lower() for k in keywords)
        if found:
            score += 100 / total_sections
        else:
            gaps.append(f"{section} disclosure missing or incomplete.")
            summary.append(f"Include detailed {section.lower()} information to align with ASRS/AASB S2.")

    return round(score, 2), gaps, summary

def map_ngfs_scenarios(text, scenario):
    output = []
    keywords = {
        "Below 2°C Orderly": ["carbon pricing", "net zero", "renewables", "transition risk"],
        "Divergent Net Zero": ["regulatory fragmentation", "carbon tax", "disorderly"],
        "Delayed Transition": ["technology shift", "late policy", "transition shock"],
        "Current Policies": ["status quo", "emission growth", "physical risks", "fossil fuels"],
        "Hot House World": ["3 degrees", "4 degrees", "severe flooding", "climate catastrophe"]
    }

    matches = [k for k in keywords[scenario] if k.lower() in text.lower()]
    if matches:
        output.append(f"Disclosure aligns with keywords for {scenario}: {', '.join(matches)}.")
    else:
        output.append(f"No specific alignment found with {scenario} keywords.")

    return output

def suggest_scenario(industry):
    mapping = {
        "Banking": "Below 2°C Orderly",
        "Insurance": "Current Policies",
        "Mining": "Delayed Transition",
        "Energy": "Divergent Net Zero",
        "Utilities": "Below 2°C Orderly",
        "Real Estate": "Current Policies",
        "Retail": "Hot House World",
        "Technology": "Below 2°C Orderly"
    }
    return mapping.get(industry, "Below 2°C Orderly")

def assess_value_at_risk(fin_text, scenario):
    exposure_base = 1000000  # placeholder exposure value in AUD
    scenario_factor = {
        "Below 2°C Orderly": 0.02,
        "Divergent Net Zero": 0.05,
        "Delayed Transition": 0.08,
        "Current Policies": 0.15,
        "Hot House World": 0.25
    }
    var = exposure_base * scenario_factor[scenario]
    return {
        "Estimated Value-at-Risk (AUD)": f"${var:,.2f}",
        "Assumed Exposure (Placeholder)": f"${exposure_base:,.2f}",
        "Scenario Risk Multiplier": scenario_factor[scenario]
    }

def aasb_s2_disclosure_table(text):
    aasb_categories = {
        "Governance": ["board", "responsibility", "oversight"],
        "Strategy": ["scenario", "transition", "resilience"],
        "Risk Management": ["identify", "assess", "manage"],
        "Metrics": ["scope 1", "scope 2", "scope 3", "target", "KPI"]
    }
    data = []
    for cat, keys in aasb_categories.items():
        presence = any(k.lower() in text.lower() for k in keys)
        data.append({"Category": cat, "Disclosed": "Yes" if presence else "No"})

    return pd.DataFrame(data)

def generate_qualitative_analysis(disclosure_df, scenario):
    insights = []
    for _, row in disclosure_df.iterrows():
        if row["Disclosed"] == "No":
            insights.append(f"{row['Category']} disclosure is absent, which may increase uncertainty under the '{scenario}' scenario.")
        else:
            insights.append(f"{row['Category']} is covered, which improves transparency under the '{scenario}' scenario.")
    return insights
