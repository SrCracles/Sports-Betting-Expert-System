# 1)pip install python-telegram-bot
import collections.abc
import sys
# Fix for collections.Mapping deprecation
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

from telegram import Update
from telegram.ext import Application, CommandHandler,MessageHandler,filters,ContextTypes
from UserSessionManager import UserSessionManager
from UserSession import UserSession
TOKEN='7700764037:AAFANrfFjOhg90YbUMi8m1QeLDqDlkgl4vc'
BOT_NAME='futifu_bot'
BOT_USERNAME='@fubotero'

user_session_manager=UserSessionManager()






# /setcommands to describe commands
# COMMANDAS
async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    msg='Lets get started. I am going to ask you some questions about the football match. You are'
    msg+=str(user_id)
    print(msg)
    await update.message.reply_text(msg)


# WHEN /HELP

async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help ')

# WHEN /custom
async def custom_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Jeje')


#Handles user messages
async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_type:str=update.message.chat.type
    text:str=update.message.text
    print(f'{update.message.chat.id} in {message_type}:  {text}')
    session=user_session_manager.get_user_session(update.message.from_user.id)
    await session.handle_message(update,context)

async def error(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('STARTING BOT')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))

    app.add_handler(CommandHandler('help', help_command))

    app.add_handler(CommandHandler('custom', custom_command))

    #Messagesc
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors

    app.add_error_handler(error)


    print('POLLING....')
    app.run_polling(poll_interval=3)


