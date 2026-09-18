import os
import logging
import random
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)
from game import (
    new_scramble, new_hangman, render_hangman,
    new_wordle, render_wordle, score_guess,
    add_score, get_top
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Per-user active game state: {user_id: {"mode": ..., "data": {...}}}
ACTIVE_GAMES = {}


# ---------- Commands ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🧩 *Welcome to World Puzzle Bot!*\n\n"
        "Sharpen your mind with three word games:\n"
        "• /scramble — Unscramble a word\n"
        "• /hangman — Classic hangman\n"
        "• /wordle — Guess the 5-letter word in 6 tries\n"
        "• /leaderboard — See the top players\n"
        "• /quit — End your current game\n\n"
        "Every correct answer earns you points. Good luck!",
        parse_mode="Markdown"
    )


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    top = get_top(10)
    if not top:
        await update.message.reply_text("🏆 No scores yet — be the first to win a game!")
        return
    lines = ["🏆 *Leaderboard — Top Players*\n"]
    for i, entry in enumerate(top, 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
        lines.append(f"{medal} {entry['name']} — {entry['score']} pts ({entry['wins']} wins)")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def quit_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in ACTIVE_GAMES:
        ACTIVE_GAMES.pop(user_id)
        await update.message.reply_text("🛑 Game ended. Send /scramble, /hangman, or /wordle to start a new one.")
    else:
        await update.message.reply_text("You don't have an active game.")


# ---------- Scramble ----------
async def start_scramble(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    data = new_scramble()
    ACTIVE_GAMES[user_id] = {"mode": "scramble", "data": data}
    await update.message.reply_text(
        f"🔤 *Word Scramble*\n\n"
        f"Unscramble this word:\n\n"
        f"`{data['scrambled']}`\n\n"
        f"💡 Hint: {data['hint']}\n\n"
        f"Type your answer, or /quit to give up.",
        parse_mode="Markdown"
    )


# ---------- Hangman ----------
async def start_hangman(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    data = new_hangman()
    ACTIVE_GAMES[user_id] = {"mode": "hangman", "data": data}
    await update.message.reply_text(render_hangman(data), parse_mode="Markdown")


# ---------- Wordle ----------
async def start_wordle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    data = new_wordle()
    ACTIVE_GAMES[user_id] = {"mode": "wordle", "data": data}
    await update.message.reply_text(render_wordle(data), parse_mode="Markdown")


# ---------- Handle text guesses ----------
async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    text = update.message.text.strip()

    if user_id not in ACTIVE_GAMES:
        await update.message.reply_text(
            "You don't have an active game. Start one with /scramble, /hangman, or /wordle."
        )
        return

    game = ACTIVE_GAMES[user_id]
    mode = game["mode"]
    data = game["data"]

    # ----- Scramble -----
    if mode == "scramble":
        if text.lower() == data["answer"].lower():
            points = 10
            add_score(user_id, user.username or user.first_name, points)
            ACTIVE_GAMES.pop(user_id)
            await update.message.reply_text(
                f"✅ Correct! The word was *{data['answer'].upper()}*.\n+{points} points! 🎉",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ Not quite. Try again or /quit.")

    # ----- Hangman -----
    elif mode == "hangman":
        if len(text) != 1 or not text.isalpha():
            await update.message.reply_text("Please send a single letter (A-Z).")
            return
        letter = text.lower()
        if letter in data["guessed"]:
            await update.message.reply_text("You already guessed that letter.")
            return
        data["guessed"].add(letter)
        if letter not in data["answer"]:
            data["wrong"] += 1

        # Win?
        if all(c in data["guessed"] for c in data["answer"]):
            points = 15
            add_score(user_id, user.username or user.first_name, points)
            ACTIVE_GAMES.pop(user_id)
            await update.message.reply_text(
                f"✅ You saved him! The word was *{data['answer'].upper()}*.\n+{points} points! 🎉",
                parse_mode="Markdown"
            )
            return

        # Lose?
        if data["wrong"] >= data["max_wrong"]:
            answer = data["answer"].upper()
            ACTIVE_GAMES.pop(user_id)
            await update.message.reply_text(
                f"💀 Game over! The word was *{answer}*.\nTry again with /hangman.",
                parse_mode="Markdown"
            )
            return

        await update.message.reply_text(render_hangman(data), parse_mode="Markdown")

    # ----- Wordle -----
    elif mode == "wordle":
        guess = text.lower()
        if len(guess) != 5 or not guess.isalpha():
            await update.message.reply_text("Please send a 5-letter word (A-Z only).")
            return
        feedback = score_guess(data["answer"], guess)
        data["guesses"].append((guess, feedback))

        if guess == data["answer"]:
            points = 20
            add_score(user_id, user.username or user.first_name, points)
            ACTIVE_GAMES.pop(user_id)
            await update.message.reply_text(
                f"✅ Excellent! The word was *{data['answer'].upper()}*.\n+{points} points! 🎉",
                parse_mode="Markdown"
            )
            return

        if len(data["guesses"]) >= data["max_guesses"]:
            answer = data["answer"].upper()
            ACTIVE_GAMES.pop(user_id)
            await update.message.reply_text(
                f"💀 Out of tries! The word was *{answer}*.\nTry again with /wordle.",
                parse_mode="Markdown"
            )
            return

        await update.message.reply_text(render_wordle(data), parse_mode="Markdown")


# ---------- Main ----------
def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Please set the TELEGRAM_BOT_TOKEN environment variable.")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("scramble", start_scramble))
    application.add_handler(CommandHandler("hangman", start_hangman))
    application.add_handler(CommandHandler("wordle", start_wordle))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("quit", quit_game))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess)
    )

    logger.info("World Puzzle Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
