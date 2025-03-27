import os
import logging
import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai

# === Configuration ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Group chat ID

# Configure logging for debugging.
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set OpenAI API key.
openai.api_key = OPENAI_API_KEY

# === Command Handlers ===
async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message on /start."""
    await update.message.reply_text(
        "Hello! I'm the Fractise AI Bot. Ask me anything about Fractise!"
    )

async def chat(update: Update, context: CallbackContext) -> None:
    """Generate and send a response using the OpenAI API."""
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant for the Fractise project. Provide detailed, helpful responses."
                },
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response["choices"][0]["message"]["content"]
        await update.message.reply_text(bot_response)
    except Exception as e:
        logger.error(f"OpenAI API Error: {e}")
        await update.message.reply_text("Sorry, I couldn't process your request at the moment.")

# === Engagement Message Scheduler using Asyncio ===
async def engagement_loop(app: Application, interval: int = 21600):
    """
    Periodically send engagement messages without using JobQueue.
    Default interval is 21600 seconds (6 hours).
    """
    messages = [
        "🔥 Have you checked out the latest Fractise updates? Ask me anything!",
        "💡 Did you know? Fractise enables fractional ownership of diverse asset types!",
        "🚀 Join the discussion! How do you think blockchain can improve asset ownership?"
    ]
    # Wait a few seconds before starting to allow the bot to be fully up.
    await asyncio.sleep(10)
    while True:
        try:
            message = random.choice(messages)
            await app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            logger.info("Engagement message sent.")
        except Exception as e:
            logger.error(f"Failed to send engagement message: {e}")
        await asyncio.sleep(interval)

# === Main Function to Run the Bot ===
async def main():
    """Build and run the Telegram bot application."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command and message handlers.
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Start the engagement message loop as a background task.
    engagement_task = asyncio.create_task(engagement_loop(app))

    logger.info("Fractise AI Bot is running 24/7...")
    # Run polling concurrently with the engagement loop.
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
