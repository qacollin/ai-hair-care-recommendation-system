# AI Hair Care Recommendation System
A Hybrid Decision Support System Using Large Language Models

Built by: Quarshona Collins and Courtney Carr
School: North Carolina A&T State University
Version: v4.0

---

## What Is This?

This is an AI-powered app that gives personalized hair care advice 
based on a short survey. You answer 13 questions about your hair 
and the app gives you a full routine, product recommendations, 
and explains exactly why those products work for your specific hair.

---

## How It Works

1. Fill out the 13-question hair survey
2. The Mini Brain (our rule-based engine) analyzes your answers
3. A Hair Profile Score Dashboard is generated showing your 
   Moisture Level, Damage Level, Scalp Health, and Breakage Risk
4. Everything gets sent to GPT-4o-mini (OpenAI)
5. The AI sends back a full personalized recommendation in 5 sections
6. You can rate the recommendation and give feedback

---

## Tech Stack

- Python
- Streamlit
- OpenAI API / GPT-4o-mini
- Rule-based logic (Mini Brain)

---

## Features

- 13-question hair assessment survey
- Hair Profile Score Dashboard
- Dual Mini Brain with weighted scoring
- AI-generated day-by-day weekly routine
- 5-section structured output
- Confidence score
- User feedback loop (1 to 5 star rating)

---

## How to Run It

Step 1: Install the required libraries by running this in your terminal:
pip install streamlit openai

Step 2: Add your OpenAI API key inside app.py

Step 3: Run the app with this command:
streamlit run app.py

---

## Demo Video

Watch the full demo here:
https://drive.google.com/file/d/1Fqz2u9xVQ9YAS1ODEFZOdeCQiZ22qpVr/view

---

## About This Project

This project was built as a graduate research project for COMP710 
at North Carolina A&T State University. It is documented as a full 
IEEE-format research paper covering three phases of development:

Phase 1 - Problem identification, literature review, and first prototype
Phase 2 - System design with UML diagrams and improved prototype  
Phase 3 - Final version with all features, evaluation, and testing

Testing included 30 response time trials with an average of 10.267 
seconds per response, accuracy testing across 20 input combinations, 
and a 5-user usability study.

---

## Future Plans

- Connect to a real product database for specific brand recommendations
- Add photo upload so AI can visually analyze your hair
- Save user sessions to track progress over time
- Run a formal user study with real participants
