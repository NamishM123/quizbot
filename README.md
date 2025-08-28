# Quizbot
CLI + Flask web quiz with JSON questions, categories, difficulty, scoring, and saved results.

## Run locally
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python web_app.py
# open http://127.0.0.1:5057/

## Data format
questions.json: [{"category":"Algorithms","question":"...","answer":"O(log n)","difficulty":"medium"}]

## Deploy
- Build: pip install -r requirements.txt
- Start: gunicorn web_app:app
