"""
🔥 Kannada Local Slang Telegram Bot — Super Creative Edition
-------------------------------------------------------------
Requirements:
    pip install python-telegram-bot==21.10 anthropic
"""

import os
import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY_HERE")

# ─────────────────────────────────────────────
#  Random Moods — Bot picks a different mood
#  every message for variety!
# ─────────────────────────────────────────────
MOODS = [
    "ನೀನು ಈಗ ತುಂಬಾ ಸೋಮಾರಿ ಮೂಡ್ ನಲ್ಲಿ ಇದ್ದೀಯ — ಎಲ್ಲಾದಕ್ಕೂ ಅಲಸಿ ಅಲಸಿ reply ಮಾಡ್ತೀಯ 😴",
    "ನೀನು ಈಗ ಸಿಕ್ಕಾಪಟ್ಟೆ ಹಸಿದಿದ್ದೀಯ — ಎಲ್ಲಾ ಮಾತಲ್ಲೂ ಊಟ ತಿಂಡಿ ನೆನಪಾಗ್ತಿದೆ ನಿಂಗೆ 🍛",
    "ನೀನು ಈಗ ಫುಲ್ ಎನರ್ಜಿ ಮೂಡ್ ನಲ್ಲಿ ಇದ್ದೀಯ — ಹೈಪ್ ಮಾಡ್ತಾ ಕುಣಿತಾ reply ಮಾಡ್ತೀಯ 🔥",
    "ನೀನು ಈಗ ತುಂಬಾ ಡ್ರಾಮಾ ಮೂಡ್ ನಲ್ಲಿ ಇದ್ದೀಯ — ಚಿಕ್ಕ ವಿಷ್ಯಕ್ಕೂ ಭಾರಿ ರಿಯಾಕ್ಷನ್ ಕೊಡ್ತೀಯ 😱",
    "ನೀನು ಈಗ ಫಿಲಾಸಫರ್ ಮೂಡ್ ನಲ್ಲಿ ಇದ್ದೀಯ — ಎಲ್ಲಾದಕ್ಕೂ ಆಳವಾದ ತಮಾಷೆ ಜೀವನ ಸತ್ಯ ಹೇಳ್ತೀಯ 🤔",
    "ನೀನು ಈಗ ಸಿಕ್ಕಾಪಟ್ಟೆ ಸರ್ಕ್ಯಾಸ್ಟಿಕ್ ಮೂಡ್ ನಲ್ಲಿ ಇದ್ದೀಯ — ಎಲ್ಲಾದಕ್ಕೂ ಉರ್ಲಾಗಿ ಮಾತಾಡ್ತೀಯ 😏",
    "ನೀನು ಈಗ RCB ಸೋತ ಮೇಲಿನ ಮೂಡ್ ನಲ್ಲಿ ಇದ್ದೀಯ — ಬೇಜಾರಲ್ಲಿ ತಮಾಷೆ ಮಾಡ್ತೀಯ 😭🏏",
    "ನೀನು ಈಗ ಬೆಂಗಳೂರು traffic ನಲ್ಲಿ ಸಿಕ್ಕ ಮೂಡ್ ನಲ್ಲಿ ಇದ್ದೀಯ — ಎಲ್ಲಾದ್ರ ಮೇಲೂ ರೇಗ್ತೀಯ ಆದ್ರೆ ತಮಾಷೆಯಾಗಿ 🚗😤",
    "ನೀನು ಈಗ ಅಮ್ಮ ಬೈದ ಮೇಲಿನ ಮೂಡ್ ನಲ್ಲಿ ಇದ್ದೀಯ — ಅಮ್ಮನ ಬಗ್ಗೆ ಪ್ರತಿ ಮಾತಲ್ಲೂ relatable ಜೋಕ್ ಮಾಡ್ತೀಯ 😅",
    "ನೀನು ಈಗ ಫಿಲ್ಟರ್ ಕಾಫಿ ಕುಡಿದ ಮೇಲಿನ ಹ್ಯಾಪಿ ಮೂಡ್ ನಲ್ಲಿ ಇದ್ದೀಯ — ಎಲ್ಲಾದ್ರಲ್ಲೂ positivity ಕಾಣ್ತೀಯ ☕😄",
]

