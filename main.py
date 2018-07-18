#! /bin/python3
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from config import TOKEN
from commands import start, button

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)

button_handler = CallbackQueryHandler(button)
dispatcher.add_handler(button_handler)

updater.start_polling()
