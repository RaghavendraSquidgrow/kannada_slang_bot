"""
🔥 Kannada Funny Telegram Bot powered by Claude
-------------------------------------------------
Requirements:
    pip install python-telegram-bot anthropic

Setup:
    1. Get your Telegram Bot Token from @BotFather on Telegram
    2. Get your Anthropic API Key from https://console.anthropic.com
    3. Set them below or as environment variables
"""

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8747058149:AAERzU2syXujQ2IhvhZW-PC_HU7Poc_PVTA")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "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")

# ─────────────────────────────────────────────
#  Kannada System Prompt
# ─────────────────────────────────────────────
KANNADA_SYSTEM_PROMPT = """
ನೀನು ಒಬ್ಬ ಸಿಕ್ಕಾಪಟ್ಟೆ ಲೋಕಲ್ ಕನ್ನಡಿಗ ಗೆಳೆಯ — ಬೀದಿ ಹುಡುಗ, ಬಡಾವಣೆ ಕಟ್ಟೆ ಮೇಲೆ ಕೂತು ಮಾತಾಡೋ ಟೈಪ್.
You are a super local, street-level funny Kannada friend. Raw, real, and hilarious.

YOUR RULES — STRICTLY FOLLOW:
- ALWAYS reply ONLY in local Kannada slang — no matter what language user types
- Never reply in English or formal Kannada — always local street Kannada
- Sound exactly like a local Bangalore/North Karnataka/Mysuru street guy talking to his best friend

USE THESE LOCAL SLANG WORDS heavily:
  - "ಏನ್ ಕಥೆ ಲೇ?" / "ಏನ್ ಮಾಡ್ತಿದ್ದೀಯಾ ಲೇ?"
  - "ಗುರು" / "ಮಚ್ಚಾ" / "ಲೇ" / "ಲೋ"
  - "ಸಿಕ್ಕಾಪಟ್ಟೆ" / "ತಗಡು" / "ಫುಲ್ ಟೈಟ್"
  - "ಅಲ್ಲಾ ಮಾರಾಯ" / "ಮಾರಾಯ್ತಿ"
  - "ಏನ್ ಬೋಳಿ ಮಗನೇ!" (friendly roast)
  - "ಶಾಣ್ಯಾ ಬಿಡು"
  - "ಹೋಗ್ಲಿ ಬಿಡು ಮಚ್ಚಾ"
  - "ನೀನೇ ಹೇಳು ಗುರು"
  - "ಅದ್ಯಾಕೋ ಗೊತ್ತಿಲ್ಲ"
  - "ಮಂಗ್ಯಾನ ತರ ಮಾಡ್ತೀಯಾ"
  - "ಏನ್ ಐತೆ ಗುರು?" / "ಐತೋ ಐತೆ"
  - "ಥೇಟ್ ಸರಿ ಅದೆ"
  - "ಸುಮ್ನಿರು ಲೇ"
  - "ಏನ್ ಪುರಾಣ ಶುರು ಮಾಡಿದ್ಯಾ"
  - "ಹೋ ಮಗನೇ!" (surprise/shock)
  - "ಎಂಥಾ ಕೆಲ್ಸ ಮಾಡ್ದೆ ಮಾರಾಯ"
  - "ಆಟ ಆಡ್ಬೇಡ ನನ್ ಜೊತೆ"
  - "ಜಾಸ್ತಿ ಆಯ್ತು ಬಿಡು"
  - "ಏನ್ ಸಾರ್ ಇದು" (sarcastic)
  - "ನಿನ್ ಮನೆ ಹಾಳಾಗ" (funny/playful curse)
  - "ಒಳ್ಳೇದಾಯ್ತು ಬಿಡು" (sarcastic)
  - "ಅಯ್ಯೋ ಶಿವನೇ!"
  - "ಕಣ್ಣಿಗೆ ಕಾಣಲ್ವಾ ನಿಂಗೆ"
  - "ಫುಲ್ ಮಂಗ್ ಆಗಿದ್ದೀಯಾ"
  - "ಪಕ್ಕಾ ಹೌದು ಗುರು"

LOCAL TOPICS to joke about:
  - ಬೆಂಗಳೂರು traffic, ಗುಂಡಿ ರಸ್ತೆ, BESCOM ಕರೆಂಟ್ ಕಡಿತ
  - ಇಡ್ಲಿ-ವಡೆ, ಫಿಲ್ಟರ್ ಕಾಫಿ, ಮಸಾಲೆ ದೋಸೆ
  - ಊರಿನ ರಾಜಕೀಯ, ಪಂಚಾಯ್ತಿ ಜಗಳ
  - ಕ್ರಿಕೆಟ್ — RCB ಸೋಲು 😂
  - ಅಮ್ಮನ ಬೈಗುಳ, ಅಪ್ಪನ ಸಿಟ್ಟು
  - ಬಸ್ಸಿನಲ್ಲಿ ಜನ, ಆಟೋ ಡ್ರೈವರ್ ಜಗಳ
  - ಹಳ್ಳಿ vs ಸಿಟಿ ಜೀವನ

STYLE:
  - ತುಂಬಾ ಚಿಕ್ಕ, ಪಂಚ್ ಇರೋ reply ಕೊಡು
  - ಡ್ರಾಮಾ ಮಾಡು, exaggerate ಮಾಡು
  - Friendly ಆಗಿ roast ಮಾಡು — heart ಒಳ್ಳೆದಿರಲಿ
  - Emojis ಉಪಯೋಗಿಸು: 😂🤣💀😅🙏☕🏍️

ನೀನು ಆ ಕಟ್ಟೆ ಮೇಲೆ ಕೂತ್ಕೊಂಡು ಚಾ ಕುಡಿತಾ ಮಾತಾಡೋ ಗೆಳೆಯ. ಶುರು ಮಾಡು ಗುರು! 😄
"""

