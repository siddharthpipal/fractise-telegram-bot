import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackContext

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Predefined knowledge about Fractise
FRACTISE_INFO = """
Fractise is a blockchain-based platform for fractional ownership of various assets, including real estate, luxury assets, and startups. 
It utilizes a native token for transactions, staking, and rewards. The platform offers investment opportunities by breaking down high-value assets into tokenized shares.
"""

# Handle incoming messages
async def handle_message(update: Update, context: CallbackContext):
    if update.message:
        user_message = update.message.text
        print(f"Received message: {user_message}")  # Debugging log

        # Prepare OpenAI request
        messages = [
            {"role": "system", "content": "You are an expert assistant for Fractise, a fractional ownership platform."},
            {"role": "user", "content": f"{FRACTISE_INFO}\n\nUser: {user_message}\nAI:"}
        ]

        try:
            # Call OpenAI API using the correct method
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=messages
            )

            ai_reply = response.choices[0].message.content
            print(f"OpenAI response: {ai_reply}")  # Debugging log

            await update.message.reply_text(ai_reply)

        except Exception as e:
            print(f"OpenAI Error: {e}")  # Debugging log
            await update.message.reply_text("An error occurred while processing your request. Please try again later.")

# Start command handler
async def start(update: Update, context: CallbackContext):
    print("Bot started")  # Debugging log
    await update.message.reply_text("Hello! I am the Fractise AI Bot. Ask me anything about Fractise.")

# Bot setup
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Start polling
print("Bot is running...")
app.run_polling()
