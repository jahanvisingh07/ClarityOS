import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizPayload(BaseModel):
    stream: str
    answers: Dict[Any, Any]

@app.post("/analyze-quiz")
async def analyze_quiz(payload: QuizPayload):
    stream = payload.stream
    raw_answers = payload.answers
    
    ans = {}
    for k, v in raw_answers.items():
        try:
            if str(v).strip():
                ans[int(k)] = str(v).lower()
        except:
            continue

    if not ans:
        empty_defaults = {
            "Science (PCB)": ["Medicine (MBBS/BDS)", "Veterinary Science", "Biotechnology & Genetics Research", "Pharmacy & Pharmaceutical Sciences", "Allied Health Professions (Physio/Nutrition)", "Public Health & Healthcare Management", "Microbiology & Immunology"],
            "Science (PCM)": ["Software Engineering & Computer Science", "Data Science & Artificial Intelligence", "Mechanical & Aerospace Engineering", "Electronics, VLSI & Robotics", "Architecture & Design", "Civil & Infrastructure Engineering", "Pure Mathematics & Quantitative Research"],
            "Commerce": ["Chartered Accountancy (CA) & Corporate Finance", "Investment Banking & Equity Research", "Corporate Law & Legal Consulting", "Marketing, Advertising & Brand Management", "Entrepreneurship & Business Strategy", "Actuarial Science & Risk Management", "Human Resources & Organizational Behavior"],
            "Arts / Humanities": ["Psychology & Counseling", "Journalism, Media & Mass Communication", "Political Science & International Relations", "Literature, Writing & Editorial", "Fine Arts, Design & Animation", "Sociology & Social Work", "History, Archaeology & Anthropology"],
            "College - Medicine & Life Sciences": ["Clinical Practice (Medicine/Surgery/Dentistry)", "Biotechnology & Genomic Research", "Allied Health & Rehabilitation", "Pharmacology & Drug Development", "Public Health & Epidemiology"],
            "College - Computer Science & IT": ["Full-Stack / Core Software Engineering", "Data Science & Artificial Intelligence", "Cybersecurity & Ethical Hacking", "Cloud Architecture & DevOps", "Game Development & Interactive Media", "Product Management & UI/UX Design", "Advanced Academic Research & Higher Studies (MS / Ph.D.)"],
            "College - Core Engineering & Physical Sciences": ["Mechanical & Aerospace Engineering", "Civil & Sustainable Infrastructure", "Electronics, VLSI & IoT", "Chemical & Materials Engineering", "Advanced Academic Research & Higher Studies (MS / Ph.D.)"],
            "College - Business, Finance & Commerce": ["Investment Banking & Corporate Finance", "Growth Marketing & Brand Strategy", "Operations & Supply Chain Management", "Entrepreneurship & Venture Capital", "Advanced Academic Research & Higher Studies (MBA / Ph.D.)"],
            "College - Arts, Humanities & Social Sciences": ["Psychology & Behavioral Science", "Journalism & Mass Media", "Sociology & Social Work", "Literature, History & Editorial", "Advanced Academic Research & Higher Studies (MS / Ph.D.)"],
            "College - Law, Policy & International Relations": ["Corporate & Commercial Law", "Criminal & Litigation Law", "Public Policy & Governance", "International Relations & Diplomacy", "Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"],
            "College - Creative Arts, Architecture & Design": ["Architecture & Spatial Design", "Fine Arts & Illustration", "Animation & Game Design", "Industrial & Product Design", "Advanced Academic Research & Higher Studies (MFA / Ph.D.)"]
        }
        
        vectors = empty_defaults.get(stream, ["No Selection"])
        sorted_matches = [{"title": v, "match": 0.0} for v in vectors]
        return {
            "status": "success",
            "stream": stream,
            "optimal_vector": sorted_matches[0],
            "evaluated_vectors": sorted_matches,
            "explanation": "No answers provided."
        }

    scores = {}

    if stream == "Science (PCB)":
        scores = { "Medicine (MBBS/BDS)": 5.0, "Veterinary Science": 5.0, "Biotechnology & Genetics Research": 5.0, "Pharmacy & Pharmaceutical Sciences": 5.0, "Allied Health Professions (Physio/Nutrition)": 5.0, "Public Health & Healthcare Management": 5.0, "Microbiology & Immunology": 5.0 }
        if "chemistry" in ans.get(1, ""): scores["Pharmacy & Pharmaceutical Sciences"] += 10.0
        q2 = ans.get(2, "")
        if "human body" in q2: scores["Medicine (MBBS/BDS)"] += 15.0; scores["Allied Health Professions (Physio/Nutrition)"] += 10.0
        elif "animal" in q2: scores["Veterinary Science"] += 25.0
        elif "genetics" in q2: scores["Biotechnology & Genetics Research"] += 20.0
        elif "micro" in q2: scores["Microbiology & Immunology"] += 20.0
        q3 = ans.get(3, "")
        if "diagnosing" in q3: scores["Medicine (MBBS/BDS)"] += 20.0
        elif "new medicine" in q3: scores["Pharmacy & Pharmaceutical Sciences"] += 20.0; scores["Biotechnology & Genetics Research"] += 15.0
        elif "cellular" in q3: scores["Biotechnology & Genetics Research"] += 15.0; scores["Microbiology & Immunology"] += 15.0
        elif "environment" in q3: scores["Public Health & Healthcare Management"] += 15.0
        elif "research" in q3: scores["Biotechnology & Genetics Research"] += 20.0

    elif stream == "Science (PCM)":
        scores = { "Software Engineering & Computer Science": 5.0, "Data Science & Artificial Intelligence": 5.0, "Mechanical & Aerospace Engineering": 5.0, "Electronics, VLSI & Robotics": 5.0, "Architecture & Design": 5.0, "Civil & Infrastructure Engineering": 5.0, "Pure Mathematics & Quantitative Research": 5.0 }
        q1 = ans.get(1, "")
        if "computer science" in q1: scores["Software Engineering & Computer Science"] += 20.0; scores["Data Science & Artificial Intelligence"] += 15.0
        elif "mathematics" in q1: scores["Pure Mathematics & Quantitative Research"] += 25.0; scores["Data Science & Artificial Intelligence"] += 15.0
        elif "physics" in q1: scores["Mechanical & Aerospace Engineering"] += 20.0; scores["Civil & Infrastructure Engineering"] += 15.0

    else:
        scores = { "General Professional Vector": 10.0 }

    sorted_matches = sorted(
        [{"title": k, "match": round(max(0.0, min(v, 98.5)), 1)} for k, v in scores.items()],
        key=lambda x: x["match"],
        reverse=True
    )

    top_careers = [f"{match['title']} ({match['match']}%)" for match in sorted_matches[:3]]
    prompt = f"A user completed a career assessment. Top 3 matches: {', '.join(top_careers)}. Write a short, encouraging 2-paragraph explanation of why these careers fit well together based on shared skills. Keep it conversational and address the user as 'you'."

    try:
        explanation = model.generate_content(prompt).text
    except Exception as e:
        explanation = f"You show a strong aptitude for these fields based on your profile analysis. (Error: {str(e)})"

    return {
        "status": "success",
        "stream": stream,
        "optimal_vector": sorted_matches[0],
        "evaluated_vectors": sorted_matches,
        "explanation": explanation
    }