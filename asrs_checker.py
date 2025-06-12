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
        "Current Policies": ["status quo", "emission growth", "physical risks", "fossil fuels"]
    }

    matches = [k for k in keywords[scenario] if k.lower() in text.lower()]
    if matches:
        output.append(f"Disclosure aligns with keywords for {scenario}: {', '.join(matches)}.")
    else:
        output.append(f"No specific alignment found with {scenario} keywords. Disclosure may lack scenario analysis.")

    return output
