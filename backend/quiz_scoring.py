import re
from typing import Dict, List, Mapping, Tuple, TypedDict


class CareerMatch(TypedDict):
    title: str
    match: float


CAREER_TRACKS: Dict[str, Dict[str, str]] = {
    "Science (PCB)": {
        "Medicine (MBBS/BDS)": "clinical",
        "Veterinary Science": "veterinary",
        "Biotechnology & Genetics Research": "biotechnology",
        "Pharmacy & Pharmaceutical Sciences": "pharmacy",
        "Allied Health Professions (Physio/Nutrition)": "allied_health",
        "Public Health & Healthcare Management": "public_health",
        "Microbiology & Immunology": "microbiology",
        "Psychology & Neuroscience": "psychology",
        "Environmental Science & Conservation": "environmental_science",
    },
    "Science (PCM)": {
        "Software Engineering & Computer Science": "software",
        "Data Science & Artificial Intelligence": "data_science",
        "Mechanical & Aerospace Engineering": "mechanical",
        "Electronics, VLSI & Robotics": "electronics",
        "Architecture & Design": "architecture",
        "Civil & Infrastructure Engineering": "civil",
        "Pure Mathematics & Quantitative Research": "mathematics",
        "Chemical & Materials Engineering": "chemical_materials",
    },
    "Commerce": {
        "Chartered Accountancy (CA) & Corporate Finance": "accounting",
        "Investment Banking & Equity Research": "investment",
        "Corporate Law & Legal Consulting": "corporate_law",
        "Marketing, Advertising & Brand Management": "marketing",
        "Entrepreneurship & Business Strategy": "entrepreneurship",
        "Actuarial Science & Risk Management": "actuarial",
        "Human Resources & Organizational Behavior": "human_resources",
    },
    "Arts / Humanities": {
        "Psychology & Counseling": "psychology",
        "Journalism, Media & Mass Communication": "journalism",
        "Political Science & International Relations": "diplomacy",
        "Literature, Writing & Editorial": "literature",
        "Fine Arts, Design & Animation": "fine_arts",
        "Sociology & Social Work": "social_work",
        "History, Archaeology & Anthropology": "history",
    },
    "College - Medicine & Life Sciences": {
        "Clinical Practice (Medicine/Surgery/Dentistry)": "clinical",
        "Biotechnology & Genomic Research": "biotechnology",
        "Allied Health & Rehabilitation": "allied_health",
        "Pharmacology & Drug Development": "pharmacy",
        "Public Health & Epidemiology": "public_health",
        "Neuroscience & Mental Health Research": "psychology",
    },
    "College - Computer Science & IT": {
        "Full-Stack / Core Software Engineering": "software",
        "Data Science & Artificial Intelligence": "data_science",
        "Cybersecurity & Ethical Hacking": "cybersecurity",
        "Cloud Architecture & DevOps": "cloud",
        "Game Development & Interactive Media": "game_development",
        "Product Management & UI/UX Design": "product",
        "Advanced Academic Research & Higher Studies (MS / Ph.D.)": "academic_research",
    },
    "College - Core Engineering & Physical Sciences": {
        "Mechanical & Aerospace Engineering": "mechanical",
        "Civil & Sustainable Infrastructure": "civil",
        "Electronics, VLSI & IoT": "electronics",
        "Chemical & Materials Engineering": "chemical_materials",
        "Advanced Academic Research & Higher Studies (MS / Ph.D.)": "academic_research",
    },
    "College - Business, Finance & Commerce": {
        "Investment Banking & Corporate Finance": "investment",
        "Growth Marketing & Brand Strategy": "marketing",
        "Operations & Supply Chain Management": "operations",
        "Entrepreneurship & Venture Capital": "entrepreneurship",
        "Advanced Academic Research & Higher Studies (MBA / Ph.D.)": "academic_research",
    },
    "College - Arts, Humanities & Social Sciences": {
        "Psychology & Behavioral Science": "psychology",
        "Journalism & Mass Media": "journalism",
        "Sociology & Social Work": "social_work",
        "Literature, History & Editorial": "literature",
        "Advanced Academic Research & Higher Studies (MS / Ph.D.)": "academic_research",
    },
    "College - Law, Policy & International Relations": {
        "Corporate & Commercial Law": "corporate_law",
        "Criminal & Litigation Law": "criminal_law",
        "Public Policy & Governance": "policy",
        "International Relations & Diplomacy": "diplomacy",
        "Advanced Academic Research & Higher Studies (LL.M / Ph.D.)": "academic_research",
    },
    "College - Creative Arts, Architecture & Design": {
        "Architecture & Spatial Design": "architecture",
        "Fine Arts & Illustration": "fine_arts",
        "Animation & Game Design": "game_development",
        "Industrial & Product Design": "product_design",
        "Advanced Academic Research & Higher Studies (MFA / Ph.D.)": "academic_research",
    },
}


