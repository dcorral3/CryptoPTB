from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from config import TOKEN
from controller import Controller

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
controller = Controller()

start_handler = CommandHandler('start', controller.start)
dispatcher.add_handler(start_handler)

button_handler = CallbackQueryHandler(controller.button)
dispatcher.add_handler(button_handler)

text_handler = MessageHandler(Filters.text, controller.textMessages)
dispatcher.add_handler(text_handler)

updater.start_polling()
