import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment variable (secure for Railway)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN set in environment variables")

async def start(update: Update, context):
    """Send a welcome message when /start is issued."""
    await update.message.reply_text(
        "🔄 *Text Reverser Bot*\n\n"
        "Send me any text and I'll reverse it for you!\n\n"
        "Examples:\n"
        "• `Hello` → `olleH`\n"
        "• `Telegram` → `margeleT`\n"
        "• `Hello world` → `dlrow olleH`\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/help - Get help\n"
        "/about - About this bot",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context):
    """Send a help message when /help is issued."""
    await update.message.reply_text(
        "📖 *Help*\n\n"
        "Just send me any text message and I'll reverse it.\n"
        "I reverse entire sentences too!\n\n"
        "Examples:\n"
        "`Hello` → `olleH`\n"
        "`Hello world` → `dlrow olleH`\n"
        "`123 abc` → `cba 321`\n\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - This help menu\n"
        "/about - About this bot",
        parse_mode="Markdown"
    )

async def about_command(update: Update, context):
    """Send an about message when /about is issued."""
    await update.message.reply_text(
        "🤖 *Text Reverser Bot v1.0*\n\n"
        "A simple bot that reverses any text you send.\n"
        "100% free, no registration needed.\n\n"
        "⚡ Features:\n"
        "• Reverse any text instantly\n"
        "• Works with emojis and special characters\n"
        "• No API keys required\n\n"
        "Built with ❤️ using python-telegram-bot",
        parse_mode="Markdown"
    )

async def reverse_text(update: Update, context):
    """Reverse any text message."""
    # Get the user's message
    original = update.message.text
    
    # Reverse the text
    reversed_text = original[::-1]
    
    # Send the result
    await update.message.reply_text(
        f"🔄 *Original:*\n`{original}`\n\n"
        f"⬅️ *Reversed:*\n`{reversed_text}`",
        parse_mode="Markdown"
    )

async def error_handler(update: Update, context):
    """Log errors."""
    logger.warning(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Create the application
    app = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    
    # Add handler for all text messages (except commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reverse_text))
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("🤖 Bot is starting with long polling...")
    print("🤖 Bot is starting with long polling...")
    
    # Run the bot (this blocks until stopped)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