CAREER_SIGNALS: Dict[str, Tuple[str, ...]] = {
    "clinical": (
        "doctor", "physician", "patient", "diagnose", "diagnosing", "diagnosis",
        "clinical", "surgery",
        "surgeon", "hospital", "medical procedure", "anatomy", "emergency care",
        "treating illness", "direct patient care", "human body", "disease",
        "blood", "injury", "injuries", "healthcare", "patient interaction",
        "patient care", "biology", "operating room", "life-or-death",
    ),
    "veterinary": (
        "animal", "wildlife", "veterinarian", "veterinary", "pets",
        "working with animals", "biology",
    ),
    "biotechnology": (
        "biotechnology", "biotech", "genetics", "genetic", "dna", "molecular",
        "cells", "cellular", "genomic", "gene", "biological research", "biology",
        "plants", "environment", "scientific discovery", "research",
    ),
    "pharmacy": (
        "pharmacy", "pharmacist", "pharmacology", "pharmaceutical", "medicine", "medicines",
        "medication", "drug", "pill", "chemistry", "clinical trial", "drugs",
        "medicines and pharmaceuticals", "biology", "drugs affect the body",
    ),
    "allied_health": (
        "physio", "physical therapy", "rehabilitation", "rehab", "nutrition",
        "dietitian", "muscles", "movement", "recovery plan", "exercise plan",
        "helping people improve their health", "patient interaction", "biology",
    ),
    "public_health": (
        "public health", "community health", "healthcare management",
        "health systems", "epidemiology", "disease spread", "prevention",
        "population health", "health policy", "community", "communities",
        "health", "population", "preventing emergencies",
        "helping people improve their health", "biology", "environment",
        "policymaker", "policy", "big data", "global health", "public",
        "analyzing data", "preventing the emergencies",
        "policymaker", "policy", "big data", "global health", "public",
    ),
    "microbiology": (
        "microbiology", "microorganism", "microorganisms", "microbe", "microbes",
        "bacteria", "virus", "viruses", "immunology", "infectious disease",
        "micro", "biology", "research", "laboratory", "lab",
    ),
    "software": (
        "software", "coding", "code", "programming", "programmer", "algorithm",
        "debugging", "debug", "full-stack", "web application", "computer science",
        "bug", "app", "application", "website", "web or mobile app", "database",
        "system", "debugging code", "coding and building software", "app finally work",
        "web app", "mobile app", "database structure",
    ),
    "data_science": (
        "data", "statistics", "statistical", "probability", "machine learning",
        "artificial intelligence", "ai", "patterns in data", "analytics",
        "predictive model", "datasets", "big data", "trends", "data analyst",
        "mathematics", "math and algorithms", "math and statistics",
    ),
    "mechanical": (
        "mechanical", "aerospace", "engine", "machine", "robot", "mechanics",
        "prototype", "motion", "aerodynamic", "flight", "manufacturing",
        "engines", "machines", "moving parts", "drone", "go-kart",
        "motorized", "gears", "motors", "physics", "physical science",
        "motorized", "gears", "motors",
    ),
    "electronics": (
        "electronics", "electronic", "circuit", "chip", "semiconductor", "vlsi",
        "solder", "hardware", "embedded", "electrical", "sensor", "motherboard",
        "arduino", "raspberry pi", "smart-home gadget", "circuit board",
        "gadget", "electronics", "electrical component", "physics",
    ),
    "architecture": (
        "architecture", "architect", "building", "spatial design", "3d objects",
        "3d visualization", "blueprint", "architectural", "interior design",
        "skyscraper", "physical structures", "spatial flow", "city skyline",
        "lighting", "structural integrity", "blueprints to clients",
    ),
    "civil": (
        "civil engineering", "infrastructure", "bridge", "dam", "construction",
        "structural", "urban planning", "city planning", "construction site",
        "skyscraper", "sustainable house", "building design", "blueprint",
    ),
    "mathematics": (
        "pure mathematics", "abstract math", "mathematics", "mathematical proof",
        "calculus", "equations", "theoretical", "number theory", "quantitative",
        "geometry", "trigonometry", "math physics", "physics simulation",
        "advanced math", "mathematical physics", "physics",
        "advanced math", "mathematical physics",
    ),
    "accounting": (
        "accountancy", "accounting", "accountant", "chartered accountant", "audit",
        "auditing",         "tax", "balance sheet", "financial statements", "cpa", "bookkeeping",
        "auditing", "financials", "financial accuracy", "arithmetic", "percentages",
        "financials", "financial accuracy", "arithmetic", "percentages",
    ),
    "investment": (
        "investment", "banking", "banker", "stock market", "equity", "trading",
        "valuation", "mergers", "acquisitions", "financial model", "portfolio",
        "macro market trends", "macro economics", "financial projections",
        "economics", "economic", "financial", "cfo", "stock charts", "gdp",
        "inflation", "unemployment", "long-term impact", "financial models",
        "economics", "economic", "financial", "cfo", "stock charts",
    ),
    "corporate_law": (
        "corporate law", "commercial law", "legal", "lawyer", "contracts",
        "legislation", "compliance codes", "legal consulting", "court",
        "compliance", "loopholes", "contract", "legal framework", "legal documents",
        "laws are made", "laws are enforced",
        "compliance", "loopholes", "contract", "legal framework", "legal documents",
    ),
    "marketing": (
        "marketing", "brand", "advertising", "campaign", "consumer behavior",
        "social media", "audience", "creative director", "go-to-market",
        "information visually appealing", "designing campaigns",
    ),
    "entrepreneurship": (
        "entrepreneur", "startup", "start-up", "founder", "venture capital",
        "pitch", "seed funding", "build a business", "my own company", "business strategy",
        "building a business", "business from zero", "million dollars", "business studies",
        "business studies", "high risk", "risk-reward", "take charge", "leadership",
        "business world", "business studies",
        "high risk", "risk-reward", "take charge", "leadership",
    ),
    "actuarial": (
        "actuarial", "risk model", "insurance", "predicting risk",
        "statistical risk", "financial derivatives", "risk management", "advanced math",
        "probability", "calculus", "mathematics",
    ),
    "human_resources": (
        "human resources", "organizational behavior", "people operations",
        "employee", "hiring", "talent management", "workplace culture",
        "follow rules", "ensure others do", "people", "leadership", "team",
    ),
    "psychology": (
        "psychology", "psychologist", "counseling", "counselor", "human mind",
        "mental health", "behavior", "behaviour", "therapy", "therapist",
        "cognitive", "trauma", "brain", "brain and behaviour", "brain and behavior",
        "listening and offering advice", "individual behaves", "empathetic",
        "healing one person's mind", "counsel them", "brain", "brain and behaviour", "brain and behavior",
        "listening and offering advice", "individual behaves", "empathetic",
        "healing one person's mind", "counsel them",
    ),
    "journalism": (
        "journalism", "journalist", "media", "newsroom", "reporting", "reporter",
        "interview", "investigative", "broadcast", "camera", "microphone",
        "public speaking", "daily news", "global affairs", "exposing corruption",
        "tell the truth", "truth to the masses", "direct questions",
        "updated with daily news", "asking tough", "document stories",
        "public speaking", "daily news", "global affairs", "exposing corruption",
        "tell the truth", "truth to the masses", "direct questions",
        "updated with daily news", "asking tough", "document stories",
    ),
    "diplomacy": (
        "diplomacy", "diplomat", "international relations", "foreign policy",
        "geopolitics", "model un", "political science", "treaty", "embassy",
        "debate", "public speaking", "government", "governments", "policy",
        "drafting policies", "social issue", "negotiate", "foreign affairs",
        "international trade", "hold power", "civil service", "civic leaders",
        "debate", "public speaking", "government", "governments", "policy",
        "drafting policies", "social issue", "negotiate", "foreign affairs",
        "international trade", "hold power", "civil service", "civic leaders",
    ),
    "literature": (
        "literature", "creative writing", "author", "editor", "editorial",
        "publishing", "poetry", "novel", "books", "historical texts",
        "writing", "text and history", "reading", "historical", "lectures",
        "academic theories",
        "writing", "text and history", "reading", "historical", "lectures",
        "academic theories",
    ),
    "fine_arts": (
        "fine art", "fine arts", "visual art", "visual arts", "illustration",
        "painting", "gallery", "artistic", "art portfolio", "art director",
        "art", "aesthetic", "color", "emotion", "creative freedom", "canvases",
        "art", "aesthetic", "color", "emotion", "creative freedom", "canvases",
    ),
    "social_work": (
        "social work", "sociology", "community", "ngo", "social justice",
        "marginalized", "vulnerable populations", "systemic inequality",
        "community programs", "listening and offering advice", "welfare systems",
        "helping them navigate", "systemic resources", "helping others",
        "advocating", "welfare", "social issue", "social issues", "listening and offering advice", "welfare systems",
        "helping them navigate", "systemic resources", "helping others",
        "advocating", "welfare", "social issue", "social issues",
    ),
    "history": (
        "history", "historian", "archaeology", "archaeologist", "anthropology",
        "museum", "archive", "ancient cultures", "historical research",
        "ancient ruins", "civilizations", "cultural history", "art history",
        "history of art", "historical significance",
        "ancient ruins", "civilizations", "cultural history", "art history",
        "history of art", "historical significance",
    ),
    "cybersecurity": (
        "cybersecurity", "cyber security", "ethical hacking", "security",
        "vulnerability", "vulnerabilities", "threat defense", "network security",
    ),
    "cloud": (
        "cloud", "devops", "deployment", "infrastructure", "automation pipeline",
        "server", "continuous integration", "platform engineering", "uptime",
    ),
    "game_development": (
        "game development", "game design", "video game", "gaming", "interactive",
        "graphics", "shader", "unity", "unreal", "animation",
    ),
    "product": (
        "product management", "product manager", "user experience", "user interface",
        "ux", "ui", "user research", "feature roadmap", "wireframe",
    ),
    "academic_research": (
        "academic research", "higher studies", "ph.d", "phd", "professor",
        "dissertation", "peer-reviewed", "research institute", "university research",
        "research lab", "research laboratory", "university office", "think tank",
        "publishing economic papers", "theoretical", "academic", "research",
        "lecturing", "lectures", "academic theories", "philosophy",
        "lecturing", "lectures", "academic theories", "philosophy",
    ),
    "chemical_materials": (
        "chemical engineering", "materials science", "material science",
        "chemical compounds", "chemical reaction", "battery chemistry",
        "carbon capture", "molecular bonds", "chemical drugs", "chemicals",
        "raw materials", "energy", "processing plant", "chemistry lab",
        "bio-plastics", "battery cells", "chemistry", "chemical", "chemistry", "chemical",
    ),
    "operations": (
        "operations", "supply chain", "logistics", "process flow", "bottleneck",
        "inventory", "distribution center", "operational efficiency",
        "manufacture and ship", "shipping", "ship globally", "production",
        "lowest cost", "process flowchart", "manufacturing", "process",
    ),
    "criminal_law": (
        "criminal law", "criminal", "litigation", "courtroom", "witness",
        "police reports", "case files", "trial", "justice system",
        "jury", "cross-examining", "cross-examine", "evidence", "jury",
    ),
    "policy": (
        "public policy", "governance", "government policy", "civil service",
        "policymaker", "policy advisor", "legislation", "social policy",
        "congress", "parliament", "government office", "think tank",
        "legislative compromise", "social issue", "government", "policymakers",
        "government office", "public service",
    ),
    "product_design": (
        "industrial design", "product design", "prototype", "ergonomics",
        "physical product", "consumer product", "cad", "manufacturing design",
        "designing sleek", "functional physical products", "human hand",
        "physical objects", "design philosophies", "functional",
    ),
    "environmental_science": (
        "environment", "environmental", "plants", "conservation", "ecosystem",
        "living organisms", "climate", "sustainability", "wildlife conservation",
        "environmental impact", "environmental science",
    ),
}


