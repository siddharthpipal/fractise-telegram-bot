import logging
import openai
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Your Telegram bot token
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Your OpenAI API key

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm the Fractise AI bot. Ask me anything about Fractise!")

# Help command
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Just type a message, and I'll reply with an AI-generated response.")

# Generate AI response
def get_ai_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        return "Sorry, I couldn't process your request."

# Handle messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    chat_id = update.message.chat.id

    logger.info(f"Received message from {chat_id}: {user_message}")

    # Generate AI response
    ai_response = get_ai_response(user_message)

    # Send response
    await update.message.reply_text(ai_response)

# Error handler
async def error(update: Update, context: CallbackContext):
    logger.error(f"Update {update} caused error {context.error}")

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    logger.info("Bot is running...")
    app.run
