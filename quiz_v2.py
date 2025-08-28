# quiz_v2.py — Day 2: load from JSON, pick category, keep score

import json, re, sys

def normalize(text: str) -> str:
    """Lowercase, trim, remove punctuation/spaces for fair comparison."""
    return re.sub(r'[^a-z0-9]+', '', text.strip().lower())

def load_questions(path: str = 'questions.json'):
    """Load questions from JSON; ensure keys exist."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("questions.json not found. Create it first in the same folder.")
        sys.exit(1)
    if not isinstance(data, list):
        print("questions.json must be a JSON array of objects.")
        sys.exit(1)
    for i, q in enumerate(data, 1):
        if not isinstance(q, dict) or 'question' not in q or 'category' not in q:
            print(f"Bad item at #{i}: {q}")
            sys.exit(1)
        q.setdefault('answer', None)  # default to open-ended
    return data

def choose_category(questions):
    """Let user choose a category (or ALL)."""
    cats = sorted({q['category'] for q in questions})
    print("\nAvailable categories:", ", ".join(cats))
    choice = input("Pick a category (or press Enter for ALL): ").strip()
    if choice == '':
        return questions, 'ALL'
    for c in cats:
        if c.lower() == choice.lower():
            return [q for q in questions if q['category'] == c], c
    print("No such category; using ALL.")
    return questions, 'ALL'

def run_quiz(questions):
    total_auto = sum(q['answer'] is not None for q in questions)
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}. [{q['category']}] {q['question']}")
        user = input("> ")
        if q['answer'] is None:
            print("✅ Thanks! (open-ended)")
            continue
        if normalize(user) == normalize(q['answer']):
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Correct answer: {q['answer']}")
    print("\n— Results —")
    print(f"Auto-graded score: {score} / {total_auto}")

def main():
    qs_all = load_questions('questions.json')
    qs, label = choose_category(qs_all)
    print(f"\nStarting quiz for: {label} ({len(qs)} question(s))")
    run_quiz(qs)

if __name__ == '__main__':
    main()