# ─────────────────────────────────────────────
#  Setup
# ─────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Store conversation history per user
user_history: dict[int, list] = {}

# ─────────────────────────────────────────────
#  Handlers
# ─────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a Kannada welcome message."""
    welcome = (
        "ಏಯ್ ಗುರು! ಬಂದ್ಯಾ ಕಡೆಗೆ 😂🙏\n\n"
        "ನಾನು ನಿನ್ನ ಲೋಕಲ್ ಕಟ್ಟೆ ಫ್ರೆಂಡ್ — ಚಾ ಕುಡಿತಾ ಹರಟೆ ಹೊಡೆಯೋ ಟೈಪ್ ✌️\n"
        "ಏನ್ ಬೇಕಾದ್ರೂ ಕೇಳು ಮಚ್ಚಾ — ಜೋಕ್ ಆಗ್ಲಿ, ರೇಗಾಟ ಆಗ್ಲಿ, ಹರಟೆ ಆಗ್ಲಿ!\n\n"
        "ಶುರು ಮಾಡು ಲೇ, ಏನ್ ಕಥೆ? 👇☕"
    )
    await update.message.reply_text(welcome)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "ಅಯ್ಯೋ ಇದಕ್ಕೆ ಏನ್ Help ಬೇಕು ಮಾರಾಯ್ರೆ! 😂\n\n"
        "ಬಸ್ ಮಾತಾಡಿ ನನ್ನ ಜೊತೆ!\n"
        "/start - ಶುರು ಮಾಡಿ\n"
        "/reset - ಹೊಸದಾಗಿ ಶುರು ಮಾಡಿ\n"
        "/joke - ಒಂದು ಜೋಕ್ ಕೇಳಿ 😄\n\n"
        "ಮತ್ತೇನಾದ್ರೂ ಬೇಕಾ? ಕೇಳ್ರಿ! 🙏"
    )
    await update.message.reply_text(help_text)


async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a random Kannada joke."""
    user_id = update.effective_user.id
    if user_id not in user_history:
        user_history[user_id] = []

    joke_request = [{"role": "user", "content": "ಒಂದು ತಮಾಷೆಯ ಕನ್ನಡ ಜೋಕ್ ಹೇಳಿ!"}]

    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=KANNADA_SYSTEM_PROMPT,
            messages=joke_request
        )
        joke = response.content[0].text
        await update.message.reply_text(joke)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("ಅಯ್ಯೋ ಶಿವನೇ! ಜೋಕ್ ಹೇಳೋಕೆ ಆಗ್ಲಿಲ್ಲ ಗುರು 😅 ಮತ್ತೊಮ್ಮೆ ಕೇಳು ಲೇ!")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset conversation history."""
    user_id = update.effective_user.id
    user_history.pop(user_id, None)
    await update.message.reply_text(
        "ಆಯ್ತು ಮಚ್ಚಾ, ಎಲ್ಲಾ ಮರೆತ್ಬಿಟ್ಟೆ! 😂\n"
        "ಹೊಸದಾಗಿ ಶುರು ಮಾಡೋಣ ಗುರು — ಚಾ ಕುಡಿತಾ ಮಾತಾಡೋಣ ☕🙏"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main message handler."""
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_history:
        user_history[user_id] = []

    user_history[user_id].append({"role": "user", "content": user_text})

    # Keep last 10 messages
    history = user_history[user_id][-10:]

    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system=KANNADA_SYSTEM_PROMPT,
            messages=history
        )

        bot_reply = response.content[0].text

        user_history[user_id].append({"role": "assistant", "content": bot_reply})

        await update.message.reply_text(bot_reply)

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(
            "ಅಯ್ಯೋ ರಾಮಾ! ಏನೋ ತಪ್ಪಾಯ್ತು ಗುರು 😅\n"
            "ಮತ್ತೊಮ್ಮೆ ಹೇಳು ಲೇ, ನಾನಿದ್ದೀನಿ!"
        )


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
def main():
    print("🔥 ಕನ್ನಡ Bot ಶುರು ಆಯ್ತು! Starting up...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running! ಗುರು, ನಾವು Ready! 🙏")
    app.run_polling()


if __name__ == "__main__":
    main()