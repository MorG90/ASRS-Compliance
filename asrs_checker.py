import pandas as pd
import re

def check_asrs_compliance(text):
    sections = {
        "Governance": ["board oversight", "management's role"],
        "Strategy": ["climate-related risks", "resilience"],
        "Risk Management": ["risk identification", "processes"],
        "Metrics & Targets": ["emissions", "targets", "KPIs"],
        "Scope 1–3 Emissions": ["scope 1", "scope 2", "scope 3"],
        "Scenario Analysis": ["scenario analysis", "ngfs", "climate scenarios"]
    }

    total_score = 0
    gaps = []
    summary = []
    data = []

    for section, keywords in sections.items():
        found = any(k.lower() in text.lower() for k in keywords)
        data.append({
            "Category": section,
            "Disclosed": "Yes" if found else "No",
            "Score": 1 if found else 0
        })
        if found:
            total_score += 1
        else:
            gaps.append(f"{section} disclosure missing or incomplete.")
            summary.append(f"Include detailed {section.lower()} information to align with AASB S2 and AUASB assurance standards.")

    df = pd.DataFrame(data)
    score_percent = round((total_score / len(sections)) * 100, 2)
    return score_percent, gaps, summary, df

def map_ngfs_scenarios(text, scenario):
    keywords = {
        "Below 2°C Orderly": ["carbon pricing", "net zero", "renewables", "transition risk"],
        "Divergent Net Zero": ["regulatory fragmentation", "carbon tax", "disorderly"],
        "Delayed Transition": ["technology shift", "late policy", "transition shock"],
        "Current Policies": ["status quo", "emission growth", "physical risks", "fossil fuels"],
        "Hot House World": ["3 degrees", "4 degrees", "severe flooding", "climate catastrophe"]
    }

    matches = [k for k in keywords[scenario] if k.lower() in text.lower()]
    if matches:
        return f"Disclosure aligns with keywords for {scenario}: {', '.join(matches)}."
    else:
        return f"No specific alignment found with {scenario} keywords."

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
    # Extract dummy revenue figure from text for risk calculation
    match = re.search(r"\$([0-9,]+)\s*million", fin_text.replace(",", ""))
    revenue = int(match.group(1)) * 1_000_000 if match else 1_000_000

    scenario_factor = {
        "Below 2°C Orderly": (0.02, 0.03),
        "Divergent Net Zero": (0.05, 0.06),
        "Delayed Transition": (0.08, 0.10),
        "Current Policies": (0.12, 0.20),
        "Hot House World": (0.15, 0.30)
    }

    transition_risk, physical_risk = scenario_factor[scenario]
    return {
        "Revenue (Estimated)": f"${revenue:,.0f}",
        "Transition Risk ($)": f"${revenue * transition_risk:,.0f}",
        "Physical Risk ($)": f"${revenue * physical_risk:,.0f}",
        "Transition %": transition_risk,
        "Physical %": physical_risk
    }

def compare_scenarios(text, scenario1, scenario2):
    return map_ngfs_scenarios(text, scenario1), map_ngfs_scenarios(text, scenario2)

def generate_qualitative_analysis(disclosure_df, scenario):
    insights = []
    for _, row in disclosure_df.iterrows():
        if row["Disclosed"] == "No":
            insights.append(f"{row['Category']} is absent, which raises uncertainty in a '{scenario}' scenario.")
        else:
            insights.append(f"{row['Category']} is addressed, supporting alignment under '{scenario}'.")
    return insights

def extract_locations(text):
    # Look for potential office city mentions in AU and abroad
    cities = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Auckland", "London", "Singapore", "New York", "Tokyo"]
    found = [city for city in cities if city.lower() in text.lower()]
    risks = [f"{city}: High physical climate risk (heat/flood/fire)." for city in found]
    return risks