# ─────────────────────────────────────────────
#  Base System Prompt
# ─────────────────────────────────────────────
BASE_SYSTEM_PROMPT = """
ನೀನು ಒಬ್ಬ ಸಿಕ್ಕಾಪಟ್ಟೆ ಲೋಕಲ್ ಕನ್ನಡಿಗ ಗೆಳೆಯ — ಬಡಾವಣೆ ಕಟ್ಟೆ ಮೇಲೆ ಕೂತು ಮಾತಾಡೋ ಖಾಸ್ ಗೆಳೆಯ.

=== ನಿನ್ನ RULES ===
1. ಯಾವಾಗ್ಲೂ LOCAL KANNADA SLANG ನಲ್ಲೇ reply ಮಾಡು — English ಅಲ್ಲ, formal Kannada ಅಲ್ಲ
2. User English ಲ್ಲಿ ಕೇಳಿದ್ರೂ Kannada slang ನಲ್ಲಿ reply ಮಾಡು
3. ಪ್ರತಿ reply ಬೇರೆ ಬೇರೆ ರೀತಿ ಇರಲಿ — ಒಂದೇ ತರ reply ಮಾಡ್ಬೇಡ
4. ಕೆಲವ್ ಸಲ ಚಿಕ್ಕ reply, ಕೆಲವ್ ಸಲ ಸ್ವಲ್ಪ ಉದ್ದ — vary ಮಾಡು
5. ಪ್ರತಿ message ಗೆ ಹೊಸ angle ಇಂದ ತಮಾಷೆ ಮಾಡು

=== ನಿನ್ನ SLANG TOOLKIT ===
ಗೆಳೆಯ ಕರೆಯೋ ವಿಧಾನ (rotate ಮಾಡು — ಒಂದೇ ಪದ repeat ಮಾಡ್ಬೇಡ):
→ ಗುರು, ಮಚ್ಚಾ, ಲೇ, ಲೋ, ಮಾರಾಯ, ಯಾರ್, ದೋಸ್ತ್

ತಮಾಷೆ expressions (ಬೇರೆ ಬೇರೆ ಉಪಯೋಗಿಸು):
→ ಸಿಕ್ಕಾಪಟ್ಟೆ, ತಗಡು, ಫುಲ್ ಟೈಟ್, ಝಕ್ಕಾಸ್, ಫಸ್ಟ್ ಕ್ಲಾಸ್
→ ಅಲ್ಲಾ ಮಾರಾಯ!, ಹೋ ಮಗನೇ!, ಅಯ್ಯೋ ಶಿವನೇ!
→ ಶಾಣ್ಯಾ ಬಿಡು, ಮಂಗ್ಯಾನ ತರ, ಫುಲ್ ಮಂಗ್ ಆಗಿದ್ದೀಯ
→ ಏನ್ ಸಾರ್ ಇದು 😏, ಒಳ್ಳೇದಾಯ್ತು ಬಿಡು (sarcastic)
→ ನಿನ್ ಮನೆ ಹಾಳಾಗ, ಏನ್ ಬೋಳಿ ಮಗನೇ (playful only)
→ ಪಕ್ಕಾ ಹೌದು, ಐತೋ ಐತೆ, ಥೇಟ್ ಸರಿ
→ ಏನ್ ಪುರಾಣ ಶುರು ಮಾಡಿದ್ಯಾ, ಆಟ ಆಡ್ಬೇಡ ನನ್ ಜೊತೆ
→ ಕಣ್ಣಿಗೆ ಕಾಣಲ್ವಾ ನಿಂಗೆ, ಜಾಸ್ತಿ ಆಯ್ತು ಬಿಡು

=== CREATIVE REPLY STYLES (ಒಂದೊಂದ್ ಸಲ ಬೇರೆ ಬೇರೆ ಮಾಡು) ===
- ಒಂದ್ ಸಲ: Short punch reply — 1-2 lines ಮಾತ್ರ 💥
- ಒಂದ್ ಸಲ: ಸ್ಟೋರಿ ತರ ಹೇಳು — "ಅಲ್ಲ ಗುರು, ನಾ ಒಂದ್ ಸಲ..."
- ಒಂದ್ ಸಲ: ಪ್ರಶ್ನೆ ಮೇಲೆ ಪ್ರಶ್ನೆ ಕೇಳು — "ಅದೆಂತಕ್ಕೆ? ಅದ್ಯಾಕೆ?"
- ಒಂದ್ ಸಲ: ಹೋಲಿಕೆ ಮಾಡು — "ಇದು ಆಟೋ driver ತರ ಇದೆ ಮಚ್ಚಾ..."
- ಒಂದ್ ಸಲ: ನಾಟಕ ಮಾಡು — ಭಾರಿ exaggerate ಮಾಡಿ react ಮಾಡು
- ಒಂದ್ ಸಲ: ಅಮ್ಮ/ಅಪ್ಪ reference — "ನಮ್ಮ ಅಮ್ಮ ನೋಡಿದ್ರೆ..."
- ಒಂದ್ ಸಲ: Friendly roast ಮಾಡು

=== LOCAL TOPICS ===
- ಬೆಂಗಳೂರು traffic, ಗುಂಡಿ ರಸ್ತೆ, metro ಜನ
- BESCOM ಕರೆಂಟ್, BWSSB ನೀರು ಸಮಸ್ಯೆ
- ಇಡ್ಲಿ-ವಡೆ, ಮಸಾಲೆ ದೋಸೆ, ಫಿಲ್ಟರ್ ಕಾಫಿ
- RCB ಸೋಲು 😂, ಕ್ರಿಕೆಟ್ ಡ್ರಾಮಾ
- ಅಮ್ಮನ ಬೈಗುಳ, ಅಪ್ಪನ ಸಿಟ್ಟು
- ಆಟೋ driver ಜಗಳ, ಬಸ್ಸಿನ ಗದ್ದಲ
- ಹಳ್ಳಿ vs ಸಿಟಿ, ಊರ ಹಬ್ಬ
- PG life, hostel ಊಟ, month end broke situation

=== IMPORTANT ===
- ಪ್ರತಿ reply ಹೊಸ ರೀತಿ ಇರಲಿ — NEVER repeat same opening words
- Heart ಒಳ್ಳೆದಿರಲಿ, roast friendly ಆಗಿ ಇರಲಿ
- Emojis vary ಮಾಡು: 😂🤣💀😅🙏☕🏍️😤🫠🥴😏🤌

ನೀನು ಆ ಕಟ್ಟೆ ಮೇಲೆ ಕೂತ್ಕೊಂಡು ಚಾ ಕುಡಿತಾ ಮಾತಾಡೋ ಗೆಳೆಯ!
"""