QUESTION_WEIGHTS: Mapping[int, float] = {
    1: 1.25,
    2: 1.25,
    3: 1.25,
    19: 1.5,
    20: 1.5,
}

_NEGATION = re.compile(
    r"\b(?:not|never|hate|dislike|struggle|uncomfortable|avoid|limited|"
    r"no interest|don't|doesn't)\b(?:\W+\w+){0,4}\s*$",
    re.IGNORECASE,
)


def _keyword_sentiment(answer: str, keyword: str) -> int:
    pattern = re.compile(rf"(?<!\w){re.escape(keyword)}(?!\w)", re.IGNORECASE)
    sentiments = []
    for match in pattern.finditer(answer):
        prefix = answer[: match.start()]
        clause = re.split(r"\b(?:but|however|although)\b|[.!?;]", prefix)[-1]
        sentiments.append(-1 if _NEGATION.search(clause) else 1)
    return max(sentiments, default=0)


def score_careers(stream: str, answers: Mapping[int, str]) -> List[CareerMatch]:
    tracks = CAREER_TRACKS[stream]
    denominator = sum(QUESTION_WEIGHTS.get(question_id, 1.0) for question_id in answers)
    raw_scores = {title: 0.0 for title in tracks}

    for question_id, answer in answers.items():
        weight = QUESTION_WEIGHTS.get(question_id, 1.0)
        for title, signal_group in tracks.items():
            sentiments = [
                _keyword_sentiment(answer, keyword)
                for keyword in CAREER_SIGNALS[signal_group]
            ]
            if 1 in sentiments:
                raw_scores[title] += weight
            elif -1 in sentiments:
                raw_scores[title] -= weight

    ranked = [
        {
            "title": title,
            "match": round(max(0.0, min(score / denominator * 100, 100.0)), 1),
        }
        for title, score in raw_scores.items()
    ]
    return sorted(ranked, key=lambda result: (-result["match"], result["title"]))
