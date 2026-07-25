import json
import os
import threading
import logging

from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Logging sozlamasi ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --- Personajlar ma'lumotlarini yuklash ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "characters.json"), encoding="utf-8") as f:
    CHARACTERS: dict = json.load(f)

# --- Bot token ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable o'rnatilmagan!")

# ---------------------------------------------------------------------------
# Handler: /personajnomi buyrug'i
# ---------------------------------------------------------------------------
async def character_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Har qanday /buyruq uchun ishlaydi; noma'lum buyruqlarni jim o'tkazadi."""
    msg = update.effective_message
    if not msg or not msg.text:
        return

    command = msg.text.split()[0].lstrip("/").split("@")[0].lower()
    character = CHARACTERS.get(command)
    if character is None:
        return

    image = character.get("image", "")
    text = character.get("text", "")

    try:
        if image.startswith("http"):
            await msg.reply_photo(photo=image, caption=text, parse_mode="Markdown")
        elif image:
            local_path = os.path.join(BASE_DIR, image)
            with open(local_path, "rb") as img_file:
                await msg.reply_photo(photo=img_file, caption=text, parse_mode="Markdown")
        else:
            await msg.reply_text(text, parse_mode="Markdown")
    except Exception:
        logger.exception("Rasm yuborishda xato (%s), faqat matn yuborilmoqda", command)
        try:
            await msg.reply_text(text, parse_mode="Markdown")
        except Exception:
            logger.exception("Matn yuborishda ham xato (%s)", command)


# ---------------------------------------------------------------------------
# Dinamik ravishda barcha personajlar uchun handler ro'yxatdan o'tkazish
# ---------------------------------------------------------------------------
def register_handlers(app):
    for name in CHARACTERS:
        app.add_handler(CommandHandler(name, character_handler))


# ---------------------------------------------------------------------------
# Flask — Render.com health-check uchun
# ---------------------------------------------------------------------------
flask_app = Flask(__name__)

@flask_app.route("/health")
def health():
    return {"status": "ok"}, 200

@flask_app.route("/")
def index():
    return {"status": "bot is running"}, 200


def run_flask():
    port = int(os.environ.get("PORT", 8000))
    flask_app.run(host="0.0.0.0", port=port, use_reloader=False)


# ---------------------------------------------------------------------------
# Asosiy funksiya
# ---------------------------------------------------------------------------
def main():
    # Flask-ni alohida threadda ishga tushiramiz
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask health-check server ishga tushdi.")

    # Asosiy thread uchun event loop yaratamiz
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Telegram botni polling bilan ishga tushiramiz
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(application)
    logger.info("Bot polling boshlandi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