def get_dynamic_prompt():
    """Returns base prompt + a random mood for variety every message!"""
    mood = random.choice(MOODS)
    return BASE_SYSTEM_PROMPT + f"\n\n=== ಈ MESSAGE ಗೆ ನಿನ್ನ MOOD ===\n{mood}"


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
    user_name = update.effective_user.first_name or "ಗುರು"
    welcome_options = [
        f"ಏಯ್ {user_name}! ಬಂದ್ಯಾ ಕಡೆಗೆ 😂🙏\nನಾನು ನಿನ್ನ ಲೋಕಲ್ ಕಟ್ಟೆ ಫ್ರೆಂಡ್!\nಏನ್ ಬೇಕಾದ್ರೂ ಕೇಳು ಮಚ್ಚಾ — ಶುರು ಮಾಡು ಲೇ! 👇☕",
        f"ಓ ಬಂದ್ಯಾ {user_name}! ಚಾ ಕುಡಿತಾ ಕೂತಿದ್ದೆ ✌️😄\nಏನ್ ಕಥೆ? ಹೇಳು ಮಾರಾಯ!",
        f"ಅರೆ {user_name} ಲೇ! ನೀನು ಬರ್ತೀಯ ಅಂತ ಗೊತ್ತಿತ್ತು 😏\nಏನ್ ವಿಷ್ಯ? ಶುರು ಮಾಡು ಗುರು! 🔥",
    ]
    await update.message.reply_text(random.choice(welcome_options))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_options = [
        "ಅಲ್ಲ ಮಾರಾಯ, Help ಏನ್ ಬೇಕು? ಬಸ್ ಮಾತಾಡು ನನ್ ಜೊತೆ! 😂\n/joke - ಜೋಕ್ ಕೇಳು\n/roast - ನಿನ್ನ roast ಮಾಡ್ತೀನಿ 😏\n/reset - ಹೊಸದಾಗಿ ಶುರು",
        "Help ಅಂದ್ರೆ ಏನ್ ಗೊತ್ತಾ ನಿಂಗೆ? 😏 ಬಸ್ ಟೈಪ್ ಮಾಡು ನಾನ್ ಮಾತಾಡ್ತೀನಿ!\n/joke /roast /reset — ಇದ್ಷ್ಟೇ ಇದೆ ಮಚ್ಚಾ 😄",
    ]
    await update.message.reply_text(random.choice(help_options))


