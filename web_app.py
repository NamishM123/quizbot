from datetime import datetime
import os

def save_score(row, path="scores.jsonl"):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


# web_app.py — Day 4: minimal Flask wrapper around your quiz logic

from flask import Flask, request, session, redirect, url_for, render_template_string
import json, re, random

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

# --- reuse the ideas from Day 3 (kept inline here for simplicity) ---

def normalize(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '', text.strip().lower())

def load_questions(path: str = "questions.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for q in data:
        q.setdefault("answer", None)
        q.setdefault("difficulty", "easy")
    return data

def available_values(questions):
    cats = sorted({q["category"] for q in questions})
    order = ("easy", "medium", "hard")
    diffs = sorted({q["difficulty"] for q in questions}, key=lambda d: order.index(d) if d in order else 999)
    return cats, diffs

def filter_questions(questions, category, difficulty):
    def match(val, actual): return (val is None) or (val.lower() == actual.lower())
    return [q for q in questions if match(category, q["category"]) and match(difficulty, q["difficulty"])]

ALL_QS = load_questions()  # load once

# --- pages ---

FORM_HTML = """
<!doctype html>
<title>Quizbot</title>
<h1>Quizbot (Web)</h1>
<form method="post" action="{{ url_for('start_quiz') }}">
  <label>Category:</label>
  <select name="category">
    <option value="">ALL</option>
    {% for c in cats %}<option value="{{ c }}">{{ c }}</option>{% endfor %}
  </select>
  &nbsp;&nbsp;
  <label>Difficulty:</label>
  <select name="difficulty">
    <option value="">ALL</option>
    {% for d in diffs %}<option value="{{ d }}">{{ d }}</option>{% endfor %}
  </select>
  &nbsp;&nbsp;
  <label><input type="checkbox" name="shuffle" checked> Shuffle</label>
  <button type="submit">Start</button>
</form>
"""

QUIZ_HTML = """
<!doctype html>
<title>Quiz</title>
<h2>Answer the questions</h2>
<form method="post" action="{{ url_for('submit_quiz') }}">
  {% for i, q in enumerate(qs) %}
    <div style="margin:12px 0;padding:8px;border:1px solid #ddd;">
      <div><b>[{{ q.category }} • {{ q.difficulty }}]</b> {{ q.question }}</div>
      {% if q.answer is not none %}
        <input name="ans_{{ i }}" style="width:60%;" autocomplete="off">
      {% else %}
        <input name="ans_{{ i }}" placeholder="(open-ended)" style="width:60%;" autocomplete="off">
      {% endif %}
    </div>
  {% endfor %}
  <button type="submit">Submit</button>
</form>
"""

RESULT_HTML = """
<!doctype html>
<title>Results</title>
<h2>Results</h2>
<p>Auto-graded score: <b>{{ correct }}</b> / <b>{{ total }}</b></p>
<a href="{{ url_for('home') }}">Try another set</a>
"""

@app.get("/")
def home():
    cats, diffs = available_values(ALL_QS)
    return render_template_string(FORM_HTML, cats=cats, diffs=diffs)


@app.post("/start")
def start_quiz():
    cat = request.form.get("category") or None
    diff = request.form.get("difficulty") or None
    shuffle = bool(request.form.get("shuffle"))

    selected = filter_questions(ALL_QS, cat, diff)
    if not selected:
        return "<p>No questions match those filters. <a href='/'>Back</a></p>", 400

    if shuffle:
        random.shuffle(selected)

    session["qs"] = selected
    session["filters"] = {"category": cat, "difficulty": diff}  # <-- add this line

    return redirect(url_for("show_quiz"))


@app.get("/quiz")
def show_quiz():
    qs = session.get("qs") or []
    return render_template_string(QUIZ_HTML, qs=qs, enumerate=enumerate)

@app.post("/submit")
def submit_quiz():
    qs = session.get("qs") or []
    filters = session.get("filters", {})  # read what we saved in /start

    correct = 0
    total = sum(q.get("answer") is not None for q in qs)

    for i, q in enumerate(qs):
        user = request.form.get(f"ans_{i}", "")
        ans = q.get("answer")
        if ans is None:
            continue
        if normalize(user) == normalize(ans):
            correct += 1

    # Persist one JSON line with your result
    save_score({
        "at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "category": filters.get("category"),
        "difficulty": filters.get("difficulty"),
        "questions": len(qs),
        "auto_total": total,
        "correct": correct,
    })

    return render_template_string(RESULT_HTML, correct=correct, total=total)


# Route names used in templates
start_quiz = start_quiz
submit_quiz = submit_quiz
