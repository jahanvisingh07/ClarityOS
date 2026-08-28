from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

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

    # Zero submission check
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
            "evaluated_vectors": sorted_matches
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

    elif stream == "Commerce":
        scores = { "Chartered Accountancy (CA) & Corporate Finance": 5.0, "Investment Banking & Equity Research": 5.0, "Corporate Law & Legal Consulting": 5.0, "Marketing, Advertising & Brand Management": 5.0, "Entrepreneurship & Business Strategy": 5.0, "Actuarial Science & Risk Management": 5.0, "Human Resources & Organizational Behavior": 5.0 }
        q1 = ans.get(1, "")
        if "accountancy" in q1: scores["Chartered Accountancy (CA) & Corporate Finance"] += 25.0; scores["Investment Banking & Equity Research"] += 10.0
        elif "economics" in q1: scores["Investment Banking & Equity Research"] += 20.0; scores["Actuarial Science & Risk Management"] += 15.0
        elif "business studies" in q1: scores["Entrepreneurship & Business Strategy"] += 20.0; scores["Marketing, Advertising & Brand Management"] += 15.0
        elif "mathematics" in q1: scores["Actuarial Science & Risk Management"] += 25.0
        q2 = ans.get(2, "")
        if "balance sheets" in q2: scores["Chartered Accountancy (CA) & Corporate Finance"] += 25.0
        elif "macro market" in q2: scores["Investment Banking & Equity Research"] += 20.0; scores["Actuarial Science & Risk Management"] += 15.0
        elif "legal documents" in q2: scores["Corporate Law & Legal Consulting"] += 25.0
        elif "consumer behaviour" in q2: scores["Marketing, Advertising & Brand Management"] += 25.0
        elif "employee performance" in q2: scores["Human Resources & Organizational Behavior"] += 25.0
        q3 = ans.get(3, "")
        if "auditing" in q3: scores["Chartered Accountancy (CA) & Corporate Finance"] += 25.0; scores["Corporate Law & Legal Consulting"] += 10.0
        elif "stock market" in q3: scores["Investment Banking & Equity Research"] += 25.0
        elif "arguing" in q3: scores["Corporate Law & Legal Consulting"] += 25.0
        elif "viral marketing" in q3: scores["Marketing, Advertising & Brand Management"] += 25.0
        elif "building a business" in q3: scores["Entrepreneurship & Business Strategy"] += 25.0
        q4 = ans.get(4, "")
        if "love advanced math" in q4: scores["Actuarial Science & Risk Management"] += 30.0; scores["Investment Banking & Equity Research"] += 15.0
        elif "basic arithmetic" in q4: scores["Chartered Accountancy (CA) & Corporate Finance"] += 15.0; scores["Entrepreneurship & Business Strategy"] += 15.0
        elif "strongly dislike" in q4: scores["Corporate Law & Legal Consulting"] += 15.0; scores["Human Resources & Organizational Behavior"] += 15.0; scores["Actuarial Science & Risk Management"] -= 25.0
        q5 = ans.get(5, "")
        if "strictly follow" in q5: scores["Chartered Accountancy (CA) & Corporate Finance"] += 20.0; scores["Actuarial Science & Risk Management"] += 15.0
        elif "creative loopholes" in q5: scores["Corporate Law & Legal Consulting"] += 20.0; scores["Entrepreneurship & Business Strategy"] += 15.0
        elif "total freedom" in q5: scores["Entrepreneurship & Business Strategy"] += 20.0; scores["Marketing, Advertising & Brand Management"] += 15.0
        elif "how laws are made" in q5: scores["Corporate Law & Legal Consulting"] += 25.0
        q6 = ans.get(6, "")
        if "very high" in q6: scores["Entrepreneurship & Business Strategy"] += 25.0; scores["Investment Banking & Equity Research"] += 15.0; scores["Chartered Accountancy (CA) & Corporate Finance"] -= 15.0
        elif "calculated" in q6: scores["Actuarial Science & Risk Management"] += 20.0; scores["Investment Banking & Equity Research"] += 15.0
        elif "low" in q6: scores["Chartered Accountancy (CA) & Corporate Finance"] += 20.0; scores["Human Resources & Organizational Behavior"] += 15.0
        q7 = ans.get(7, "")
        if "invest it" in q7: scores["Investment Banking & Equity Research"] += 20.0
        elif "legal and financial" in q7: scores["Corporate Law & Legal Consulting"] += 15.0; scores["Chartered Accountancy (CA) & Corporate Finance"] += 15.0
        elif "facebook ads" in q7: scores["Marketing, Advertising & Brand Management"] += 25.0
        elif "prototype" in q7: scores["Entrepreneurship & Business Strategy"] += 25.0
        elif "high-interest" in q7: scores["Actuarial Science & Risk Management"] += 15.0; scores["Chartered Accountancy (CA) & Corporate Finance"] += 15.0
        q8 = ans.get(8, "")
        if "quiet desk" in q8: scores["Chartered Accountancy (CA) & Corporate Finance"] += 15.0; scores["Actuarial Science & Risk Management"] += 15.0
        elif "trading floor" in q8: scores["Investment Banking & Equity Research"] += 25.0
        elif "law firm" in q8: scores["Corporate Law & Legal Consulting"] += 25.0
        elif "advertising studio" in q8: scores["Marketing, Advertising & Brand Management"] += 25.0
        elif "startup hub" in q8: scores["Entrepreneurship & Business Strategy"] += 25.0
        q9 = ans.get(9, "")
        if "pitching ideas" in q9: scores["Entrepreneurship & Business Strategy"] += 20.0; scores["Marketing, Advertising & Brand Management"] += 15.0
        elif "debating" in q9: scores["Corporate Law & Legal Consulting"] += 25.0
        elif "small board" in q9: scores["Chartered Accountancy (CA) & Corporate Finance"] += 15.0; scores["Investment Banking & Equity Research"] += 15.0
        elif "strongly dislike" in q9: scores["Corporate Law & Legal Consulting"] -= 20.0; scores["Marketing, Advertising & Brand Management"] -= 15.0
        q11 = ans.get(11, "")
        if "enjoy reading deep laws" in q11: scores["Corporate Law & Legal Consulting"] += 30.0
        elif "spreadsheet" in q11: scores["Chartered Accountancy (CA) & Corporate Finance"] += 20.0; scores["Actuarial Science & Risk Management"] += 15.0; scores["Corporate Law & Legal Consulting"] -= 15.0
        q12 = ans.get(12, "")
        if "product/service" in q12: scores["Marketing, Advertising & Brand Management"] += 20.0; scores["Entrepreneurship & Business Strategy"] += 15.0
        elif "people" in q12: scores["Human Resources & Organizational Behavior"] += 30.0
        elif "numbers" in q12: scores["Chartered Accountancy (CA) & Corporate Finance"] += 20.0; scores["Investment Banking & Equity Research"] += 20.0; scores["Actuarial Science & Risk Management"] += 15.0
        q16 = ans.get(16, "")
        if "extreme wealth" in q16: scores["Investment Banking & Equity Research"] += 20.0; scores["Entrepreneurship & Business Strategy"] += 15.0
        if "power and influence" in q16: scores["Corporate Law & Legal Consulting"] += 15.0; scores["Investment Banking & Equity Research"] += 10.0
        if "creative expression" in q16: scores["Marketing, Advertising & Brand Management"] += 20.0; scores["Chartered Accountancy (CA) & Corporate Finance"] -= 15.0
        if "job security" in q16: scores["Chartered Accountancy (CA) & Corporate Finance"] += 20.0; scores["Entrepreneurship & Business Strategy"] -= 20.0
        q18 = ans.get(18, "")
        if "competitive professional" in q18: scores["Chartered Accountancy (CA) & Corporate Finance"] += 25.0; scores["Actuarial Science & Risk Management"] += 15.0
        elif "mba" in q18: scores["Investment Banking & Equity Research"] += 15.0; scores["Marketing, Advertising & Brand Management"] += 15.0
        elif "law school" in q18: scores["Corporate Law & Legal Consulting"] += 30.0
        elif "start working" in q18: scores["Entrepreneurship & Business Strategy"] += 25.0
        q19 = ans.get(19, "")
        if "hardcore finance" in q19: scores["Chartered Accountancy (CA) & Corporate Finance"] += 20.0; scores["Investment Banking & Equity Research"] += 20.0
        elif "lawyer" in q19: scores["Corporate Law & Legal Consulting"] += 25.0
        elif "marketing" in q19: scores["Marketing, Advertising & Brand Management"] += 25.0; scores["Human Resources & Organizational Behavior"] += 15.0
        elif "entrepreneur" in q19: scores["Entrepreneurship & Business Strategy"] += 25.0
        q20 = ans.get(20, "")
        if "cfo" in q20: scores["Chartered Accountancy (CA) & Corporate Finance"] += 25.0
        elif "investment banker" in q20: scores["Investment Banking & Equity Research"] += 25.0
        elif "lawyer" in q20: scores["Corporate Law & Legal Consulting"] += 25.0
        elif "cmo" in q20: scores["Marketing, Advertising & Brand Management"] += 25.0
        elif "ceo" in q20: scores["Entrepreneurship & Business Strategy"] += 25.0
        elif "hr" in q20: scores["Human Resources & Organizational Behavior"] += 25.0
        elif "actuary" in q20: scores["Actuarial Science & Risk Management"] += 25.0

    elif stream == "Arts / Humanities":
        scores = { "Psychology & Counseling": 5.0, "Journalism, Media & Mass Communication": 5.0, "Political Science & International Relations": 5.0, "Literature, Writing & Editorial": 5.0, "Fine Arts, Design & Animation": 5.0, "Sociology & Social Work": 5.0, "History, Archaeology & Anthropology": 5.0 }
        q1 = ans.get(1, "")
        if "psychology" in q1: scores["Psychology & Counseling"] += 25.0; scores["Sociology & Social Work"] += 10.0
        elif "political science" in q1: scores["Political Science & International Relations"] += 25.0; scores["Journalism, Media & Mass Communication"] += 10.0
        elif "literature" in q1: scores["Literature, Writing & Editorial"] += 25.0
        elif "history" in q1: scores["History, Archaeology & Anthropology"] += 25.0
        elif "fine arts" in q1: scores["Fine Arts, Design & Animation"] += 25.0
        elif "sociology" in q1: scores["Sociology & Social Work"] += 25.0
        q2 = ans.get(2, "")
        if "storytelling" in q2: scores["Literature, Writing & Editorial"] += 20.0; scores["Fine Arts, Design & Animation"] += 10.0
        elif "public speaking" in q2: scores["Political Science & International Relations"] += 20.0; scores["Journalism, Media & Mass Communication"] += 15.0
        elif "visual art" in q2: scores["Fine Arts, Design & Animation"] += 25.0
        elif "factual reporting" in q2: scores["Journalism, Media & Mass Communication"] += 25.0
        elif "listening" in q2: scores["Psychology & Counseling"] += 25.0; scores["Sociology & Social Work"] += 15.0
        q3 = ans.get(3, "")
        if "mental health" in q3: scores["Psychology & Counseling"] += 25.0
        elif "global news" in q3: scores["Journalism, Media & Mass Communication"] += 25.0; scores["Political Science & International Relations"] += 15.0
        elif "drafting policies" in q3: scores["Political Science & International Relations"] += 25.0
        elif "writing a novel" in q3: scores["Literature, Writing & Editorial"] += 25.0
        elif "beautiful painting" in q3: scores["Fine Arts, Design & Animation"] += 25.0
        elif "ancient ruins" in q3: scores["History, Archaeology & Anthropology"] += 25.0
        q4 = ans.get(4, "")
        if "deep academic" in q4: scores["History, Archaeology & Anthropology"] += 20.0; scores["Political Science & International Relations"] += 15.0
        elif "fiction" in q4: scores["Literature, Writing & Editorial"] += 25.0
        elif "daily news" in q4: scores["Journalism, Media & Mass Communication"] += 25.0
        elif "visual media" in q4: scores["Fine Arts, Design & Animation"] += 25.0; scores["Literature, Writing & Editorial"] -= 15.0
        q5 = ans.get(5, "")
        if "individual behaves" in q5: scores["Psychology & Counseling"] += 25.0
        elif "society and cultures" in q5: scores["Sociology & Social Work"] += 20.0; scores["History, Archaeology & Anthropology"] += 20.0
        elif "governments negotiate" in q5: scores["Political Science & International Relations"] += 25.0
        elif "visually appealing" in q5: scores["Fine Arts, Design & Animation"] += 25.0
        q6 = ans.get(6, "")
        if "empathetic" in q6: scores["Psychology & Counseling"] += 20.0; scores["Sociology & Social Work"] += 20.0
        elif "objectively" in q6: scores["Political Science & International Relations"] += 15.0; scores["Journalism, Media & Mass Communication"] += 15.0
        elif "art or writing" in q6: scores["Fine Arts, Design & Animation"] += 20.0; scores["Literature, Writing & Editorial"] += 20.0
        elif "social justice" in q6: scores["Sociology & Social Work"] += 25.0; scores["Political Science & International Relations"] += 15.0
        q7 = ans.get(7, "")
        if "therapy office" in q7: scores["Psychology & Counseling"] += 25.0
        elif "newsroom" in q7: scores["Journalism, Media & Mass Communication"] += 25.0
        elif "government office" in q7: scores["Political Science & International Relations"] += 25.0
        elif "creative design" in q7: scores["Fine Arts, Design & Animation"] += 25.0
        elif "museum" in q7: scores["History, Archaeology & Anthropology"] += 25.0
        elif "ngo" in q7: scores["Sociology & Social Work"] += 25.0
        q8 = ans.get(8, "")
        if "healing one person" in q8: scores["Psychology & Counseling"] += 25.0
        elif "exposing the truth" in q8: scores["Journalism, Media & Mass Communication"] += 25.0
        elif "rewriting laws" in q8: scores["Political Science & International Relations"] += 25.0
        elif "creating art" in q8: scores["Literature, Writing & Editorial"] += 20.0; scores["Fine Arts, Design & Animation"] += 20.0
        elif "community social work" in q8: scores["Sociology & Social Work"] += 25.0
        q9 = ans.get(9, "")
        if "fictional writing" in q9: scores["Literature, Writing & Editorial"] += 25.0
        elif "investigative writing" in q9: scores["Journalism, Media & Mass Communication"] += 25.0
        elif "academic, historical" in q9: scores["History, Archaeology & Anthropology"] += 20.0; scores["Political Science & International Relations"] += 15.0
        elif "do not enjoy writing" in q9: scores["Fine Arts, Design & Animation"] += 25.0; scores["Literature, Writing & Editorial"] -= 20.0; scores["Journalism, Media & Mass Communication"] -= 15.0
        q10 = ans.get(10, "")
        if "debates" in q10: scores["Political Science & International Relations"] += 25.0
        elif "camera or microphone" in q10: scores["Journalism, Media & Mass Communication"] += 25.0
        elif "one-on-one" in q10: scores["Psychology & Counseling"] += 20.0; scores["Sociology & Social Work"] += 15.0
        elif "text or art" in q10: scores["Fine Arts, Design & Animation"] += 20.0; scores["Literature, Writing & Editorial"] += 20.0
        q11 = ans.get(11, "")
        if "strong artistic" in q11: scores["Fine Arts, Design & Animation"] += 30.0
        elif "dabble" in q11: scores["Fine Arts, Design & Animation"] += 15.0
        elif "zero interest" in q11: scores["Fine Arts, Design & Animation"] -= 25.0
        q12 = ans.get(12, "")
        if "directly help" in q12: scores["Sociology & Social Work"] += 25.0; scores["Psychology & Counseling"] += 15.0
        elif "document" in q12: scores["Journalism, Media & Mass Communication"] += 20.0
        elif "change the laws" in q12: scores["Political Science & International Relations"] += 20.0
        elif "struggle to handle" in q12: scores["Sociology & Social Work"] -= 20.0; scores["Psychology & Counseling"] -= 20.0
        q16 = ans.get(16, "")
        if "creative freedom" in q16: scores["Fine Arts, Design & Animation"] += 15.0; scores["Literature, Writing & Editorial"] += 15.0
        if "social impact" in q16: scores["Sociology & Social Work"] += 20.0; scores["Psychology & Counseling"] += 10.0
        if "understanding the human mind" in q16: scores["Psychology & Counseling"] += 20.0
        if "influence and shaping" in q16: scores["Political Science & International Relations"] += 20.0
        if "uncovering the truth" in q16: scores["Journalism, Media & Mass Communication"] += 20.0
        if "aesthetic beauty" in q16: scores["Fine Arts, Design & Animation"] += 20.0
        if "preserving history" in q16: scores["History, Archaeology & Anthropology"] += 20.0
        q17 = ans.get(17, "")
        if "the past" in q17: scores["History, Archaeology & Anthropology"] += 25.0; scores["Literature, Writing & Editorial"] += 10.0
        elif "the present" in q17: scores["Journalism, Media & Mass Communication"] += 20.0; scores["Sociology & Social Work"] += 15.0
        elif "the future" in q17: scores["Political Science & International Relations"] += 25.0
        q18 = ans.get(18, "")
        if "psychology or counseling" in q18: scores["Psychology & Counseling"] += 25.0
        elif "journalism or media" in q18: scores["Journalism, Media & Mass Communication"] += 25.0
        elif "international relations" in q18: scores["Political Science & International Relations"] += 25.0
        elif "creative portfolio" in q18: scores["Fine Arts, Design & Animation"] += 25.0; scores["Literature, Writing & Editorial"] += 15.0
        q19 = ans.get(19, "")
        if "psychologist" in q19: scores["Psychology & Counseling"] += 25.0
        elif "media, journalism" in q19: scores["Journalism, Media & Mass Communication"] += 25.0
        elif "politics" in q19: scores["Political Science & International Relations"] += 25.0
        elif "writer, author" in q19: scores["Literature, Writing & Editorial"] += 25.0
        elif "designer, animator" in q19: scores["Fine Arts, Design & Animation"] += 25.0
        elif "historian" in q19: scores["History, Archaeology & Anthropology"] += 25.0
        q20 = ans.get(20, "")
        if "psychologist" in q20: scores["Psychology & Counseling"] += 25.0
        elif "investigative journalist" in q20: scores["Journalism, Media & Mass Communication"] += 25.0
        elif "diplomat" in q20: scores["Political Science & International Relations"] += 25.0
        elif "published author" in q20: scores["Literature, Writing & Editorial"] += 25.0
        elif "creative art director" in q20: scores["Fine Arts, Design & Animation"] += 25.0
        elif "social worker" in q20: scores["Sociology & Social Work"] += 25.0
        elif "historian" in q20: scores["History, Archaeology & Anthropology"] += 25.0

    elif stream == "College - Medicine & Life Sciences":
        scores = {
            "Clinical Practice (Medicine/Surgery/Dentistry)": 5.0,
            "Biotechnology & Genomic Research": 5.0,
            "Allied Health & Rehabilitation": 5.0,
            "Pharmacology & Drug Development": 5.0,
            "Public Health & Epidemiology": 5.0
        }
        q1 = ans.get(1, "")
        if "patient care" in q1: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 20.0
        elif "dna and cells" in q1: scores["Biotechnology & Genomic Research"] += 20.0
        elif "chemical drugs" in q1: scores["Pharmacology & Drug Development"] += 20.0
        elif "big data" in q1: scores["Public Health & Epidemiology"] += 20.0
        elif "muscles" in q1: scores["Allied Health & Rehabilitation"] += 20.0
        q2 = ans.get(2, "")
        if "hospital" in q2: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 20.0
        elif "research lab" in q2: scores["Biotechnology & Genomic Research"] += 20.0
        elif "manufacturing" in q2: scores["Pharmacology & Drug Development"] += 20.0
        elif "office analyzing" in q2: scores["Public Health & Epidemiology"] += 20.0
        elif "gym or physical" in q2: scores["Allied Health & Rehabilitation"] += 20.0
        q3 = ans.get(3, "")
        if "all day long" in q3: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 15.0; scores["Allied Health & Rehabilitation"] += 15.0
        elif "just a little" in q3: scores["Pharmacology & Drug Development"] += 15.0
        elif "none at all" in q3: scores["Biotechnology & Genomic Research"] += 20.0; scores["Clinical Practice (Medicine/Surgery/Dentistry)"] -= 20.0
        elif "policymakers" in q3: scores["Public Health & Epidemiology"] += 20.0
        elif "recovery journey" in q3: scores["Allied Health & Rehabilitation"] += 20.0
        q4 = ans.get(4, "")
        if "thrive in intense" in q4: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 20.0
        elif "predictable schedule" in q4: scores["Allied Health & Rehabilitation"] += 15.0; scores["Pharmacology & Drug Development"] += 15.0
        elif "deep, slow" in q4: scores["Biotechnology & Genomic Research"] += 20.0
        elif "preventing" in q4: scores["Public Health & Epidemiology"] += 20.0
        q5 = ans.get(5, "")
        if "operating room" in q5: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 25.0
        elif "medicines and pills" in q5: scores["Pharmacology & Drug Development"] += 20.0
        elif "microscopes" in q5: scores["Biotechnology & Genomic Research"] += 20.0
        elif "keep me away" in q5: scores["Public Health & Epidemiology"] += 15.0; scores["Allied Health & Rehabilitation"] += 15.0; scores["Clinical Practice (Medicine/Surgery/Dentistry)"] -= 25.0
        q6 = ans.get(6, "")
        if "face-to-face" in q6: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 15.0
        elif "invent a new drug" in q6: scores["Pharmacology & Drug Development"] += 20.0; scores["Biotechnology & Genomic Research"] += 15.0
        elif "cities or countries" in q6: scores["Public Health & Epidemiology"] += 25.0
        elif "recovering" in q6: scores["Allied Health & Rehabilitation"] += 20.0
        q7 = ans.get(7, "")
        if "illness a patient has" in q7: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 20.0
        elif "genetic mutation" in q7: scores["Biotechnology & Genomic Research"] += 20.0
        elif "pill absorb" in q7: scores["Pharmacology & Drug Development"] += 20.0
        elif "virus spread" in q7: scores["Public Health & Epidemiology"] += 20.0
        elif "custom exercise" in q7: scores["Allied Health & Rehabilitation"] += 20.0
        q8 = ans.get(8, "")
        if "surgeons" in q8: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 20.0
        elif "biologists" in q8: scores["Biotechnology & Genomic Research"] += 20.0
        elif "chemists" in q8: scores["Pharmacology & Drug Development"] += 20.0
        elif "government" in q8: scores["Public Health & Epidemiology"] += 20.0
        elif "dietitians" in q8: scores["Allied Health & Rehabilitation"] += 20.0
        q9 = ans.get(9, "")
        if "surprise" in q9: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 15.0
        elif "steady routine" in q9: scores["Biotechnology & Genomic Research"] += 15.0; scores["Pharmacology & Drug Development"] += 15.0
        elif "scheduled patient" in q9: scores["Allied Health & Rehabilitation"] += 15.0
        elif "desk" in q9: scores["Public Health & Epidemiology"] += 15.0
        q10 = ans.get(10, "")
        if "pure anatomy" in q10: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 20.0
        elif "chemistry" in q10: scores["Pharmacology & Drug Development"] += 25.0
        elif "statistics" in q10: scores["Public Health & Epidemiology"] += 25.0
        elif "genetics" in q10: scores["Biotechnology & Genomic Research"] += 25.0
        elif "kinesiology" in q10: scores["Allied Health & Rehabilitation"] += 25.0
        q11 = ans.get(11, "")
        if "losing a patient" in q11: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 10.0
        elif "experiment failing" in q11: scores["Biotechnology & Genomic Research"] += 10.0
        elif "drug failing" in q11: scores["Pharmacology & Drug Development"] += 10.0
        elif "ignoring public health" in q11: scores["Public Health & Epidemiology"] += 10.0
        elif "rehab exercises" in q11: scores["Allied Health & Rehabilitation"] += 10.0
        q12 = ans.get(12, "")
        if "medical case studies" in q12: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 15.0
        elif "crispr" in q12: scores["Biotechnology & Genomic Research"] += 15.0
        elif "fda drug" in q12: scores["Pharmacology & Drug Development"] += 15.0
        elif "pandemic tracking" in q12: scores["Public Health & Epidemiology"] += 15.0
        elif "sports medicine" in q12: scores["Allied Health & Rehabilitation"] += 15.0
        q13 = ans.get(13, "")
        if "immediate" in q13: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 15.0
        elif "weeks or months" in q13: scores["Allied Health & Rehabilitation"] += 20.0
        elif "years" in q13: scores["Biotechnology & Genomic Research"] += 15.0; scores["Pharmacology & Drug Development"] += 15.0
        q14 = ans.get(14, "")
        if "lead doctor" in q14: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 15.0
        elif "research lab" in q14: scores["Biotechnology & Genomic Research"] += 15.0
        elif "health department" in q14: scores["Public Health & Epidemiology"] += 15.0
        elif "supportive" in q14: scores["Allied Health & Rehabilitation"] += 15.0
        q15 = ans.get(15, "")
        if "stethoscope" in q15: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 20.0
        elif "dna sequencer" in q15: scores["Biotechnology & Genomic Research"] += 20.0
        elif "flasks" in q15: scores["Pharmacology & Drug Development"] += 20.0
        elif "laptop" in q15: scores["Public Health & Epidemiology"] += 20.0
        elif "therapy bands" in q15: scores["Allied Health & Rehabilitation"] += 20.0
        q16 = ans.get(16, "")
        if "crucial for drug" in q16: scores["Pharmacology & Drug Development"] += 15.0
        elif "protecting public health" in q16: scores["Public Health & Epidemiology"] += 15.0
        elif "hospital protocols" in q16: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 15.0
        elif "annoying" in q16: scores["Biotechnology & Genomic Research"] += 15.0
        q17 = ans.get(17, "")
        if "life-saving doctor" in q17: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 20.0
        elif "new gene" in q17: scores["Biotechnology & Genomic Research"] += 20.0
        elif "rehab" in q17: scores["Allied Health & Rehabilitation"] += 20.0
        elif "blockbuster" in q17: scores["Pharmacology & Drug Development"] += 20.0
        elif "outbreak" in q17: scores["Public Health & Epidemiology"] += 20.0
        q18 = ans.get(18, "")
        if "crazy on-call" in q18: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 15.0
        elif "strict 9-to-5" in q18: scores["Pharmacology & Drug Development"] += 15.0; scores["Public Health & Epidemiology"] += 15.0; scores["Clinical Practice (Medicine/Surgery/Dentistry)"] -= 15.0
        elif "flexibility" in q18: scores["Biotechnology & Genomic Research"] += 15.0
        elif "balanced schedule" in q18: scores["Allied Health & Rehabilitation"] += 15.0
        q19 = ans.get(19, "")
        if "medical school" in q19: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 25.0
        elif "phd" in q19: scores["Biotechnology & Genomic Research"] += 15.0; scores["Public Health & Epidemiology"] += 15.0
        elif "shorter specialized" in q19: scores["Allied Health & Rehabilitation"] += 20.0; scores["Clinical Practice (Medicine/Surgery/Dentistry)"] -= 20.0
        q20 = ans.get(20, "")
        if "detective" in q20: scores["Clinical Practice (Medicine/Surgery/Dentistry)"] += 10.0
        elif "chemical engineer" in q20: scores["Pharmacology & Drug Development"] += 15.0
        elif "politician" in q20: scores["Public Health & Epidemiology"] += 15.0
        elif "fitness coach" in q20: scores["Allied Health & Rehabilitation"] += 15.0
        elif "software" in q20: scores["Biotechnology & Genomic Research"] += 15.0

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
        q2 = ans.get(2, "")
        if "fast it loads" in q2: scores["Full-Stack / Core Software Engineering"] += 20.0
        elif "recommendation algorithm" in q2: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "secure my personal data" in q2: scores["Cybersecurity & Ethical Hacking"] += 20.0
        elif "stays online" in q2: scores["Cloud Architecture & DevOps"] += 20.0
        elif "animations and graphics" in q2: scores["Game Development & Interactive Media"] += 20.0
        elif "buttons are placed" in q2: scores["Product Management & UI/UX Design"] += 20.0
        elif "foundational computer science theory" in q2: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q3 = ans.get(3, "")
        if "satisfaction of finally fixing" in q3: scores["Full-Stack / Core Software Engineering"] += 20.0
        elif "math and algorithms" in q3: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "reverse-engineering" in q3: scores["Cybersecurity & Ethical Hacking"] += 20.0
        elif "automate the testing pipelines" in q3: scores["Cloud Architecture & DevOps"] += 20.0
        elif "tweaking physics" in q3: scores["Game Development & Interactive Media"] += 20.0
        elif "user flow" in q3: scores["Product Management & UI/UX Design"] += 20.0; scores["Full-Stack / Core Software Engineering"] -= 15.0
        elif "mathematical proofs" in q3: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q4 = ans.get(4, "")
        if "functional web" in q4: scores["Full-Stack / Core Software Engineering"] += 20.0
        elif "scraping a website" in q4: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "capture the flag" in q4: scores["Cybersecurity & Ethical Hacking"] += 20.0
        elif "home network" in q4: scores["Cloud Architecture & DevOps"] += 20.0
        elif "mini 2d/3d game" in q4: scores["Game Development & Interactive Media"] += 20.0
        elif "figma prototype" in q4: scores["Product Management & UI/UX Design"] += 20.0
        elif "research paper" in q4: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q5 = ans.get(5, "")
        if "basic logic" in q5: scores["Full-Stack / Core Software Engineering"] += 15.0
        elif "statistics, calculus" in q5: scores["Data Science & Artificial Intelligence"] += 25.0
        elif "cryptography" in q5: scores["Cybersecurity & Ethical Hacking"] += 15.0
        elif "calculating server bandwidth" in q5: scores["Cloud Architecture & DevOps"] += 15.0
        elif "physics, geometry" in q5: scores["Game Development & Interactive Media"] += 25.0
        elif "human psychology" in q5: scores["Product Management & UI/UX Design"] += 20.0
        elif "formal proofs" in q5: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 35.0
        q6 = ans.get(6, "")
        if "other software developers" in q6: scores["Full-Stack / Core Software Engineering"] += 15.0
        elif "data analysts" in q6: scores["Data Science & Artificial Intelligence"] += 15.0
        elif "security auditors" in q6: scores["Cybersecurity & Ethical Hacking"] += 15.0
        elif "network engineers" in q6: scores["Cloud Architecture & DevOps"] += 15.0
        elif "artists, animators" in q6: scores["Game Development & Interactive Media"] += 25.0
        elif "users, customers" in q6: scores["Product Management & UI/UX Design"] += 25.0
        elif "professors" in q6: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q7 = ans.get(7, "")
        if "lead developer" in q7: scores["Full-Stack / Core Software Engineering"] += 25.0
        elif "ai wizard" in q7: scores["Data Science & Artificial Intelligence"] += 25.0
        elif "head of security" in q7: scores["Cybersecurity & Ethical Hacking"] += 25.0
        elif "infrastructure boss" in q7: scores["Cloud Architecture & DevOps"] += 25.0
        elif "technical artist" in q7: scores["Game Development & Interactive Media"] += 25.0
        elif "visionary deciding" in q7: scores["Product Management & UI/UX Design"] += 25.0
        elif "chief scientist" in q7: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q8 = ans.get(8, "")
        if "works perfectly" in q8: scores["Full-Stack / Core Software Engineering"] += 15.0
        elif "data visualization" in q8: scores["Data Science & Artificial Intelligence"] += 15.0
        elif "secure" in q8: scores["Cybersecurity & Ethical Hacking"] += 15.0
        elif "scalable" in q8: scores["Cloud Architecture & DevOps"] += 15.0
        elif "rendering, lighting" in q8: scores["Game Development & Interactive Media"] += 25.0
        elif "layouts, wireframes" in q8: scores["Product Management & UI/UX Design"] += 25.0
        elif "mathematical precision" in q8: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 20.0
        q9 = ans.get(9, "")
        if "demo of my working code" in q9: scores["Full-Stack / Core Software Engineering"] += 15.0
        elif "data discovery" in q9: scores["Data Science & Artificial Intelligence"] += 15.0
        elif "threat models" in q9: scores["Cybersecurity & Ethical Hacking"] += 15.0
        elif "uptime metrics" in q9: scores["Cloud Architecture & DevOps"] += 15.0
        elif "visual demo" in q9: scores["Game Development & Interactive Media"] += 20.0
        elif "pitch the product" in q9: scores["Product Management & UI/UX Design"] += 25.0
        elif "academic conferences" in q9: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q10 = ans.get(10, "")
        if "coding katas" in q10: scores["Full-Stack / Core Software Engineering"] += 15.0
        elif "number games" in q10: scores["Data Science & Artificial Intelligence"] += 15.0
        elif "escape rooms" in q10: scores["Cybersecurity & Ethical Hacking"] += 15.0
        elif "optimizing a messy" in q10: scores["Cloud Architecture & DevOps"] += 15.0
        elif "spatial puzzles" in q10: scores["Game Development & Interactive Media"] += 20.0
        elif "people make the decisions" in q10: scores["Product Management & UI/UX Design"] += 20.0
        elif "unsolved theoretical theorems" in q10: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q11 = ans.get(11, "")
        if "tangled codebase" in q11: scores["Full-Stack / Core Software Engineering"] += 20.0
        elif "biased or wrong answers" in q11: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "data breach" in q11: scores["Cybersecurity & Ethical Hacking"] += 25.0
        elif "servers crashing" in q11: scores["Cloud Architecture & DevOps"] += 25.0
        elif "laggy visuals" in q11: scores["Game Development & Interactive Media"] += 20.0
        elif "nobody actually wants" in q11: scores["Product Management & UI/UX Design"] += 25.0
        elif "commercial coding instead of deep" in q11: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q12 = ans.get(12, "")
        if "react" in q12: scores["Full-Stack / Core Software Engineering"] += 25.0
        elif "tensorflow" in q12: scores["Data Science & Artificial Intelligence"] += 25.0
        elif "kali linux" in q12: scores["Cybersecurity & Ethical Hacking"] += 25.0
        elif "aws" in q12: scores["Cloud Architecture & DevOps"] += 25.0
        elif "unity" in q12: scores["Game Development & Interactive Media"] += 25.0
        elif "figma" in q12: scores["Product Management & UI/UX Design"] += 25.0
        elif "latex" in q12: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q13 = ans.get(13, "")
        if "features from nothing" in q13: scores["Full-Stack / Core Software Engineering"] += 20.0
        elif "hidden patterns" in q13: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "before the bad guys" in q13: scores["Cybersecurity & Ethical Hacking"] += 25.0
        elif "run faster behind the scenes" in q13: scores["Cloud Architecture & DevOps"] += 20.0
        elif "interactive worlds" in q13: scores["Game Development & Interactive Media"] += 20.0
        elif "beautiful and intuitive" in q13: scores["Product Management & UI/UX Design"] += 20.0
        elif "fundamental new computer science principles" in q13: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q14 = ans.get(14, "")
        if "code is logical" in q14: scores["Full-Stack / Core Software Engineering"] += 15.0
        elif "massive datasets" in q14: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "weakest link" in q14: scores["Cybersecurity & Ethical Hacking"] += 20.0
        elif "route their web traffic" in q14: scores["Cloud Architecture & DevOps"] += 15.0
        elif "entertain them" in q14: scores["Game Development & Interactive Media"] += 20.0
        elif "solve their problems" in q14: scores["Product Management & UI/UX Design"] += 25.0
        elif "formal academic models" in q14: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q15 = ans.get(15, "")
        if "cto" in q15: scores["Full-Stack / Core Software Engineering"] += 20.0
        elif "data scientist" in q15: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "ciso" in q15: scores["Cybersecurity & Ethical Hacking"] += 25.0
        elif "devops engineer" in q15: scores["Cloud Architecture & DevOps"] += 20.0
        elif "game director" in q15: scores["Game Development & Interactive Media"] += 20.0
        elif "ceo" in q15: scores["Product Management & UI/UX Design"] += 20.0
        elif "university professor" in q15: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 35.0
        q16 = ans.get(16, "")
        if "coding frameworks" in q16: scores["Full-Stack / Core Software Engineering"] += 20.0
        elif "math and stats" in q16: scores["Data Science & Artificial Intelligence"] += 15.0
        elif "zero-day vulnerabilities" in q16: scores["Cybersecurity & Ethical Hacking"] += 20.0
        elif "deployment automation" in q16: scores["Cloud Architecture & DevOps"] += 20.0
        elif "graphics capabilities" in q16: scores["Game Development & Interactive Media"] += 20.0
        elif "timeless human psychology" in q16: scores["Product Management & UI/UX Design"] += 20.0
        elif "theoretical fundamentals" in q16: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q17 = ans.get(17, "")
        if "clean architecture" in q17: scores["Full-Stack / Core Software Engineering"] += 20.0
        elif "artificial intelligence" in q17: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "famous cyber attacks" in q17: scores["Cybersecurity & Ethical Hacking"] += 20.0
        elif "site reliability" in q17: scores["Cloud Architecture & DevOps"] += 20.0
        elif "legendary video game" in q17: scores["Game Development & Interactive Media"] += 20.0
        elif "iconic products" in q17: scores["Product Management & UI/UX Design"] += 20.0
        elif "quantum computing or deep learning theory" in q17: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q18 = ans.get(18, "")
        if "bug-free code" in q18: scores["Full-Stack / Core Software Engineering"] += 20.0
        elif "trends in data" in q18: scores["Data Science & Artificial Intelligence"] += 20.0
        elif "attacker to defend" in q18: scores["Cybersecurity & Ethical Hacking"] += 20.0
        elif "scaling massive systems" in q18: scores["Cloud Architecture & DevOps"] += 20.0
        elif "technical logic with creative" in q18: scores["Game Development & Interactive Media"] += 20.0
        elif "understanding what users" in q18: scores["Product Management & UI/UX Design"] += 20.0
        elif "rigorous academic thinking" in q18: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q19 = ans.get(19, "")
        if "code libraries" in q19: scores["Full-Stack / Core Software Engineering"] += 15.0
        elif "a/b testing data" in q19: scores["Data Science & Artificial Intelligence"] += 15.0
        elif "security bugs" in q19: scores["Cybersecurity & Ethical Hacking"] += 15.0
        elif "servers are handling" in q19: scores["Cloud Architecture & DevOps"] += 15.0
        elif "ui animations" in q19: scores["Game Development & Interactive Media"] += 15.0
        elif "easier to use" in q19: scores["Product Management & UI/UX Design"] += 15.0
        elif "whitepaper" in q19: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q20 = ans.get(20, "")
        if "bachelor's degree" in q20: scores["Full-Stack / Core Software Engineering"] += 15.0
        elif "mba" in q20: scores["Product Management & UI/UX Design"] += 20.0
        elif "master's degree (ms" in q20: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        elif "ph.d." in q20: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 35.0
        elif "creative portfolio" in q20: scores["Game Development & Interactive Media"] += 20.0

    elif stream == "College - Core Engineering & Physical Sciences":
        scores = {
            "Mechanical & Aerospace Engineering": 5.0,
            "Civil & Sustainable Infrastructure": 5.0,
            "Electronics, VLSI & IoT": 5.0,
            "Chemical & Materials Engineering": 5.0,
            "Advanced Academic Research & Higher Studies (MS / Ph.D.)": 5.0
        }
        q1 = ans.get(1, "")
        if "engines, robots" in q1: scores["Mechanical & Aerospace Engineering"] += 25.0
        elif "massive skyscrapers" in q1: scores["Civil & Sustainable Infrastructure"] += 25.0
        elif "microchips" in q1: scores["Electronics, VLSI & IoT"] += 25.0
        elif "raw materials, chemicals" in q1: scores["Chemical & Materials Engineering"] += 25.0
        elif "mathematical physics" in q1: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q2 = ans.get(2, "")
        if "aerospace hangar" in q2: scores["Mechanical & Aerospace Engineering"] += 20.0
        elif "construction site" in q2: scores["Civil & Sustainable Infrastructure"] += 20.0
        elif "cleanroom" in q2: scores["Electronics, VLSI & IoT"] += 20.0
        elif "heavy industrial processing" in q2: scores["Chemical & Materials Engineering"] += 20.0
        elif "university office" in q2: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q3 = ans.get(3, "")
        if "custom drone" in q3: scores["Mechanical & Aerospace Engineering"] += 20.0
        elif "scale model" in q3: scores["Civil & Sustainable Infrastructure"] += 20.0
        elif "smart-home gadget" in q3: scores["Electronics, VLSI & IoT"] += 20.0
        elif "bio-plastics" in q3: scores["Chemical & Materials Engineering"] += 20.0
        elif "math physics simulations" in q3: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q4 = ans.get(4, "")
        if "gears, motors" in q4: scores["Mechanical & Aerospace Engineering"] += 20.0
        elif "structural load" in q4: scores["Civil & Sustainable Infrastructure"] += 20.0
        elif "multimeter" in q4: scores["Electronics, VLSI & IoT"] += 20.0
        elif "chemical balance" in q4: scores["Chemical & Materials Engineering"] += 20.0
        elif "fundamental equations" in q4: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q5 = ans.get(5, "")
        if "robot or machine" in q5: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "structural analysis" in q5: scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "microcontrollers" in q5: scores["Electronics, VLSI & IoT"] += 25.0
        elif "chemistry and physics" in q5: scores["Chemical & Materials Engineering"] += 15.0
        elif "model complex theoretical" in q5: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q6 = ans.get(6, "")
        if "spacecraft or autonomous" in q6: scores["Mechanical & Aerospace Engineering"] += 20.0
        elif "eco-friendly smart cities" in q6: scores["Civil & Sustainable Infrastructure"] += 20.0
        elif "quantum computing chips" in q6: scores["Electronics, VLSI & IoT"] += 20.0
        elif "clean energy source" in q6: scores["Chemical & Materials Engineering"] += 20.0
        elif "law of physics" in q6: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q7 = ans.get(7, "")
        if "thermodynamics" in q7: scores["Mechanical & Aerospace Engineering"] += 25.0
        elif "statics, concrete" in q7: scores["Civil & Sustainable Infrastructure"] += 25.0
        elif "electromagnetism" in q7: scores["Electronics, VLSI & IoT"] += 25.0
        elif "organic chemistry" in q7: scores["Chemical & Materials Engineering"] += 25.0
        elif "advanced calculus" in q7: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q8 = ans.get(8, "")
        if "3d part and printing" in q8: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "massive blueprint" in q8: scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "soldering components" in q8: scores["Electronics, VLSI & IoT"] += 15.0
        elif "mixing compounds" in q8: scores["Chemical & Materials Engineering"] += 15.0
        elif "pages of equations" in q8: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q9 = ans.get(9, "")
        if "build and hold" in q9: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "massive scale" in q9: scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "microscopic scale" in q9: scores["Electronics, VLSI & IoT"] += 15.0
        elif "molecular scale" in q9: scores["Chemical & Materials Engineering"] += 15.0
        elif "universal scale" in q9: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q10 = ans.get(10, "")
        if "planes don't crash" in q10: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "building falls" in q10: scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "electrical fires" in q10: scores["Electronics, VLSI & IoT"] += 15.0
        elif "chemical spills" in q10: scores["Chemical & Materials Engineering"] += 15.0
        elif "pure scientific discovery" in q10: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q11 = ans.get(11, "")
        if "machinists" in q11: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "architects" in q11: scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "hardware testers" in q11: scores["Electronics, VLSI & IoT"] += 15.0
        elif "biologists, material" in q11: scores["Chemical & Materials Engineering"] += 15.0
        elif "fellow ph.d." in q11: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q12 = ans.get(12, "")
        if "friction" in q12: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "zoning laws" in q12: scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "tiny short circuit" in q12: scores["Electronics, VLSI & IoT"] += 15.0
        elif "chemical batch" in q12: scores["Chemical & Materials Engineering"] += 15.0
        elif "commercial product instead of my own research" in q12: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q13 = ans.get(13, "")
        if "jet engines" in q13: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "mega-engineering" in q13: scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "tear-downs" in q13: scores["Electronics, VLSI & IoT"] += 15.0
        elif "chemistry experiments" in q13: scores["Chemical & Materials Engineering"] += 15.0
        elif "black holes" in q13: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q14 = ans.get(14, "")
        if "wrenches" in q14: scores["Mechanical & Aerospace Engineering"] += 20.0
        elif "surveying equipment" in q14: scores["Civil & Sustainable Infrastructure"] += 20.0
        elif "oscilloscopes" in q14: scores["Electronics, VLSI & IoT"] += 20.0
        elif "beakers" in q14: scores["Chemical & Materials Engineering"] += 20.0
        elif "matlab" in q14: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q15 = ans.get(15, "")
        if "mechanical engineer" in q15: scores["Mechanical & Aerospace Engineering"] += 25.0
        elif "project manager" in q15: scores["Civil & Sustainable Infrastructure"] += 25.0
        elif "hardware architect" in q15: scores["Electronics, VLSI & IoT"] += 25.0
        elif "process engineering" in q15: scores["Chemical & Materials Engineering"] += 25.0
        elif "tenured university professor" in q15: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 35.0
        q16 = ans.get(16, "")
        if "electric engines" in q16: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "greener buildings" in q16: scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "smart-grids" in q16: scores["Electronics, VLSI & IoT"] += 15.0
        elif "carbon-capture" in q16: scores["Chemical & Materials Engineering"] += 15.0
        elif "fundamental physics" in q16: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q17 = ans.get(17, "")
        if "prototype of a physical machine" in q17: scores["Mechanical & Aerospace Engineering"] += 20.0
        elif "massive 3d render" in q17: scores["Civil & Sustainable Infrastructure"] += 20.0
        elif "custom circuit board" in q17: scores["Electronics, VLSI & IoT"] += 20.0
        elif "chemical synthesis" in q17: scores["Chemical & Materials Engineering"] += 20.0
        elif "published academic paper" in q17: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q18 = ans.get(18, "")
        if "physical parts move" in q18: scores["Mechanical & Aerospace Engineering"] += 20.0
        elif "managing massive, complex" in q18: scores["Civil & Sustainable Infrastructure"] += 20.0
        elif "fragile components" in q18: scores["Electronics, VLSI & IoT"] += 20.0
        elif "chemical reactions" in q18: scores["Chemical & Materials Engineering"] += 20.0
        elif "abstract theoretical concepts" in q18: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q19 = ans.get(19, "")
        if "aerodynamics" in q19: scores["Mechanical & Aerospace Engineering"] += 15.0
        elif "city infrastructure" in q19: scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "embedded software" in q19: scores["Electronics, VLSI & IoT"] += 15.0
        elif "battery chemistry" in q19: scores["Chemical & Materials Engineering"] += 15.0
        elif "academic physics research" in q19: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q20 = ans.get(20, "")
        if "core engineering industry" in q20: scores["Mechanical & Aerospace Engineering"] += 15.0; scores["Civil & Sustainable Infrastructure"] += 15.0
        elif "mba" in q20: scores["Civil & Sustainable Infrastructure"] += 10.0; scores["Chemical & Materials Engineering"] += 10.0
        elif "quick master's" in q20: scores["Electronics, VLSI & IoT"] += 20.0; scores["Mechanical & Aerospace Engineering"] += 10.0
        elif "ph.d." in q20: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 35.0
        elif "learn everything" in q20: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 10.0

    elif stream == "College - Business, Finance & Commerce":
        scores = {
            "Investment Banking & Corporate Finance": 5.0,
            "Growth Marketing & Brand Strategy": 5.0,
            "Operations & Supply Chain Management": 5.0,
            "Entrepreneurship & Venture Capital": 5.0,
            "Advanced Academic Research & Higher Studies (MBA / Ph.D.)": 5.0
        }
        q1 = ans.get(1, "")
        if "financial models" in q1: scores["Investment Banking & Corporate Finance"] += 25.0
        elif "viral marketing" in q1: scores["Growth Marketing & Brand Strategy"] += 25.0
        elif "supply chains" in q1: scores["Operations & Supply Chain Management"] += 25.0
        elif "startup" in q1: scores["Entrepreneurship & Venture Capital"] += 25.0
        elif "macroeconomic research" in q1: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 30.0
        q2 = ans.get(2, "")
        if "trading floor" in q2: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "advertising agency" in q2: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "corporate headquarters" in q2: scores["Operations & Supply Chain Management"] += 20.0
        elif "startup incubator" in q2: scores["Entrepreneurship & Venture Capital"] += 20.0
        elif "think tank" in q2: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q3 = ans.get(3, "")
        if "profit margins" in q3: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "go-to-market" in q3: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "manufacture and ship" in q3: scores["Operations & Supply Chain Management"] += 20.0
        elif "seed funding" in q3: scores["Entrepreneurship & Venture Capital"] += 20.0
        elif "global market trends" in q3: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q4 = ans.get(4, "")
        if "meticulously" in q4: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "creative risks" in q4: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "predictable, efficient" in q4: scores["Operations & Supply Chain Management"] += 20.0
        elif "extreme risk" in q4: scores["Entrepreneurship & Venture Capital"] += 20.0
        elif "risk models theoretically" in q4: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q5 = ans.get(5, "")
        if "balance sheets" in q5: scores["Investment Banking & Corporate Finance"] += 25.0
        elif "consumer behavior metrics" in q5: scores["Growth Marketing & Brand Strategy"] += 25.0
        elif "inventory levels" in q5: scores["Operations & Supply Chain Management"] += 25.0
        elif "pitch deck projections" in q5: scores["Entrepreneurship & Venture Capital"] += 25.0
        elif "gdp, inflation" in q5: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 30.0
        q6 = ans.get(6, "")
        if "cfos, bankers" in q6: scores["Investment Banking & Corporate Finance"] += 15.0
        elif "creative directors" in q6: scores["Growth Marketing & Brand Strategy"] += 15.0
        elif "suppliers, warehouse" in q6: scores["Operations & Supply Chain Management"] += 15.0
        elif "angel investors" in q6: scores["Entrepreneurship & Venture Capital"] += 15.0
        elif "researchers, professors" in q6: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q7 = ans.get(7, "")
        if "number-crunching" in q7: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "brainstorming creative ideas" in q7: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "organizing chaos" in q7: scores["Operations & Supply Chain Management"] += 20.0
        elif "leading the vision" in q7: scores["Entrepreneurship & Venture Capital"] += 20.0
        elif "evidence-based research" in q7: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q8 = ans.get(8, "")
        if "wall street hours" in q8: scores["Investment Banking & Corporate Finance"] += 15.0
        elif "major ad campaign" in q8: scores["Growth Marketing & Brand Strategy"] += 15.0
        elif "steady, predictable" in q8: scores["Operations & Supply Chain Management"] += 15.0
        elif "never truly clock out" in q8: scores["Entrepreneurship & Venture Capital"] += 15.0
        elif "self-paced research" in q8: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q9 = ans.get(9, "")
        if "math error ruining" in q9: scores["Investment Banking & Corporate Finance"] += 15.0
        elif "boring marketing" in q9: scores["Growth Marketing & Brand Strategy"] += 15.0
        elif "supply chain bottleneck" in q9: scores["Operations & Supply Chain Management"] += 15.0
        elif "zero equity" in q9: scores["Entrepreneurship & Venture Capital"] += 15.0
        elif "quarterly profits instead of long-term" in q9: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q10 = ans.get(10, "")
        if "bloomberg terminals" in q10: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "google analytics" in q10: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "erp" in q10: scores["Operations & Supply Chain Management"] += 20.0
        elif "pitch decks" in q10: scores["Entrepreneurship & Venture Capital"] += 20.0
        elif "stata, r, python" in q10: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q11 = ans.get(11, "")
        if "corporate deals" in q11: scores["Investment Banking & Corporate Finance"] += 15.0
        elif "consumer psychology" in q11: scores["Growth Marketing & Brand Strategy"] += 15.0
        elif "volume and distribution" in q11: scores["Operations & Supply Chain Management"] += 15.0
        elif "selling the vision" in q11: scores["Entrepreneurship & Venture Capital"] += 15.0
        elif "analyze consumer demand academically" in q11: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q12 = ans.get(12, "")
        if "stock market movements" in q12: scores["Investment Banking & Corporate Finance"] += 15.0
        elif "pop culture trends" in q12: scores["Growth Marketing & Brand Strategy"] += 15.0
        elif "global trade agreements" in q12: scores["Operations & Supply Chain Management"] += 15.0
        elif "unicorn valuations" in q12: scores["Entrepreneurship & Venture Capital"] += 15.0
        elif "the economist" in q12: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q13 = ans.get(13, "")
        if "index funds" in q13: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "facebook/google ads" in q13: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "automate a business" in q13: scores["Operations & Supply Chain Management"] += 20.0
        elif "seed money" in q13: scores["Entrepreneurship & Venture Capital"] += 20.0
        elif "academic study" in q13: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q14 = ans.get(14, "")
        if "financial model" in q14: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "a/b test" in q14: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "process flowchart" in q14: scores["Operations & Supply Chain Management"] += 20.0
        elif "pivot the business" in q14: scores["Entrepreneurship & Venture Capital"] += 20.0
        elif "peer-reviewed literature" in q14: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q15 = ans.get(15, "")
        if "managing director" in q15: scores["Investment Banking & Corporate Finance"] += 25.0
        elif "cmo" in q15: scores["Growth Marketing & Brand Strategy"] += 25.0
        elif "coo" in q15: scores["Operations & Supply Chain Management"] += 25.0
        elif "founder" in q15: scores["Entrepreneurship & Venture Capital"] += 25.0
        elif "professor of economics" in q15: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 35.0
        q16 = ans.get(16, "")
        if "shareholder value" in q16: scores["Investment Banking & Corporate Finance"] += 15.0
        elif "positive, trustworthy" in q16: scores["Growth Marketing & Brand Strategy"] += 15.0
        elif "fair labor" in q16: scores["Operations & Supply Chain Management"] += 15.0
        elif "disrupts the industry" in q16: scores["Entrepreneurship & Venture Capital"] += 15.0
        elif "systemic impact of corporate" in q16: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q17 = ans.get(17, "")
        if "financial valuation report" in q17: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "viral" in q17: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "reduction in operational waste" in q17: scores["Operations & Supply Chain Management"] += 20.0
        elif "venture capital" in q17: scores["Entrepreneurship & Venture Capital"] += 20.0
        elif "macroeconomic policy" in q17: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 30.0
        q18 = ans.get(18, "")
        if "extreme wealth" in q18: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "creative impact" in q18: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "perfect order" in q18: scores["Operations & Supply Chain Management"] += 20.0
        elif "from scratch" in q18: scores["Entrepreneurship & Venture Capital"] += 20.0
        elif "advancing human knowledge" in q18: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 30.0
        q19 = ans.get(19, "")
        if "stock price" in q19: scores["Investment Banking & Corporate Finance"] += 15.0
        elif "minimalist marketing" in q19: scores["Growth Marketing & Brand Strategy"] += 15.0
        elif "incredible logistics" in q19: scores["Operations & Supply Chain Management"] += 15.0
        elif "niche feature they missed" in q19: scores["Entrepreneurship & Venture Capital"] += 15.0
        elif "broader economic implications" in q19: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 25.0
        q20 = ans.get(20, "")
        if "cfa or cpa" in q20: scores["Investment Banking & Corporate Finance"] += 20.0
        elif "digital marketing" in q20: scores["Growth Marketing & Brand Strategy"] += 20.0
        elif "mba" in q20: scores["Operations & Supply Chain Management"] += 20.0
        elif "drop out" in q20: scores["Entrepreneurship & Venture Capital"] += 25.0
        elif "ph.d. in economics" in q20: scores["Advanced Academic Research & Higher Studies (MBA / Ph.D.)"] += 35.0

    elif stream == "College - Arts, Humanities & Social Sciences":
        scores = {
            "Psychology & Behavioral Science": 5.0,
            "Journalism & Mass Media": 5.0,
            "Sociology & Social Work": 5.0,
            "Literature, History & Editorial": 5.0,
            "Advanced Academic Research & Higher Studies (MS / Ph.D.)": 5.0
        }
        q1 = ans.get(1, "")
        if "human mind" in q1: scores["Psychology & Behavioral Science"] += 25.0
        elif "reporting the truth" in q1: scores["Journalism & Mass Media"] += 25.0
        elif "systemic inequality" in q1: scores["Sociology & Social Work"] += 25.0
        elif "classic literature" in q1: scores["Literature, History & Editorial"] += 25.0
        elif "theoretical research in humanities" in q1: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q2 = ans.get(2, "")
        if "therapy office" in q2: scores["Psychology & Behavioral Science"] += 20.0
        elif "newsroom" in q2: scores["Journalism & Mass Media"] += 20.0
        elif "ngos" in q2: scores["Sociology & Social Work"] += 20.0
        elif "publishing house" in q2: scores["Literature, History & Editorial"] += 20.0
        elif "university classroom" in q2: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q3 = ans.get(3, "")
        if "heal from mental health" in q3: scores["Psychology & Behavioral Science"] += 20.0
        elif "exposing corruption" in q3: scores["Journalism & Mass Media"] += 20.0
        elif "fighting for marginalized" in q3: scores["Sociology & Social Work"] += 20.0
        elif "writing a novel" in q3: scores["Literature, History & Editorial"] += 20.0
        elif "sociological or psychological research" in q3: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q4 = ans.get(4, "")
        if "empathetic, one-on-one" in q4: scores["Psychology & Behavioral Science"] += 20.0
        elif "tough, direct questions" in q4: scores["Journalism & Mass Media"] += 20.0
        elif "advocating for them" in q4: scores["Sociology & Social Work"] += 20.0
        elif "text and history rather than face-to-face" in q4: scores["Literature, History & Editorial"] += 20.0
        elif "lectures and discussing academic theories" in q4: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q5 = ans.get(5, "")
        if "brain development" in q5: scores["Psychology & Behavioral Science"] += 20.0
        elif "investigative journalism" in q5: scores["Journalism & Mass Media"] += 20.0
        elif "social justice" in q5: scores["Sociology & Social Work"] += 20.0
        elif "classic literature" in q5: scores["Literature, History & Editorial"] += 20.0
        elif "peer-reviewed academic journals" in q5: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q6 = ans.get(6, "")
        if "counsel them" in q6: scores["Psychology & Behavioral Science"] += 15.0
        elif "document it objectively" in q6: scores["Journalism & Mass Media"] += 15.0
        elif "provide systemic resources" in q6: scores["Sociology & Social Work"] += 15.0
        elif "creative or editorial writing" in q6: scores["Literature, History & Editorial"] += 15.0
        elif "academic or theoretical lens" in q6: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q7 = ans.get(7, "")
        if "extreme empathy" in q7: scores["Psychology & Behavioral Science"] += 20.0
        elif "writing under pressure" in q7: scores["Journalism & Mass Media"] += 20.0
        elif "resilience in the face of societal struggles" in q7: scores["Sociology & Social Work"] += 20.0
        elif "appreciation for language" in q7: scores["Literature, History & Editorial"] += 20.0
        elif "rigorous academic discipline" in q7: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q8 = ans.get(8, "")
        if "client who refuses" in q8: scores["Psychology & Behavioral Science"] += 15.0
        elif "news story breaking" in q8: scores["Journalism & Mass Media"] += 15.0
        elif "bureaucratic red tape" in q8: scores["Sociology & Social Work"] += 15.0
        elif "writers' block" in q8: scores["Literature, History & Editorial"] += 15.0
        elif "teach basic classes instead of doing deep research" in q8: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q9 = ans.get(9, "")
        if "dsm-5" in q9: scores["Psychology & Behavioral Science"] += 20.0
        elif "microphones" in q9: scores["Journalism & Mass Media"] += 20.0
        elif "community resource directories" in q9: scores["Sociology & Social Work"] += 20.0
        elif "manuscripts" in q9: scores["Literature, History & Editorial"] += 20.0
        elif "academic citations" in q9: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q10 = ans.get(10, "")
        if "clinical notes" in q10: scores["Psychology & Behavioral Science"] += 15.0
        elif "punchy, fact-driven" in q10: scores["Journalism & Mass Media"] += 15.0
        elif "grants, policy" in q10: scores["Sociology & Social Work"] += 15.0
        elif "long-form creative" in q10: scores["Literature, History & Editorial"] += 15.0
        elif "formally cited academic dissertations" in q10: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q11 = ans.get(11, "")
        if "patients, clients" in q11: scores["Psychology & Behavioral Science"] += 15.0
        elif "editors, sources" in q11: scores["Journalism & Mass Media"] += 15.0
        elif "vulnerable populations" in q11: scores["Sociology & Social Work"] += 15.0
        elif "authors, historians" in q11: scores["Literature, History & Editorial"] += 15.0
        elif "fellow ph.d. candidates" in q11: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q12 = ans.get(12, "")
        if "mental health treatments" in q12: scores["Psychology & Behavioral Science"] += 15.0
        elif "media cycle" in q12: scores["Journalism & Mass Media"] += 15.0
        elif "housing, poverty" in q12: scores["Sociology & Social Work"] += 15.0
        elif "cultural critiques" in q12: scores["Literature, History & Editorial"] += 15.0
        elif "academic discoveries" in q12: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q13 = ans.get(13, "")
        if "self-improvement or psychology" in q13: scores["Psychology & Behavioral Science"] += 15.0
        elif "podcast" in q13: scores["Journalism & Mass Media"] += 15.0
        elif "volunteer" in q13: scores["Sociology & Social Work"] += 15.0
        elif "museum" in q13: scores["Literature, History & Editorial"] += 15.0
        elif "academic research paper" in q13: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q14 = ans.get(14, "")
        if "mental health and trauma" in q14: scores["Psychology & Behavioral Science"] += 20.0
        elif "broadcast their reality" in q14: scores["Journalism & Mass Media"] += 20.0
        elif "directly provide food" in q14: scores["Sociology & Social Work"] += 20.0
        elif "historical eras" in q14: scores["Literature, History & Editorial"] += 20.0
        elif "systemic, sociological root causes" in q14: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q15 = ans.get(15, "")
        if "clinical psychologist" in q15: scores["Psychology & Behavioral Science"] += 25.0
        elif "investigative journalist" in q15: scores["Journalism & Mass Media"] += 25.0
        elif "social worker" in q15: scores["Sociology & Social Work"] += 25.0
        elif "published author" in q15: scores["Literature, History & Editorial"] += 25.0
        elif "tenured professor" in q15: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 35.0
        q16 = ans.get(16, "")
        if "neutral blank slate" in q16: scores["Psychology & Behavioral Science"] += 15.0
        elif "unbiased to report" in q16: scores["Journalism & Mass Media"] += 15.0
        elif "actively advocate" in q16: scores["Sociology & Social Work"] += 15.0
        elif "subjective" in q16: scores["Literature, History & Editorial"] += 15.0
        elif "peer-reviewed evidence" in q16: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q17 = ans.get(17, "")
        if "patient's recovery" in q17: scores["Psychology & Behavioral Science"] += 20.0
        elif "viral documentary" in q17: scores["Journalism & Mass Media"] += 20.0
        elif "lowered homelessness" in q17: scores["Sociology & Social Work"] += 20.0
        elif "historical exhibition" in q17: scores["Literature, History & Editorial"] += 20.0
        elif "defended ph.d." in q17: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q18 = ans.get(18, "")
        if "helping people heal" in q18: scores["Psychology & Behavioral Science"] += 20.0
        elif "holding power accountable" in q18: scores["Journalism & Mass Media"] += 20.0
        elif "social justice" in q18: scores["Sociology & Social Work"] += 20.0
        elif "preserving human culture" in q18: scores["Literature, History & Editorial"] += 20.0
        elif "theoretical knowledge" in q18: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 30.0
        q19 = ans.get(19, "")
        if "psychological motivations" in q19: scores["Psychology & Behavioral Science"] += 15.0
        elif "propaganda" in q19: scores["Journalism & Mass Media"] += 15.0
        elif "class struggles" in q19: scores["Sociology & Social Work"] += 15.0
        elif "historical timelines" in q19: scores["Literature, History & Editorial"] += 15.0
        elif "academic consensus" in q19: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 25.0
        q20 = ans.get(20, "")
        if "psy.d" in q20: scores["Psychology & Behavioral Science"] += 25.0
        elif "media or journalism immediately" in q20: scores["Journalism & Mass Media"] += 20.0
        elif "msw" in q20: scores["Sociology & Social Work"] += 25.0
        elif "mfa in creative writing" in q20: scores["Literature, History & Editorial"] += 25.0
        elif "ph.d. for a career in academia" in q20: scores["Advanced Academic Research & Higher Studies (MS / Ph.D.)"] += 35.0

    elif stream == "College - Law, Policy & International Relations":
        scores = {
            "Corporate & Commercial Law": 5.0,
            "Criminal & Litigation Law": 5.0,
            "Public Policy & Governance": 5.0,
            "International Relations & Diplomacy": 5.0,
            "Advanced Academic Research & Higher Studies (LL.M / Ph.D.)": 5.0
        }
        q1 = ans.get(1, "")
        if "corporate mergers" in q1: scores["Corporate & Commercial Law"] += 25.0
        elif "courtroom" in q1: scores["Criminal & Litigation Law"] += 25.0
        elif "writing legislation" in q1: scores["Public Policy & Governance"] += 25.0
        elif "cross-border" in q1: scores["International Relations & Diplomacy"] += 25.0
        elif "studying legal theory" in q1: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 30.0
        q2 = ans.get(2, "")
        if "corporate law firm" in q2: scores["Corporate & Commercial Law"] += 20.0
        elif "public defender" in q2: scores["Criminal & Litigation Law"] += 20.0
        elif "government office" in q2: scores["Public Policy & Governance"] += 20.0
        elif "embassy" in q2: scores["International Relations & Diplomacy"] += 20.0
        elif "university office" in q2: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q3 = ans.get(3, "")
        if "loopholes" in q3: scores["Corporate & Commercial Law"] += 20.0
        elif "narrative for the jury" in q3: scores["Criminal & Litigation Law"] += 20.0
        elif "future public policy" in q3: scores["Public Policy & Governance"] += 20.0
        elif "foreign relations" in q3: scores["International Relations & Diplomacy"] += 20.0
        elif "supreme court precedents" in q3: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q4 = ans.get(4, "")
        if "ceos and executives" in q4: scores["Corporate & Commercial Law"] += 20.0
        elif "cross-examining witnesses" in q4: scores["Criminal & Litigation Law"] += 20.0
        elif "debating with politicians" in q4: scores["Public Policy & Governance"] += 20.0
        elif "diplomatically negotiating" in q4: scores["International Relations & Diplomacy"] += 20.0
        elif "debating with fellow academics" in q4: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q5 = ans.get(5, "")
        if "contracts, compliance codes" in q5: scores["Corporate & Commercial Law"] += 20.0
        elif "police reports" in q5: scores["Criminal & Litigation Law"] += 20.0
        elif "policy briefs" in q5: scores["Public Policy & Governance"] += 20.0
        elif "international treaties" in q5: scores["International Relations & Diplomacy"] += 20.0
        elif "peer-reviewed legal journals" in q5: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 30.0
        q6 = ans.get(6, "")
        if "negotiate settlements" in q6: scores["Corporate & Commercial Law"] += 15.0
        elif "courtroom confrontation" in q6: scores["Criminal & Litigation Law"] += 15.0
        elif "legislative compromise" in q6: scores["Public Policy & Governance"] += 15.0
        elif "tact, cultural understanding" in q6: scores["International Relations & Diplomacy"] += 15.0
        elif "objectively through established" in q6: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q7 = ans.get(7, "")
        if "contract drafting" in q7: scores["Corporate & Commercial Law"] += 20.0
        elif "persuasive argumentation" in q7: scores["Criminal & Litigation Law"] += 20.0
        elif "drafting policy" in q7: scores["Public Policy & Governance"] += 20.0
        elif "cultural adaptability" in q7: scores["International Relations & Diplomacy"] += 20.0
        elif "rigorous academic discipline" in q7: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q8 = ans.get(8, "")
        if "regulatory compliance issue" in q8: scores["Corporate & Commercial Law"] += 15.0
        elif "losing a trial" in q8: scores["Criminal & Litigation Law"] += 15.0
        elif "partisan political gridlock" in q8: scores["Public Policy & Governance"] += 15.0
        elif "cultural misunderstandings" in q8: scores["International Relations & Diplomacy"] += 15.0
        elif "routine paperwork instead of deep" in q8: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q9 = ans.get(9, "")
        if "corporate databases" in q9: scores["Corporate & Commercial Law"] += 20.0
        elif "penal code" in q9: scores["Criminal & Litigation Law"] += 20.0
        elif "public polling data" in q9: scores["Public Policy & Governance"] += 20.0
        elif "passports" in q9: scores["International Relations & Diplomacy"] += 20.0
        elif "academic citations" in q9: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q10 = ans.get(10, "")
        if "corporate board meetings" in q10: scores["Corporate & Commercial Law"] += 15.0
        elif "command a courtroom" in q10: scores["Criminal & Litigation Law"] += 15.0
        elif "debating policy on a panel" in q10: scores["Public Policy & Governance"] += 15.0
        elif "every word in diplomacy matters" in q10: scores["International Relations & Diplomacy"] += 15.0
        elif "formal academic lectures" in q10: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q11 = ans.get(11, "")
        if "corporate clients" in q11: scores["Corporate & Commercial Law"] += 15.0
        elif "judges, juries" in q11: scores["Criminal & Litigation Law"] += 15.0
        elif "senators, mayors" in q11: scores["Public Policy & Governance"] += 15.0
        elif "ambassadors" in q11: scores["International Relations & Diplomacy"] += 15.0
        elif "law professors" in q11: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q12 = ans.get(12, "")
        if "corporate acquisitions" in q12: scores["Corporate & Commercial Law"] += 15.0
        elif "criminal trials" in q12: scores["Criminal & Litigation Law"] += 15.0
        elif "elections, domestic" in q12: scores["Public Policy & Governance"] += 15.0
        elif "global conflicts" in q12: scores["International Relations & Diplomacy"] += 15.0
        elif "supreme court rulings" in q12: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q13 = ans.get(13, "")
        if "hostile takeover" in q13: scores["Corporate & Commercial Law"] += 15.0
        elif "courtroom drama" in q13: scores["Criminal & Litigation Law"] += 15.0
        elif "political campaign" in q13: scores["Public Policy & Governance"] += 15.0
        elif "foreign culture" in q13: scores["International Relations & Diplomacy"] += 15.0
        elif "academic legal paper" in q13: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q14 = ans.get(14, "")
        if "corporate compliance" in q14: scores["Corporate & Commercial Law"] += 20.0
        elif "prosecute companies" in q14: scores["Criminal & Litigation Law"] += 20.0
        elif "federal policies" in q14: scores["Public Policy & Governance"] += 20.0
        elif "paris agreement" in q14: scores["International Relations & Diplomacy"] += 20.0
        elif "legal constitutionality" in q14: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 30.0
        q15 = ans.get(15, "")
        if "fortune 500" in q15: scores["Corporate & Commercial Law"] += 25.0
        elif "lead prosecutor" in q15: scores["Criminal & Litigation Law"] += 25.0
        elif "senator" in q15: scores["Public Policy & Governance"] += 25.0
        elif "ambassador" in q15: scores["International Relations & Diplomacy"] += 25.0
        elif "tenured law professor" in q15: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 35.0
        q16 = ans.get(16, "")
        if "secure business and trade" in q16: scores["Corporate & Commercial Law"] += 15.0
        elif "adversarial arena" in q16: scores["Criminal & Litigation Law"] += 15.0
        elif "constantly be updated" in q16: scores["Public Policy & Governance"] += 15.0
        elif "human rights standards" in q16: scores["International Relations & Diplomacy"] += 15.0
        elif "theoretical construct" in q16: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q17 = ans.get(17, "")
        if "merger agreement" in q17: scores["Corporate & Commercial Law"] += 20.0
        elif "not guilty" in q17: scores["Criminal & Litigation Law"] += 20.0
        elif "legislation that successfully" in q17: scores["Public Policy & Governance"] += 20.0
        elif "peace or trade treaty" in q17: scores["International Relations & Diplomacy"] += 20.0
        elif "yale law journal" in q17: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 30.0
        q18 = ans.get(18, "")
        if "protecting corporate assets" in q18: scores["Corporate & Commercial Law"] += 20.0
        elif "courtroom victories" in q18: scores["Criminal & Litigation Law"] += 20.0
        elif "government policy" in q18: scores["Public Policy & Governance"] += 20.0
        elif "cultural divides" in q18: scores["International Relations & Diplomacy"] += 20.0
        elif "jurisprudence" in q18: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 30.0
        q19 = ans.get(19, "")
        if "legal liability" in q19: scores["Corporate & Commercial Law"] += 15.0
        elif "trial will play out" in q19: scores["Criminal & Litigation Law"] += 15.0
        elif "new laws need to be written" in q19: scores["Public Policy & Governance"] += 15.0
        elif "global stage" in q19: scores["International Relations & Diplomacy"] += 15.0
        elif "constitutional law principles" in q19: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 25.0
        q20 = ans.get(20, "")
        if "join a corporate firm" in q20: scores["Corporate & Commercial Law"] += 25.0
        elif "into the courtroom" in q20: scores["Criminal & Litigation Law"] += 25.0
        elif "public policy" in q20: scores["Public Policy & Governance"] += 25.0
        elif "global affairs" in q20: scores["International Relations & Diplomacy"] += 25.0
        elif "ll.m" in q20: scores["Advanced Academic Research & Higher Studies (LL.M / Ph.D.)"] += 35.0

    elif stream == "College - Creative Arts, Architecture & Design":
        scores = {
            "Architecture & Spatial Design": 5.0,
            "Fine Arts & Illustration": 5.0,
            "Animation & Game Design": 5.0,
            "Industrial & Product Design": 5.0,
            "Advanced Academic Research & Higher Studies (MFA / Ph.D.)": 5.0
        }
        q1 = ans.get(1, "")
        if "physical building" in q1: scores["Architecture & Spatial Design"] += 25.0
        elif "visual art" in q1: scores["Fine Arts & Illustration"] += 25.0
        elif "animation and game" in q1: scores["Animation & Game Design"] += 25.0
        elif "physical products" in q1: scores["Industrial & Product Design"] += 25.0
        elif "academic design philosophies" in q1: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 30.0
        q2 = ans.get(2, "")
        if "architectural firm" in q2: scores["Architecture & Spatial Design"] += 20.0
        elif "art studio" in q2: scores["Fine Arts & Illustration"] += 20.0
        elif "unity or maya" in q2: scores["Animation & Game Design"] += 20.0
        elif "industrial design workshop" in q2: scores["Industrial & Product Design"] += 20.0
        elif "museum curation backroom" in q2: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q3 = ans.get(3, "")
        if "spatial flow" in q3: scores["Architecture & Spatial Design"] += 20.0
        elif "color, emotion" in q3: scores["Fine Arts & Illustration"] += 20.0
        elif "character would move" in q3: scores["Animation & Game Design"] += 20.0
        elif "human hand would hold" in q3: scores["Industrial & Product Design"] += 20.0
        elif "cultural and historical significance" in q3: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q4 = ans.get(4, "")
        if "blueprints" in q4: scores["Architecture & Spatial Design"] += 20.0
        elif "gallery" in q4: scores["Fine Arts & Illustration"] += 20.0
        elif "programmers and sound designers" in q4: scores["Animation & Game Design"] += 20.0
        elif "prototype" in q4: scores["Industrial & Product Design"] += 20.0
        elif "art theory with fellow academics" in q4: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q5 = ans.get(5, "")
        if "autocad" in q5: scores["Architecture & Spatial Design"] += 25.0
        elif "brushes, charcoal" in q5: scores["Fine Arts & Illustration"] += 25.0
        elif "unreal engine" in q5: scores["Animation & Game Design"] += 25.0
        elif "solidworks" in q5: scores["Industrial & Product Design"] += 25.0
        elif "art history journals" in q5: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 30.0
        q6 = ans.get(6, "")
        if "strict physics" in q6: scores["Architecture & Spatial Design"] += 15.0
        elif "pure artistic expression" in q6: scores["Fine Arts & Illustration"] += 15.0
        elif "frame rates" in q6: scores["Animation & Game Design"] += 15.0
        elif "mass production" in q6: scores["Industrial & Product Design"] += 15.0
        elif "historical artists navigated" in q6: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q7 = ans.get(7, "")
        if "spatial awareness" in q7: scores["Architecture & Spatial Design"] += 20.0
        elif "mastery of color" in q7: scores["Fine Arts & Illustration"] += 20.0
        elif "digital timing" in q7: scores["Animation & Game Design"] += 20.0
        elif "ergonomics" in q7: scores["Industrial & Product Design"] += 20.0
        elif "rigorous academic discipline" in q7: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q8 = ans.get(8, "")
        if "zoning board" in q8: scores["Architecture & Spatial Design"] += 15.0
        elif "match their couch" in q8: scores["Fine Arts & Illustration"] += 15.0
        elif "game engine crashing" in q8: scores["Animation & Game Design"] += 15.0
        elif "cheap, breakable plastic" in q8: scores["Industrial & Product Design"] += 15.0
        elif "instead of deep research" in q8: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q9 = ans.get(9, "")
        if "sustainable, eco-friendly modern home" in q9: scores["Architecture & Spatial Design"] += 20.0
        elif "painting a mural" in q9: scores["Fine Arts & Illustration"] += 20.0
        elif "combat sequence" in q9: scores["Animation & Game Design"] += 20.0
        elif "electric car" in q9: scores["Industrial & Product Design"] += 20.0
        elif "evolution of renaissance art" in q9: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 30.0
        q10 = ans.get(10, "")
        if "safe and functional first" in q10: scores["Architecture & Spatial Design"] += 15.0
        elif "aesthetics are everything" in q10: scores["Fine Arts & Illustration"] += 15.0
        elif "60 frames per second" in q10: scores["Animation & Game Design"] += 15.0
        elif "uncomfortable, it's garbage" in q10: scores["Industrial & Product Design"] += 15.0
        elif "philosophical definitions" in q10: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q11 = ans.get(11, "")
        if "civil engineers" in q11: scores["Architecture & Spatial Design"] += 15.0
        elif "fellow painters" in q11: scores["Fine Arts & Illustration"] += 15.0
        elif "vfx artists" in q11: scores["Animation & Game Design"] += 15.0
        elif "manufacturing engineers" in q11: scores["Industrial & Product Design"] += 15.0
        elif "art history professors" in q11: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q12 = ans.get(12, "")
        if "architectural digest" in q12: scores["Architecture & Spatial Design"] += 15.0
        elif "art station" in q12: scores["Fine Arts & Illustration"] += 15.0
        elif "pixar" in q12: scores["Animation & Game Design"] += 15.0
        elif "industrial design blogs" in q12: scores["Industrial & Product Design"] += 15.0
        elif "academic journals on aesthetics" in q12: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q13 = ans.get(13, "")
        if "skyscrapers and urban flow" in q13: scores["Architecture & Spatial Design"] += 15.0
        elif "sketch or paint" in q13: scores["Fine Arts & Illustration"] += 15.0
        elif "animated film" in q13: scores["Animation & Game Design"] += 15.0
        elif "household appliance" in q13: scores["Industrial & Product Design"] += 15.0
        elif "academic paper on art theory" in q13: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q14 = ans.get(14, "")
        if "building codes" in q14: scores["Architecture & Spatial Design"] += 20.0
        elif "abstract shapes" in q14: scores["Fine Arts & Illustration"] += 20.0
        elif "animation timeline" in q14: scores["Animation & Game Design"] += 20.0
        elif "physical prototype out of clay" in q14: scores["Industrial & Product Design"] += 20.0
        elif "peer-reviewed literature" in q14: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q15 = ans.get(15, "")
        if "lead architect" in q15: scores["Architecture & Spatial Design"] += 25.0
        elif "fine artist" in q15: scores["Fine Arts & Illustration"] += 25.0
        elif "art director at a aaa" in q15: scores["Animation & Game Design"] += 25.0
        elif "senior industrial designer" in q15: scores["Industrial & Product Design"] += 25.0
        elif "museum chief curator" in q15: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 35.0
        q16 = ans.get(16, "")
        if "physical structure is what matters" in q16: scores["Architecture & Spatial Design"] += 15.0
        elif "traditional mediums" in q16: scores["Fine Arts & Illustration"] += 15.0
        elif "3d software" in q16: scores["Animation & Game Design"] += 15.0
        elif "tangible physical object" in q16: scores["Industrial & Product Design"] += 15.0
        elif "theoretical impact of technology" in q16: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q17 = ans.get(17, "")
        if "scale model of a new library" in q17: scores["Architecture & Spatial Design"] += 20.0
        elif "gallery exhibition" in q17: scores["Fine Arts & Illustration"] += 20.0
        elif "demo of a beautifully animated" in q17: scores["Animation & Game Design"] += 20.0
        elif "ergonomic prototype" in q17: scores["Industrial & Product Design"] += 20.0
        elif "mfa/ph.d. dissertation" in q17: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 30.0
        q18 = ans.get(18, "")
        if "define human cities" in q18: scores["Architecture & Spatial Design"] += 20.0
        elif "inner soul" in q18: scores["Fine Arts & Illustration"] += 20.0
        elif "immersive, interactive digital" in q18: scores["Animation & Game Design"] += 20.0
        elif "useful objects that make daily life better" in q18: scores["Industrial & Product Design"] += 20.0
        elif "art history and design theory" in q18: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 30.0
        q19 = ans.get(19, "")
        if "spatial design of the room" in q19: scores["Architecture & Spatial Design"] += 15.0
        elif "visual emotional impact" in q19: scores["Fine Arts & Illustration"] += 15.0
        elif "3d model it for a game" in q19: scores["Animation & Game Design"] += 15.0
        elif "ergonomics, the materials used" in q19: scores["Industrial & Product Design"] += 15.0
        elif "historical bauhaus" in q19: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 25.0
        q20 = ans.get(20, "")
        if "b.arch/m.arch" in q20: scores["Architecture & Spatial Design"] += 25.0
        elif "exhibiting my art" in q20: scores["Fine Arts & Illustration"] += 25.0
        elif "game design and enter the industry" in q20: scores["Animation & Game Design"] += 25.0
        elif "degree in industrial design" in q20: scores["Industrial & Product Design"] += 25.0
        elif "mfa for academia" in q20: scores["Advanced Academic Research & Higher Studies (MFA / Ph.D.)"] += 35.0

    else:
        scores = { "Awaiting Stream Data": 0.0 }

    sorted_matches = sorted(
        [{"title": k, "match": round(max(0.0, min(v, 98.5)), 1)} for k, v in scores.items()],
        key=lambda x: x["match"],
        reverse=True
    )

    return {
        "status": "success",
        "stream": stream,
        "optimal_vector": sorted_matches[0],
        "evaluated_vectors": sorted_matches
    }