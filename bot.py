import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID", "0").strip()

# Validate GROUP_CHAT_ID
try:
    GROUP_CHAT_ID = int(GROUP_CHAT_ID)
except ValueError:
    logging.error(f"❌ Invalid GROUP_CHAT_ID: {repr(GROUP_CHAT_ID)}")
    exit(1)

# Check for missing variables
if not BOT_TOKEN or not OPENAI_API_KEY or GROUP_CHAT_ID == 0:
    logging.error("❌ Missing required environment variables! Set BOT_TOKEN, OPENAI_API_KEY, and GROUP_CHAT_ID correctly.")
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to handle user messages
async def chat_with_ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat_id != GROUP_CHAT_ID:
        return  # Ignore messages outside the group

    user_message = update.message.text
    logging.info(f"User: {update.effective_user.first_name} → {user_message}")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        logging.error(f"❌ OpenAI API error: {e}")
        ai_reply = "Sorry, I'm having trouble responding right now."

    await update.message.reply_text(ai_reply)

# Initialize Telegram bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_ai))

logging.info("🚀 Bot is running...")
app.run_polling()
