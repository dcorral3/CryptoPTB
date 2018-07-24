from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from config import TOKEN
from controller import Controller

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
controller = Controller()

start_handler = CommandHandler('start', controller.start)
dispatcher.add_handler(start_handler)

add_coin_handler = CommandHandler('add_coin', controller.add_coin)
dispatcher.add_handler(add_coin_handler)

button_handler = CallbackQueryHandler(controller.button)
dispatcher.add_handler(button_handler)

updater.start_polling()
