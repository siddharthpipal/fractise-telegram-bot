import os
import logging
import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai

# === Configuration ===
# Environment variables (set these in Railway)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # This should be the group chat ID

# Configure logging to help with debugging and monitoring.
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# === Command Handlers ===
async def start(update: Update, context: CallbackContext) -> None:
    """
    Send a welcome message when a user sends the /start command.
    """
    await update.message.reply_text(
        "Hello! I'm the Fractise AI Bot. Ask me anything about Fractise and I'll do my best to help!"
    )

async def chat(update: Update, context: CallbackContext) -> None:
    """
    Process incoming text messages by sending the content to the OpenAI API and returning the generated response.
    """
    user_message = update.message.text
    try:
        # Call the OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant for the Fractise project. Provide helpful and detailed answers."
                },
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response["choices"][0]["message"]["content"]
        await update.message.reply_text(bot_response)
    except Exception as e:
        logger.error(f"OpenAI API Error: {e}")
        await update.message.reply_text("Sorry, I couldn't process your request at the moment.")

# === Scheduled Engagement Messages ===
async def send_engagement_message(context: CallbackContext) -> None:
    """
    Periodically send engagement messages to the Fractise group to stimulate conversation.
    """
    messages = [
        "🔥 Have you checked out the latest Fractise updates? Ask me anything!",
        "💡 Did you know? Fractise enables fractional ownership of diverse asset types!",
        "🚀 Join the discussion! How do you think blockchain can improve asset ownership?"
    ]
    message = random.choice(messages)
    try:
        await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        logger.error(f"Failed to send engagement message: {e}")

# === Main Function to Run the Bot ===
async def main():
    """
    Build and run the Telegram bot application.
    """
    # Build the application using the bot token
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Schedule the engagement messages to run every 6 hours (21600 seconds)
    job_queue = app.job_queue
    job_queue.run_repeating(send_engagement_message, interval=21600, first=10)

    logger.info("Fractise AI Bot is running 24/7...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
