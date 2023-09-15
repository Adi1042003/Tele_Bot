from typing import Final # pip install python-telegram-bot
from random import choice
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import datetime

print('Starting up bot...')

TOKEN: Final = 'ADD_TOKEN_HERE'
BOT_USERNAME: Final = 'BOT_USERNAME'


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello there! I\'m {BOT_USERNAME}. What\'s up?')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')


def handle_response(text: str) -> str:
    # Create your own response logic
    processed: str = text.lower()
    x = ['hello','hi','hi there',f'Namaste mera naam {BOT_USERNAME} hai','hello','annyeong-haseyo']
    if processed in x:
        reply1=choice(x)
        return reply1

    if 'how are you' in processed:
        return 'I\'m good!'

    if 'i love you' in processed:
        return 'I love You!'

    if 'what is your age' in processed:
        return 'Age is simply the number of years the world has been enjoying you!'

    if 'stop' in processed:
        exit()

    return 'I don\'t understand'

    if 'what is the current time' in processed:
        x=datetime.datetime.now()
        return x.strftime("%Y-%m-%d %H:%M:%S")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text
    first_name: str = update.message.from_user.first_name
    last_name: str = update.message.from_user.last_name

    # Print a log for debugging
    print(f'User ({first_name} {last_name}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print(f'{BOT_USERNAME}:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Checking for new commands')
    # Run the bot
    app.run_polling(poll_interval=5)




