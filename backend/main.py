import logging
import os
from typing import Dict

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from quiz_scoring import CAREER_TRACKS, score_careers

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")
logger = logging.getLogger(__name__)

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
    answers: Dict[int, str]


@app.post("/analyze-quiz")
async def analyze_quiz(payload: QuizPayload):
    if payload.stream not in CAREER_TRACKS:
        raise HTTPException(status_code=422, detail="Choose a supported study track.")

    question_ids = set(payload.answers)
    if question_ids != set(range(1, 21)):
        raise HTTPException(
            status_code=422,
            detail="Answer all 20 questions before requesting results.",
        )

    answers = {question_id: answer.strip() for question_id, answer in payload.answers.items()}
    if any(not answer or len(answer) > 500 for answer in answers.values()):
        raise HTTPException(
            status_code=422,
            detail="Each answer must contain between 1 and 500 characters.",
        )

    ranked_results = score_careers(payload.stream, answers)
    optimal_vector = ranked_results[0] if ranked_results[0]["match"] > 0 else None

    if optimal_vector is None:
        explanation = (
            "Your answers do not yet point strongly toward one of these paths. "
            "Use the list as a starting point for exploring what interests you; "
            "this quiz is not a definitive career recommendation."
        )
    else:
        top_careers = [
            f"{match['title']} ({match['match']}% alignment)"
            for match in ranked_results[:3]
        ]
        prompt = (
            "A student completed an exploratory career questionnaire. Their leading "
            f"areas of interest are: {', '.join(top_careers)}. Write two short, "
            "encouraging paragraphs explaining possible shared interests and one "
            "small way they could explore these areas. Do not claim the result is "
            "scientific, definitive, guaranteed, or a measure of ability. Address "
            "the student as 'you'."
        )
        try:
            explanation = model.generate_content(prompt).text
            if not explanation or not explanation.strip():
                raise ValueError("The explanation service returned an empty response.")
        except Exception:
            logger.exception("Could not generate the assessment explanation.")
            explanation = (
                "Your answers show some interest in the paths listed below. Try a "
                "small project, class, or conversation with someone in one of these "
                "fields to learn more. These scores are exploratory, not a definitive "
                "career recommendation."
            )

    return {
        "status": "success",
        "stream": payload.stream,
        "optimal_vector": optimal_vector,
        "evaluated_vectors": ranked_results,
        "explanation": explanation,
        "score_type": "exploratory",
    }
