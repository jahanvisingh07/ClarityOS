from fastapi import FastAPI
from models import StudentProfile
from algorithm import calculate_career_fit

app = FastAPI(title="ClarityOS API")

@app.get("/")
def read_root():
    return {"message": "ClarityOS Engine is running."}

@app.post("/analyze")
def analyze_profile(profile: StudentProfile):
    # This takes the JSON from the frontend and runs it through your WSM algorithm
    result = calculate_career_fit(profile)
    return result