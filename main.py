from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from config import TOKEN
from controller import Controller

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
controller = Controller()

start_handler = CommandHandler('start', controller.start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', controller.help)
dispatcher.add_handler(help_handler)

add_coin_handler = CommandHandler('add_coin', controller.add_coin)
dispatcher.add_handler(add_coin_handler)

settings_handler = CommandHandler('settings', controller.settings)
dispatcher.add_handler(settings_handler)

search_coin_handler = CommandHandler('search_coin', controller.search_coin)
dispatcher.add_handler(search_coin_handler)

button_handler = CallbackQueryHandler(controller.button)
dispatcher.add_handler(button_handler)

text_handler = MessageHandler(Filters.text, controller.text_messages)
dispatcher.add_handler(text_handler)

updater.start_polling()
