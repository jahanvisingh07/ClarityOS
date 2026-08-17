import numpy as np
from typing import Dict, Any
from models import StudentProfile

CAREER_WEIGHT_MATRIX: Dict[str, Dict[str, float]] = {
    "SWE": {"cgpa": 0.15, "projects": 0.35, "internships": 0.20, "risk_appetite": 0.05, "communication": 0.05, "urgency": 0.20},
    "PM": {"cgpa": 0.10, "projects": 0.25, "internships": 0.15, "risk_appetite": 0.15, "communication": 0.30, "urgency": 0.05},
    "Data Science / AI": {"cgpa": 0.25, "projects": 0.30, "internships": 0.15, "risk_appetite": 0.10, "communication": 0.05, "urgency": 0.15},
    "Higher Studies (MS/MEM)": {"cgpa": 0.40, "projects": 0.20, "internships": 0.15, "risk_appetite": 0.10, "communication": 0.10, "urgency": 0.05},
    "Tech Consulting": {"cgpa": 0.20, "projects": 0.15, "internships": 0.15, "risk_appetite": 0.10, "communication": 0.30, "urgency": 0.10}
}

def normalize_profile(profile: StudentProfile) -> Dict[str, float]:
    return {
        "cgpa": min(max(profile.cgpa / 10.0, 0.0), 1.0),
        "projects": min(profile.projects_built / 5.0, 1.0),
        "internships": min(profile.internship_experience / 6.0, 1.0),
        "risk_appetite": profile.risk_appetite / 10.0,
        "communication": profile.communication_preference / 10.0,
        "urgency": profile.timeline_urgency / 10.0,
    }

def calculate_career_fit(profile: StudentProfile) -> Dict[str, Any]:
    norm_scores = normalize_profile(profile)
    ranked_results = []

    for path, weights in CAREER_WEIGHT_MATRIX.items():
        score = sum(norm_scores[factor] * weights[factor] for factor in weights)
        ranked_results.append({
            "path": path,
            "fit_score": round(score * 100, 2),
            "factor_contributions": {factor: round(norm_scores[factor] * weights[factor] * 100, 2) for factor in weights}
        })

    ranked_results.sort(key=lambda x: x["fit_score"], reverse=True)
    top_path = ranked_results[0]
    
    gaps = []
    for factor, weight in CAREER_WEIGHT_MATRIX[top_path["path"]].items():
        if norm_scores[factor] < 0.6 and weight >= 0.15:
            gaps.append({"factor": factor, "current_score": round(norm_scores[factor] * 10, 1), "importance": "High" if weight >= 0.25 else "Medium"})

    return {"top_recommendation": top_path, "ranked_paths": ranked_results, "gap_analysis": gaps}