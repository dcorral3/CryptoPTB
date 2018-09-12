# coding=utf-8
import telegram

from views import View
from services import Mongodb
import view_utils as vu
import os
import errno

def clean_wallet(wallet):
    new_wallet = []
    for coin in wallet:
        if 'id' in coin:
            my_dict = {
                'id': coin['id'],
                'name': coin['name'],
                'symbol': coin['symbol']
            }
            new_wallet.append(my_dict)
        else:
            new_wallet.append(coin)
    return new_wallet

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

class Controller:

    def __init__(self):
        self.mongo = Mongodb()
        self.view  = View()

    # Commands
    def start(self, bot, update):
        user_id  = update.message.chat_id
        user     = self.mongo.get_user_id(user_id)
        settings = None

        if not user:
            wallet = []
            settings = {'language': 'ENG', 'currency': 'USD'}
        else:
            wallet = user["wallet"]
            wallet = clean_wallet(wallet)
            if 'settings' not in user:
                settings = {'language:': 'ENG', 'currency': 'USD'}
            else:
                settings = user['settings']

        self.mongo.insert_or_update_user(update.message.chat_id, wallet, settings)
        self.mongo.reset_context(user_id)
        view = self.view.get_start(settings)
        update.message.reply_text(view.text, reply_markup=view.keyboard)

    def help(self, bot, update):
        user_id = update.message.chat_id
        settings = self.mongo.get_user_settings(user_id)
        view = self.view.get_help(settings)
        update.message.reply_text(view.text, reply_markup=view.keyboard)

    def add_coin(self, bot, update):
        user_id = update.message.chat_id
        settings = self.mongo.get_user_settings(user_id)
        self.mongo.update_context(user_id, 'add_coin')
        view = self.view.get_add_coin(settings)
        update.message.reply_text(view.text, reply_markup=view.keyboard)

    def settings(self, bot, update):
        user_id = update.message.chat_id
        settings = self.mongo.get_user_settings(user_id)
        view = self.view.get_settings(settings)
        update.message.reply_text(view.text, reply_markup=view.keyboard)

    def search_coin(self, bot, update):
        user_id = update.message.chat_id
        settings = self.mongo.get_user_settings(user_id)
        self.mongo.update_context(user_id, 'search_coin')
        view = self.view.get_search(settings)
        update.message.reply_text(view.text, reply_markup=view.keyboard)

    def wallet(self, bot, update):
        user_id = update.message.chat_id
        settings = self.mongo.get_user_settings(user_id)
        data = self.mongo.get_wallet(user_id)
        view = self.view.get_wallet(command='wallet', data=data, settings=settings)
        update.message.reply_text(view.text, reply_markup=view.keyboard)

    def text_messages(self, bot, update):
        user_id = update.message.chat_id
        settings = self.mongo.get_user_settings(user_id)

        if self.mongo.is_add_coin(user_id=user_id):
            symbol = update.message.text.upper()
            try:
                if self.mongo.coin_exist(symbol):
                    coin = self.mongo.get_db_coin(symbol)
                    self.mongo.add_coin_to_user(user_id, coin)
                    data = self.mongo.get_wallet(user_id)
                    view = self.view.get_wallet(command="wallet", data=data, settings=settings)
                else:
                    view = self.view.get_search_error(command="add_coin", settings=settings)
                update.message.reply_text(view.text, reply_markup=view.keyboard)
                self.mongo.update_context(user_id, "add_coin")
            except Exception as e:
                print("EXCEPTION ADDING COIN")
                print(str(e))

        elif self.mongo.is_search(user_id=user_id):
            symbol = update.message.text.upper()
            try:
                if self.mongo.coin_exist(symbol):
                    data = self.mongo.get_coin(symbol, settings)
                    in_wallet = self.mongo.in_wallet(user_id, data)
                    view = self.view.get_coin("start", data, settings, in_wallet)
                else:
                    view = self.view.get_search_error(command="search_coin", settings=settings)
                self.mongo.update_context(user_id, "search_coin")
                update.message.reply_text(view.text, reply_markup=view.keyboard)
            except Exception as e:
                print("EXCEPTION SEARCHING")
                print(str(e))

        else:
            view = self.view.get_help(settings)
            update.message.reply_text(text=view.text)

    # Buttons
    def button(self, bot, update):
        query = update.callback_query
        command = query.data
        user_id = query.message.chat_id
        settings = self.mongo.get_user_settings(user_id)
        view = None
        if "coin" in command:
            if command == "add_coin":
                self.mongo.update_context(user_id, command)
                view = self.view.get_add_coin(settings)
            elif "cancel" in command:
                command = command.split()
                self.mongo.update_context(command=command[2], user_id=user_id)
                if command[1] == 'wallet':
                    data = self.mongo.get_wallet(user_id)
                    view = self.view.get_wallet(data=data, settings=settings)
                else:
                    view = None
            elif "remove" in command:
                command = command.split()
                symbol = command[1]
                from_view = command[2]
                coin = self.mongo.get_db_coin(symbol)
                self.mongo.remove_coin(user_id=user_id, coin=coin)
                data = self.mongo.get_coin(symbol, settings)
                view = self.view.get_coin(from_view=from_view, coin=data, settings=settings, in_wallet=False, feedback='feed_coin_removed')
            elif "search" in command:
                self.mongo.update_context(user_id, command)
                view = self.view.get_search(settings)
            else:
                command = command.split()
                coin_symbol = command[1]
                from_view = command[2]
                data = self.mongo.get_coin(coin_symbol, settings)
                in_wallet=self.mongo.in_wallet(user_id, data)
                view = self.view.get_coin(from_view=from_view, coin=data, settings=settings, in_wallet=in_wallet)
        elif "hour_graph" in command:
            graph_type = command.split()[0]
            symbol = command.split()[1]
            currency = settings['currency']
            text_title = vu.get_text('hour_graph_title', settings)
            self.save_graph(graph_type, symbol, currency, text_title, user_id)
            keyb = self.view.get_hide_button(settings)
            bot.send_photo(chat_id=user_id,
                           photo=open('graphs/' + str(user_id) + '.png', 'rb'),
                           reply_markup=keyb)
            silentremove('graphs/'+str(user_id)+'.png')
            bot.answer_callback_query(query.id)
        elif "day_graph" in command:
            graph_type = command.split()[0]
            symbol = command.split()[1]
            currency = settings['currency']
            text_title = vu.get_text('day_graph_title', settings)
            self.save_graph(graph_type, symbol, currency, text_title, user_id)
            keyb = self.view.get_hide_button(settings)
            bot.send_photo(chat_id=user_id,
                           photo=open('graphs/' + str(user_id) + '.png', 'rb'),
                           reply_markup=keyb)
            silentremove('graphs/'+str(user_id)+'.png')
            bot.answer_callback_query(query.id)
        elif "week_graph" in command:
            graph_type = command.split()[0]
            symbol = command.split()[1]
            currency = settings['currency']
            text_title = vu.get_text('week_graph_title', settings)
            self.save_graph(graph_type, symbol, currency, text_title, user_id)
            keyb = self.view.get_hide_button(settings)
            bot.send_photo(chat_id=user_id,
                           photo=open('graphs/' + str(user_id) + '.png', 'rb'),
                           reply_markup=keyb)
            silentremove('graphs/'+str(user_id)+'.png')
            bot.answer_callback_query(query.id)
        elif "month_graph" in command:
            graph_type = command.split()[0]
            symbol = command.split()[1]
            currency = settings['currency']
            text_title = vu.get_text('month_graph_title', settings)
            self.save_graph(graph_type, symbol, currency, text_title, user_id)
            keyb = self.view.get_hide_button(settings)
            bot.send_photo(chat_id=user_id,
                           photo=open('graphs/' + str(user_id) + '.png', 'rb'),
                           reply_markup=keyb)
            silentremove('graphs/'+str(user_id)+'.png')
            bot.answer_callback_query(query.id)
        elif command == 'report':
            wallet = self.mongo.get_wallet(user_id)
            coins_data = self.mongo.get_coins_data(wallet, settings)
            view_report = self.view.get_report(wallet, coins_data, settings)
            bot.send_message(chat_id=user_id, text=view_report.text, reply_markup=view_report.keyboard, parse_mode=telegram.ParseMode.HTML)
            bot.answer_callback_query(query.id)
        elif command == 'hide':
            bot.delete_message(chat_id=user_id, message_id=query.message.message_id)
        elif command == "top_10":
            data = self.mongo.get_top_10()
            view = self.view.get_top_10(command=command, data=data, settings=settings)
        elif command == "wallet":
            data = self.mongo.get_wallet(user_id)
            view = self.view.get_wallet(command=command, data=data, settings=settings)
        elif command == "settings":
            is_in_report = self.mongo.is_in_report(user_id)
            view = self.view.get_settings(settings, is_in_report=is_in_report)
        elif command == "language":
            view = self.view.get_languaje(settings)
        elif command == "currency":
            view = self.view.get_currency(settings)
        elif 'add_to_wallet' in command:
            command = command.split()
            symbol = command[1]
            from_view = command[2]
            coin = self.mongo.get_db_coin(symbol)
            self.mongo.add_coin_to_user(user_id, coin)
            data = self.mongo.get_coin(symbol, settings)
            view = self.view.get_coin(from_view=from_view, coin=data, settings=settings, in_wallet=True, feedback='feed_coin_added')
        elif 'db' in command:
            attribute = command.split()[1]
            value = command.split()[2]
            self.mongo.update_settings(user_id, attribute, value)
            settings = self.mongo.get_user_settings(user_id)
            view = self.view.get_settings(settings)
        elif command == "start" or command == "cancel_search":
            settings = self.mongo.get_user_settings(user_id)
            view = self.view.get_start(settings)
        elif command == "add_report":
            self.mongo.add_user_report(user_id)
            view = self.view.get_settings(settings=settings, is_in_report=True, feedback='feed_report_added')
        elif command == 'del_report':
            self.mongo.del_user_report(user_id)
            view = self.view.get_settings(settings=settings, is_in_report=False, feedback='feed_report_deleted')
        else:
            data = ""
        try:
            bot.edit_message_text(text=view.text, chat_id=user_id,message_id=query.message.message_id,reply_markup=view.keyboard)
        except Exception as e:
            print(str(e))
        bot.answer_callback_query(query.id, text=view.feedback)

    def save_graph(self, graph_type, symbol, currency, text_title, user_id):
        graph = self.mongo.get_graph(graph_type, symbol, currency)
        graph.title = text_title
        graph.save_graph_png(user_id)
