# 🧠 Quizbot

A tiny quiz app you can run in the terminal **and** as a Flask web app.  
Questions live in JSON, you can filter by category and difficulty, and auto-graded answers ignore case/spacing/punctuation. Results are saved locally.

---

## ✨ Features
- CLI and Flask web UI
- JSON-driven questions
- Category & difficulty filters
- Input normalization (fair matching)
- Open-ended questions supported
- Saves results to `scores.jsonl`

---

## ▶️ Run locally

**Requirements:** Python 3.10+

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
