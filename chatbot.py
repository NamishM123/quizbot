# quiz_v2.py — Day 2: JSON + categories + scoring

import json, re, sys

def normalize(text: str) -> str:
    """Lowercase, trim, remove punctuation/spaces for fair comparison."""
    return re.sub(r'[^a-z0-9]+', '', text.strip().lower())

def load_questions(path: str = 'questions.json'):
    """Load questions from JSON and do minimal validation."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i, q in enumerate(data, 1):
        if not all(k in q for k in ('category', 'question')):
            raise ValueError(f"Bad item at #{i}: {q}")
        if 'answer' not in q:
            q['answer'] = None
    return data

def choose_category(questions):
    """Let the user pick a category (or ALL). Returns (filtered, label)."""
    cats = sorted({q['category'] for q in questions})
    print("\nAvailable categories:", ", ".join(cats))
    choice = input("Pick a category (or press Enter for ALL): ").strip()
    if choice == '':
        return questions, 'ALL'
    for c in cats:
        if c.lower() == choice.lower():
            selected = [q for q in questions if q['category'] == c]
            return selected, c
    print("No such category; using ALL.")
    return questions, 'ALL'

def run_quiz(questions):
    """Ask questions and keep score (auto-graded only)."""
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
    try:
        all_questions = load_questions()
    except FileNotFoundError:
        print("questions.json not found. Create it first.")
        sys.exit(1)
    qs, label = choose_category(all_questions)
    print(f"\nStarting quiz for: {label} ({len(qs)} question(s))")
    run_quiz(qs)

if __name__ == '__main__':
    main()
