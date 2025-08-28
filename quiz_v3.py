# quiz_v3.py — Day 3: clean structure, difficulty filter, retry loop

import json, re, random, sys
from typing import List, Dict, Tuple, Optional

# ---------- Core utilities ----------

def normalize(text: str) -> str:
    """
    Fair comparison:
    - lowercase
    - strip edges
    - remove punctuation/whitespace
    e.g., '  O( LOG n ) ' -> 'ologn'
    """
    return re.sub(r'[^a-z0-9]+', '', text.strip().lower())

def load_questions(path: str = 'questions.json') -> List[Dict]:
    """Load questions from JSON; validate and set defaults."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("questions.json not found. Create it first.")
        sys.exit(1)

    if not isinstance(data, list):
        print("questions.json must be a JSON array.")
        sys.exit(1)

    for i, q in enumerate(data, 1):
        if not isinstance(q, dict):
            print(f"Item #{i} is not an object: {q!r}"); sys.exit(1)
        if 'category' not in q or 'question' not in q:
            print(f"Item #{i} missing category/question: {q!r}"); sys.exit(1)
        q.setdefault('answer', None)        # open-ended if missing
        q.setdefault('difficulty', 'easy')  # default difficulty
        if q['difficulty'] not in ('easy', 'medium', 'hard'):
            print(f"Item #{i} has invalid difficulty: {q['difficulty']!r}")
            sys.exit(1)
    return data

def available_values(questions: List[Dict]) -> Tuple[List[str], List[str]]:
    """Return sorted unique (categories, difficulties)."""
    cats = sorted({q['category'] for q in questions})
    order = ('easy','medium','hard')
    diffs = sorted({q['difficulty'] for q in questions}, key=lambda d: order.index(d) if d in order else 999)
    return cats, diffs

def filter_questions(questions: List[Dict], category: Optional[str], difficulty: Optional[str]) -> List[Dict]:
    """Filter by category and difficulty (case-insensitive)."""
    def match(val: Optional[str], actual: str) -> bool:
        return val is None or val.lower() == actual.lower()
    return [q for q in questions if match(category, q['category']) and match(difficulty, q['difficulty'])]

# ---------- Quiz flow ----------

def ask_one(q: Dict) -> Tuple[Optional[bool], bool]:
    """
    Ask a single question.
    Returns (is_correct, is_auto_gradable):
      - (True, True)  -> correct graded
      - (False, True) -> wrong graded
      - (None, False) -> open-ended (not graded)
    """
    print(f"\n[{q['category']} • {q['difficulty']}] {q['question']}")
    user = input("> ")
    if q['answer'] is None:
        print("✅ Thanks! (open-ended)")
        return None, False
    ok = normalize(user) == normalize(q['answer'])
    if ok: print("✅ Correct!")
    else:  print(f"❌ Correct answer: {q['answer']}")
    return ok, True

def run_quiz(qs: List[Dict], shuffle: bool = True) -> Tuple[int, int]:
    """Run through a set of questions; return (correct, total_auto)."""
    if shuffle:
        random.shuffle(qs)
    correct = 0
    total_auto = sum(q['answer'] is not None for q in qs)
    for q in qs:
        is_correct, is_auto = ask_one(q)
        if is_auto and is_correct:
            correct += 1
    return correct, total_auto

# ---------- Console UI helpers ----------

def choose(prompt: str, options: List[str]) -> Optional[str]:
    """Ask the user to pick a value from options; Enter means ALL (None)."""
    print(f"{prompt} " + "/".join(options) + " (Enter=ALL)")
    val = input("> ").strip()
    if val == "": return None
    for opt in options:
        if opt.lower() == val.lower():
            return opt
    print("No match; using ALL.")
    return None

def play():
    """High-level loop: load -> choose filters -> quiz -> retry."""
    all_qs = load_questions()
    cats, diffs = available_values(all_qs)

    print("🤖 Quizbot Day 3 — category + difficulty + retry")
    while True:
        print("\nAvailable categories:", ", ".join(cats))
        cat = choose("Pick category:", cats)

        print("\nAvailable difficulties:", ", ".join(diffs))
        diff = choose("Pick difficulty:", diffs)

        selected = filter_questions(all_qs, cat, diff)
        if not selected:
            print("No questions match those filters. Try again.")
            continue

        print(f"\nStarting quiz with {len(selected)} question(s).")
        correct, total = run_quiz(selected, shuffle=True)
        print("\n— Results —")
        print(f"Auto-graded score: {correct} / {total}")

        again = input("\nPlay another set? (y/n): ").strip().lower()
        if again != 'y':
            print("Bye! 👋")
            break

def main():
    try:
        play()
    except KeyboardInterrupt:
        print("\nInterrupted — bye!")

if __name__ == "__main__":
    main()
