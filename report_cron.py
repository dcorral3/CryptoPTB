from telegram.ext import Updater
import telegram
from config import TOKEN
import config as conf
from pprint import pprint
from views import View
from services import Mongodb

updater = Updater(token=TOKEN)

mongo = Mongodb()
view = View()
users = mongo.get_users_report()
for user in users:
    user_id = user['_id']
    settings = mongo.get_user_settings(user_id)
    wallet = mongo.get_wallet(user_id)
    if len(wallet) > 0:
        coins_data = mongo.get_coins_data(wallet, settings)
        view_report = view.get_report(wallet, coins_data, settings)
        updater.bot.send_message(chat_id=user_id, text=view_report.text, reply_markup=view_report.keyboard, parse_mode=telegram.ParseMode.HTML)