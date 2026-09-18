# game.py
import json
import os
import random
from words import (
    FIVE_LETTER_WORDS, SCRAMBLE_WORDS, HANGMAN_WORDS,
    SCRAMBLE_HINTS, HANGMAN_HINTS
)

LEADERBOARD_FILE = "leaderboard.json"


# ---------- Leaderboard ----------
def load_leaderboard() -> dict:
    if not os.path.exists(LEADERBOARD_FILE):
        return {}
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_leaderboard(data: dict) -> None:
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_score(user_id: int, username: str, points: int) -> None:
    data = load_leaderboard()
    key = str(user_id)
    if key not in data:
        data[key] = {"name": username or f"User{user_id}", "score": 0, "wins": 0}
    data[key]["score"] += points
    data[key]["wins"] += 1
    data[key]["name"] = username or data[key]["name"]
    save_leaderboard(data)


def get_top(limit: int = 10) -> list:
    data = load_leaderboard()
    items = sorted(data.values(), key=lambda x: x["score"], reverse=True)
    return items[:limit]


# ---------- Word Scramble ----------
def new_scramble():
    word = random.choice(SCRAMBLE_WORDS)
    scrambled = "".join(random.sample(word, len(word)))
    # Ensure scrambled is not identical to original
    while scrambled.lower() == word.lower():
        scrambled = "".join(random.sample(word, len(word)))
    hint = SCRAMBLE_HINTS.get(word, "No hint available.")
    return {"answer": word, "scrambled": scrambled.upper(), "hint": hint}


# ---------- Hangman ----------
def new_hangman():
    word = random.choice(HANGMAN_WORDS)
    hint = HANGMAN_HINTS.get(word, "No hint available.")
    return {"answer": word, "hint": hint, "guessed": set(), "wrong": 0, "max_wrong": 6}


def render_hangman(game: dict) -> str:
    word = game["answer"]
    display = " ".join(c if c in game["guessed"] else "_" for c in word)
    wrong_letters = sorted(l for l in game["guessed"] if l not in word)
    return (
        f"🎯 *Hangman*\n\n"
        f"Hint: {game['hint']}\n\n"
        f"`{display}`\n\n"
        f"❌ Wrong guesses ({game['wrong']}/{game['max_wrong']}): "
        f"{' '.join(wrong_letters) if wrong_letters else '—'}\n\n"
        f"Send a single letter to guess."
    )


# ---------- Wordle-style ----------
def new_wordle():
    word = random.choice(FIVE_LETTER_WORDS).lower()
    return {"answer": word, "guesses": [], "max_guesses": 6}


def score_guess(answer: str, guess: str) -> str:
    """Return emoji feedback for each letter: 🟩 correct, 🟨 wrong place, ⬛ absent."""
    answer_chars = list(answer)
    guess_chars = list(guess)
    result = ["⬛"] * len(guess)

    # First pass: exact matches
    for i, (a, g) in enumerate(zip(answer_chars, guess_chars)):
        if a == g:
            result[i] = "🟩"
            answer_chars[i] = None
            guess_chars[i] = None

    # Second pass: misplaced
    for i, g in enumerate(guess_chars):
        if g is None:
            continue
        if g in answer_chars:
            result[i] = "🟨"
            answer_chars[answer_chars.index(g)] = None

    return "".join(result)


def render_wordle(game: dict) -> str:
    lines = ["🎯 *Wordle* — guess the 5-letter word\n"]
    for guess, feedback in game["guesses"]:
        lines.append(f"`{guess.upper()}`  {feedback}")
    remaining = game["max_guesses"] - len(game["guesses"])
    lines.append(f"\nRemaining tries: {remaining}")
    lines.append("Send a 5-letter word to guess.")
    return "\n".join(lines)
