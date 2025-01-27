import os
import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    InlineQueryHandler,
)

# Read the bot token from the environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [["/help", "/about"], ["/echo"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        f"Hello, {user.first_name}! I'm your bot. How can I help you today?",
        reply_markup=reply_markup,
    )

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Here are the commands you can use:
/start - Start the bot
/help - Show this help message
/about - Learn more about this bot
/echo <text> - Echo back the text you send
    """
    await update.message.reply_text(help_text)

# Command: /about
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
This is a simple Telegram bot created using the python-telegram-bot library.
It demonstrates basic features like commands, custom keyboards, and inline queries.
    """
    await update.message.reply_text(about_text)

# Command: /echo
async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)  # Get the text after the /echo command
    if text:
        await update.message.reply_text(f"You said: {text}")
    else:
        await update.message.reply_text("Please provide some text to echo.")

# Handle inline queries
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultArticle(
            id="1",
            title="Echo",
            input_message_content=InputTextMessageContent(f"You said: {query}"),
        )
    ]
    await update.inline_query.answer(results)

# Handle unknown commands
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry, I don't understand that command.")

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

def main():
    # Build the application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("echo", echo_command))

    # Add inline query handler
    app.add_handler(InlineQueryHandler(inline_query))

    # Add handler for unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Add error handler
    app.add_error_handler(error_handler)

    # Start the bot in polling mode
    print("Starting bot in polling mode...")
    app.run_polling()

if __name__ == "__main__":
    main()