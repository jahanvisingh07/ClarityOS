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
        q4 = ans.get(4, "")
        if "love it" in q4: scores["Medicine (MBBS/BDS)"] += 15.0; scores["Allied Health Professions (Physio/Nutrition)"] += 15.0
        elif "limited" in q4 or "do not want" in q4: scores["Medicine (MBBS/BDS)"] -= 20.0; scores["Biotechnology & Genetics Research"] += 20.0; scores["Microbiology & Immunology"] += 15.0; scores["Pharmacy & Pharmaceutical Sciences"] += 15.0
        q5 = ans.get(5, "")
        if "completely comfortable" in q5: scores["Medicine (MBBS/BDS)"] += 15.0; scores["Veterinary Science"] += 15.0
        elif "uncomfortable" in q5: scores["Medicine (MBBS/BDS)"] -= 25.0; scores["Veterinary Science"] -= 20.0; scores["Pharmacy & Pharmaceutical Sciences"] += 15.0; scores["Public Health & Healthcare Management"] += 15.0
        q6 = ans.get(6, "")
        if "one patient" in q6: scores["Medicine (MBBS/BDS)"] += 15.0; scores["Allied Health Professions (Physio/Nutrition)"] += 15.0
        elif "thousands" in q6: scores["Pharmacy & Pharmaceutical Sciences"] += 15.0; scores["Public Health & Healthcare Management"] += 15.0
        elif "scientific knowledge" in q6: scores["Biotechnology & Genetics Research"] += 20.0
        elif "communities" in q6: scores["Public Health & Healthcare Management"] += 25.0
        q8 = ans.get(8, "")
        if "hospital" in q8: scores["Medicine (MBBS/BDS)"] += 15.0
        elif "laboratory" in q8: scores["Biotechnology & Genetics Research"] += 20.0; scores["Microbiology & Immunology"] += 20.0
        elif "field" in q8: scores["Veterinary Science"] += 15.0; scores["Public Health & Healthcare Management"] += 15.0
        q9 = ans.get(9, "")
        if "love it" in q9: scores["Pharmacy & Pharmaceutical Sciences"] += 20.0
        elif "dislike" in q9 or "struggle" in q9: scores["Pharmacy & Pharmaceutical Sciences"] -= 20.0
        q11 = ans.get(11, "")
        if "dislike" in q11: scores["Medicine (MBBS/BDS)"] -= 15.0
        q13 = ans.get(13, "")
        if "extremely" in q13: scores["Biotechnology & Genetics Research"] += 25.0; scores["Microbiology & Immunology"] += 20.0
        elif "not interested" in q13: scores["Biotechnology & Genetics Research"] -= 20.0
        q14 = ans.get(14, "")
        if "animal" in q14: scores["Veterinary Science"] += 30.0
        elif "researcher" in q14: scores["Biotechnology & Genetics Research"] += 20.0
        q16 = ans.get(16, "")
        if "work-life balance" in q16: scores["Medicine (MBBS/BDS)"] -= 15.0; scores["Public Health & Healthcare Management"] += 15.0
        if "prestige" in q16: scores["Medicine (MBBS/BDS)"] += 10.0
        if "scientific discovery" in q16: scores["Biotechnology & Genetics Research"] += 15.0
        q17 = ans.get(17, "")
        if "dislike" in q17: scores["Medicine (MBBS/BDS)"] -= 20.0; scores["Pharmacy & Pharmaceutical Sciences"] += 15.0
        q18 = ans.get(18, "")
        if "shorter path" in q18: scores["Medicine (MBBS/BDS)"] -= 25.0; scores["Allied Health Professions (Physio/Nutrition)"] += 25.0
        elif "absolutely" in q18: scores["Medicine (MBBS/BDS)"] += 15.0; scores["Biotechnology & Genetics Research"] += 15.0
        q19 = ans.get(19, "")
        if "doctor" in q19: scores["Medicine (MBBS/BDS)"] += 30.0
        elif "research" in q19: scores["Biotechnology & Genetics Research"] += 25.0
        elif "pharmaceutic" in q19: scores["Pharmacy & Pharmaceutical Sciences"] += 25.0
        elif "animal" in q19: scores["Veterinary Science"] += 25.0
        q20 = ans.get(20, "")
        if "veterinarian" in q20: scores["Veterinary Science"] += 25.0
        elif "pharmacist" in q20: scores["Pharmacy & Pharmaceutical Sciences"] += 25.0
        elif "biotechnology" in q20: scores["Biotechnology & Genetics Research"] += 25.0
        elif "physiotherapist" in q20 or "nutrition" in q20: scores["Allied Health Professions (Physio/Nutrition)"] += 25.0
        elif "public health" in q20: scores["Public Health & Healthcare Management"] += 25.0

    elif stream == "Science (PCM)":
        scores = { "Software Engineering & Computer Science": 5.0, "Data Science & Artificial Intelligence": 5.0, "Mechanical & Aerospace Engineering": 5.0, "Electronics, VLSI & Robotics": 5.0, "Architecture & Design": 5.0, "Civil & Infrastructure Engineering": 5.0, "Pure Mathematics & Quantitative Research": 5.0 }
        q1 = ans.get(1, "")
        if "computer science" in q1: scores["Software Engineering & Computer Science"] += 20.0; scores["Data Science & Artificial Intelligence"] += 15.0
        elif "mathematics" in q1: scores["Pure Mathematics & Quantitative Research"] += 25.0; scores["Data Science & Artificial Intelligence"] += 15.0
        elif "physics" in q1: scores["Mechanical & Aerospace Engineering"] += 20.0; scores["Civil & Infrastructure Engineering"] += 15.0
        q2 = ans.get(2, "")
        if "algebra" in q2: scores["Software Engineering & Computer Science"] += 15.0
        elif "geometry" in q2: scores["Architecture & Design"] += 20.0; scores["Civil & Infrastructure Engineering"] += 15.0
        elif "probability" in q2: scores["Data Science & Artificial Intelligence"] += 25.0; scores["Pure Mathematics & Quantitative Research"] += 15.0
        elif "differential equations" in q2: scores["Pure Mathematics & Quantitative Research"] += 20.0; scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "do not enjoy" in q2: scores["Pure Mathematics & Quantitative Research"] -= 20.0; scores["Data Science & Artificial Intelligence"] -= 15.0
        q3 = ans.get(3, "")
        if "writing code" in q3: scores["Software Engineering & Computer Science"] += 25.0
        elif "physical machines" in q3: scores["Mechanical & Aerospace Engineering"] += 25.0; scores["Electronics, VLSI & Robotics"] += 15.0
        elif "complex data" in q3: scores["Data Science & Artificial Intelligence"] += 25.0
        elif "buildings" in q3: scores["Architecture & Design"] += 25.0; scores["Civil & Infrastructure Engineering"] += 20.0
        elif "pure, abstract" in q3: scores["Pure Mathematics & Quantitative Research"] += 25.0
        q4 = ans.get(4, "")
        if "theoretical formulas" in q4: scores["Pure Mathematics & Quantitative Research"] += 15.0
        elif "physical prototype" in q4: scores["Mechanical & Aerospace Engineering"] += 15.0; scores["Electronics, VLSI & Robotics"] += 15.0
        elif "automate" in q4: scores["Software Engineering & Computer Science"] += 15.0; scores["Data Science & Artificial Intelligence"] += 15.0
        elif "drawing" in q4: scores["Architecture & Design"] += 20.0
        q5 = ans.get(5, "")
        if "love it" in q5: scores["Software Engineering & Computer Science"] += 25.0; scores["Data Science & Artificial Intelligence"] += 15.0
        elif "do not like" in q5 or "no interest" in q5: scores["Software Engineering & Computer Science"] -= 30.0; scores["Data Science & Artificial Intelligence"] -= 20.0
        q6 = ans.get(6, "")
        if "mechanics" in q6: scores["Mechanical & Aerospace Engineering"] += 20.0; scores["Civil & Infrastructure Engineering"] += 15.0
        elif "electricity" in q6: scores["Electronics, VLSI & Robotics"] += 25.0
        elif "not very interested" in q6: scores["Mechanical & Aerospace Engineering"] -= 20.0; scores["Civil & Infrastructure Engineering"] -= 15.0
        q7 = ans.get(7, "")
        if "very easy" in q7: scores["Architecture & Design"] += 20.0; scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "struggle" in q7: scores["Architecture & Design"] -= 25.0
        q8 = ans.get(8, "")
        if "tech office" in q8: scores["Software Engineering & Computer Science"] += 15.0; scores["Data Science & Artificial Intelligence"] += 15.0
        elif "manufacturing" in q8: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "construction" in q8: scores["Civil & Infrastructure Engineering"] += 20.0
        elif "design" in q8: scores["Architecture & Design"] += 20.0
        q9 = ans.get(9, "")
        if "sit for hours" in q9: scores["Software Engineering & Computer Science"] += 15.0; scores["Pure Mathematics & Quantitative Research"] += 15.0
        q13 = ans.get(13, "")
        if "digital app" in q13: scores["Software Engineering & Computer Science"] += 20.0
        elif "robotics" in q13: scores["Electronics, VLSI & Robotics"] += 20.0; scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "ai and machine" in q13: scores["Data Science & Artificial Intelligence"] += 25.0
        elif "smart cities" in q13: scores["Civil & Infrastructure Engineering"] += 20.0; scores["Architecture & Design"] += 15.0
        q14 = ans.get(14, "")
        if "pure software" in q14: scores["Software Engineering & Computer Science"] += 20.0; scores["Mechanical & Aerospace Engineering"] -= 15.0
        elif "pure hardware" in q14: scores["Mechanical & Aerospace Engineering"] += 20.0; scores["Civil & Infrastructure Engineering"] += 15.0; scores["Software Engineering & Computer Science"] -= 15.0
        elif "mixture" in q14: scores["Electronics, VLSI & Robotics"] += 25.0
        q15 = ans.get(15, "")
        if "algorithms" in q15: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "engineering physics" in q15: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "pure theories" in q15: scores["Pure Mathematics & Quantitative Research"] += 25.0
        elif "geometry" in q15: scores["Architecture & Design"] += 20.0
        q16 = ans.get(16, "")
        if "remote work" in q16: scores["Software Engineering & Computer Science"] += 15.0; scores["Civil & Infrastructure Engineering"] -= 15.0
        if "tangible, physical" in q16: scores["Mechanical & Aerospace Engineering"] += 15.0; scores["Civil & Infrastructure Engineering"] += 15.0; scores["Software Engineering & Computer Science"] -= 10.0
        if "creative expression" in q16: scores["Architecture & Design"] += 20.0
        q19 = ans.get(19, "")
        if "it/computer" in q19: scores["Software Engineering & Computer Science"] += 25.0
        elif "core engineering" in q19: scores["Mechanical & Aerospace Engineering"] += 25.0; scores["Civil & Infrastructure Engineering"] += 15.0
        elif "architecture" in q19: scores["Architecture & Design"] += 25.0
        elif "data, ai" in q19: scores["Data Science & Artificial Intelligence"] += 25.0; scores["Pure Mathematics & Quantitative Research"] += 15.0
        q20 = ans.get(20, "")
        if "data analyst" in q20: scores["Data Science & Artificial Intelligence"] += 25.0
        elif "aerospace" in q20: scores["Mechanical & Aerospace Engineering"] += 25.0
        elif "architect" in q20: scores["Architecture & Design"] += 25.0
        elif "robotics" in q20: scores["Electronics, VLSI & Robotics"] += 25.0
        elif "civil" in q20: scores["Civil & Infrastructure Engineering"] += 25.0
        elif "mathematician" in q20: scores["Pure Mathematics & Quantitative Research"] += 25.0

    elif stream == "College - Computer Science & IT":
        scores = {
            "Full-Stack / Core Software Engineering": 5.0,
            "Data Science & Artificial Intelligence": 5.0,
            "Cybersecurity & Ethical Hacking": 5.0,
            "Cloud Architecture & DevOps": 5.0,
            "Game Development & Interactive Media": 5.0,
            "Product Management & UI/UX Design": 5.0,
            "Advanced Academic Research & Higher Studies (MS / Ph.D.)": 5.0
        }
        q1 = ans.get(1, "")
        if "complex bug" in q1: scores["Full-Stack / Core Software Engineering"] += 25.0
        elif "predictive model" in q1: scores["Data Science & Artificial Intelligence"] += 25.0
        elif "security loophole" in q1: scores["Cybersecurity & Ethical Hacking"] += 25.0
        elif "server deployment" in q1: scores["Cloud Architecture & DevOps"] += 25.0
        elif "move and look amazing" in q1: scores["Game Development & Interactive Media"] += 25.0
        elif "frictionless user journey" in q1: scores["Product Management & UI/UX Design"] += 25.0
        elif "theoretical computer science algorithm" in q1: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0

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