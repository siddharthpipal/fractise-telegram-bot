import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackContext

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Predefined knowledge about Fractise
FRACTISE_INFO = """
Fractise is a blockchain-based platform for fractional ownership of various assets, including real estate, luxury assets, and startups. 
It utilizes a native token for transactions, staking, and rewards. The platform offers investment opportunities by breaking down high-value assets into tokenized shares.
"""

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    # Prepare prompt
    messages = [
        {"role": "system", "content": "You are an expert assistant for Fractise, a fractional ownership platform."},
        {"role": "user", "content": f"{FRACTISE_INFO}\n\nUser: {user_message}"}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )
        ai_reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        ai_reply = "An error occurred while processing your request. Please try again later."

    await update.message.reply_text(ai_reply)

# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am the Fractise AI Bot. Ask me anything about Fractise.")

# Bot setup
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Start polling
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