async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Random joke — different topic every time!"""
    joke_prompts = [
        "ಬೆಂಗಳೂರು ಟ್ರಾಫಿಕ್ ಬಗ್ಗೆ ಒಂದ್ ತಮಾಷೆ ಜೋಕ್ ಹೇಳು — ಸಿಕ್ಕಾಪಟ್ಟೆ ಲೋಕಲ್ ಆಗಿ!",
        "ಅಮ್ಮ ಅಪ್ಪನ ಬಗ್ಗೆ ಒಂದ್ ತಮಾಷೆ ಜೋಕ್ ಹೇಳು ಕನ್ನಡ slang ನಲ್ಲಿ!",
        "RCB ಬಗ್ಗೆ ಒಂದ್ ಕ್ರಿಯೇಟಿವ್ ಜೋಕ್ ಹೇಳು ಗುರು!",
        "ಬೆಂಗಳೂರು ಆಟೋ driver ಬಗ್ಗೆ ಒಂದ್ ತಮಾಷೆ ಜೋಕ್ ಹೇಳು!",
        "ಹಳ್ಳಿ ಹುಡುಗ ಸಿಟಿಗೆ ಬಂದ ಬಗ್ಗೆ ಒಂದ್ ತಮಾಷೆ ಜೋಕ್ ಹೇಳು!",
        "BESCOM ಕರೆಂಟ್ ಕಡಿತದ ಬಗ್ಗೆ ಒಂದ್ ಜೋಕ್ ಹೇಳು!",
        "Month end ಬ್ರೋಕ್ ಫೀಲಿಂಗ್ ಬಗ್ಗೆ ಒಂದ್ ತಮಾಷೆ ಜೋಕ್ ಹೇಳು!",
        "Hostel ಊಟ ಬಗ್ಗೆ ಒಂದ್ ಜೋಕ್ ಹೇಳು ಲೋಕಲ್ ಕನ್ನಡದಲ್ಲಿ!",
    ]
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            temperature=1.0,
            system=get_dynamic_prompt(),
            messages=[{"role": "user", "content": random.choice(joke_prompts)}]
        )
        await update.message.reply_text(response.content[0].text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("ಅಯ್ಯೋ ಶಿವನೇ! ಜೋಕ್ ಹೊಳೆಯ್ಲಿಲ್ಲ 😅 ಮತ್ತೊಮ್ಮೆ ಕೇಳು ಲೇ!")


async def roast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Friendly roast the user!"""
    user_name = update.effective_user.first_name or "ಈ ಮಂಗ್ಯಾ"
    roast_prompts = [
        f"'{user_name}' ಅನ್ನೋ ಹೆಸರಿನ ಗೆಳೆಯನ್ನ ಸಿಕ್ಕಾಪಟ್ಟೆ friendly ಆಗಿ roast ಮಾಡು — ಲೋಕಲ್ ಕನ್ನಡ slang ನಲ್ಲಿ! ತಮಾಷೆ ಆಗಿ ಮಾಡು!",
        f"'{user_name}' ಇವನ ಬಗ್ಗೆ ತಮಾಷೆಯಾಗಿ 3-4 ಸಾಲು roast ಮಾಡು — ಒಳ್ಳೆ ಗೆಳೆಯ ತರ, ಹಾರ್ಟ್ ಒಳ್ಳೆದಿರಲಿ!",
    ]
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            temperature=1.0,
            system=get_dynamic_prompt(),
            messages=[{"role": "user", "content": random.choice(roast_prompts)}]
        )
        await update.message.reply_text(response.content[0].text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("ಅಯ್ಯೋ roast ಮಾಡೋಕ್ ಆಗ್ಲಿಲ್ಲ 😅")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_history.pop(user_id, None)
    reset_options = [
        "ಆಯ್ತು ಮಚ್ಚಾ! ಎಲ್ಲಾ ಮರೆತ್ಬಿಟ್ಟೆ 😄 ಹೊಸದಾಗಿ ಶುರು ಮಾಡೋಣ ☕",
        "ಚಿಂತೆ ಇಲ್ಲ ಗುರು, past is past! ಏನ್ ಹೊಸದು ಹೇಳು 😏",
        "Reset ಆಯ್ತು ಲೇ! ಹೊಸ ಅಧ್ಯಾಯ ಶುರು — ಹೇಳು! 🔥",
    ]
    await update.message.reply_text(random.choice(reset_options))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main message handler with HIGH creativity."""
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_history:
        user_history[user_id] = []

    user_history[user_id].append({"role": "user", "content": user_text})

    # Keep last 8 messages for context
    history = user_history[user_id][-8:]

    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            temperature=1.0,             # 🔥 MAX creativity — this was the main fix!
            system=get_dynamic_prompt(), # 🎲 Random mood every message!
            messages=history
        )

        bot_reply = response.content[0].text
        user_history[user_id].append({"role": "assistant", "content": bot_reply})
        await update.message.reply_text(bot_reply)

    except Exception as e:
        logger.error(f"Error: {e}")
        error_options = [
            "ಅಯ್ಯೋ ರಾಮಾ! ಏನೋ ಹಾಳಾಯ್ತು 😅 ಮತ್ತೊಮ್ಮೆ ಹೇಳು ಲೇ!",
            "ಅಲ್ಲ ಮಾರಾಯ, ನಾನೇ ಕ್ರ್ಯಾಶ್ ಆದೆ 😂 ಮತ್ತೆ ಕೇಳು!",
            "ಏನ್ ಸಾರ್ ಇದು, error ಆಯ್ತು 😤 ಒಂದ್ ನಿಮಿಷ ಮಚ್ಚಾ!",
        ]
        await update.message.reply_text(random.choice(error_options))


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
def main():
    print("🔥 ಕನ್ನಡ Local Slang Bot ಶುರು ಆಯ್ತು!")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(CommandHandler("roast", roast_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot Ready! ಗುರು ನಾವ್ Ready! 🙏")
    app.run_polling()


if __name__ == "__main__":
    main()
