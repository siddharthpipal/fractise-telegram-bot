import logging
import asyncio
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext

# Logging setup
logging.basicConfig(level=logging.INFO)

# Replace these with your actual credentials
BOT_TOKEN = "YOUR_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
GROUP_CHAT_ID = -1001234567890  # Replace with your group chat ID

# Initialize OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to generate AI responses
async def get_ai_response(text):
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are FractiseBot, a helpful assistant for the Fractise community."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return "I'm currently experiencing issues, please try again later."

# Handle messages in the group
async def handle_message(update: Update, context: CallbackContext):
    if update.message.chat_id == GROUP_CHAT_ID:
        user_message = update.message.text
        if user_message:
            bot_reply = await get_ai_response(user_message)
            await update.message.reply_text(bot_reply)

# Main function to run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(GROUP_CHAT_ID), handle_message))

    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
