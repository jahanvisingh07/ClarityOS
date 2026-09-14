ClarityOS

Live Project: https://clarity-os-delta.vercel.app

Assessment Route: https://clarity-os-delta.vercel.app/assessment

ClarityOS is a full stack AI career assessment platform built to replace static career quizzes with a dynamic mathematical evaluation engine. I built this to solve the problem of generic career advice by combining a rigorous scoring model with natural language generation, giving users personalized and highly accurate insights.

Architecture and Engineering
  1. Custom Scoring Engine
I engineered a Weighted Sum Model (MCDA) using Python and FastAPI. Instead of basic logic trees, the algorithm dynamically processes up to 20 behavioral and academic data points, scoring them against up to 7 specialized career tracks per stream to calculate highly calibrated compatibility percentages.

  2. LLM Explanation Layer
Raw numbers are not enough for a great user experience. I integrated the Gemini API to act as a reasoning layer, translating the mathematical percentage scores into plain English career advice and actionable strength breakdowns.

  3. Modern Frontend Implementation
The client interface is built with Next.js, React, and TypeScript. It features a step by step assessment form and a dynamic results dashboard designed for flawless cross device responsiveness and state management.

  4. Decoupled Cloud Deployment
The platform uses a strict separation of concerns. The REST API backend is hosted on Render, and the Next.js frontend is deployed on Vercel. I configured the automated CI/CD pipeline and resolved strict framework build bottlenecks to ensure stable production uptime.

Tech Stack
  - Frontend: Next.js, React, TypeScript, Tailwind CSS

  - Backend: Python, FastAPI

  - AI Integration: Gemini API

  - Deployment: Vercel, Render, Git
