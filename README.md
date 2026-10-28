ClarityOS

Live Project: https://clarity-os-delta.vercel.app

Assessment Route: https://clarity-os-delta.vercel.app/assessment

ClarityOS is a career-exploration website for students in grades 11-12 and college. Each study track has a 20-question questionnaire, and the results rank career areas using signals found in the student's selected answers.

The quiz currently supports four high-school streams (PCM, PCB, Commerce, and Arts/Humanities) and seven college tracks. It is not designed for younger children yet.

## How results work

The FastAPI backend scores each career area against answer-language signals and returns an exploratory alignment score. These scores are heuristic, are not validated psychometric measurements, and should not be treated as predictions of ability or definitive career advice. Students should explore several options and discuss important decisions with a trusted adult or career counselor.

Gemini can provide a plain-language explanation of the leading areas. If that service is unavailable, the assessment still returns its calculated results with a fallback explanation.

## Checks

- Backend: from `backend`, run `python -m unittest -v test_quiz`.
- Frontend: from `frontend`, run `npx tsc --noEmit` and `npm run build`.

## Tech stack

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: Python, FastAPI
- Optional explanation service: Gemini API

- Deployment: Vercel (frontend), Render (backend)
