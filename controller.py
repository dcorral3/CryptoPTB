# coding=utf-8
from views import View
from services import Mongodb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, MinuteLocator, DateFormatter, drange
from numpy import arange
import numpy as np
import os
import errno


def clean_wallet(wallet):
    new_wallet = []
    for coin in wallet:
        if 'id' in coin:
            my_dict = {'id': coin['id'], 'name': coin['name'], 'symbol': coin['symbol']}
            new_wallet.append(my_dict)
        else:
            new_wallet.append(coin)
    return new_wallet


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: 
        print(e.message)
        if e.errno != errno.ENOENT:
            raise


class Controller:

    def __init__(self):
        self.view = View()
        self.mongo = Mongodb()

    # Commands
    def start(self, bot, update):
        user_id = update.message.chat_id
        user = self.mongo.get_user_id(user_id)

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
        view = self.view.get_start(settings)
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
                self.mongo.update_context(user_id, "add_coin")
                update.message.reply_text(view.text, reply_markup=view.keyboard)
            except Exception as e:
                print("EXCEPTION ADDING COIN")
                print(str(e))

        elif self.mongo.is_search(user_id=user_id):
            symbol = update.message.text.upper()
            try:
                if self.mongo.coin_exist(symbol):
                    wallet = self.mongo.get_wallet(user_id)
                    i = 0
                    in_wallet = False
                    while i < len(wallet) and in_wallet is False:
                        if symbol == wallet[i]['symbol']:
                            in_wallet = True
                        else:
                            in_wallet = False
                        i += 1

                    data = self.mongo.get_coin(symbol, settings)
                    view = self.view.get_coin("start", data, settings, in_wallet)
                else:
                    view = self.view.get_search_error(command="search_coin", settings=settings)
                self.mongo.update_context(user_id, "search_coin")
                update.message.reply_text(view.text, reply_markup=view.keyboard)
            except Exception as e:
                print("EXCEPTION SEARCHING")
                print(str(e))

        else:
            view = self.view.get_help()
            update.message.reply_text(view.text, reply_markup=view.keyboard)

    # Buttons
    def button(self, bot, update):
        query = update.callback_query
        command = query.data
        user_id = query.message.chat_id
        old_text = query.message.text
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
                coin = self.mongo.get_db_coin(symbol)
                self.mongo.remove_coin(user_id=user_id, coin=coin)

                data = self.mongo.get_coin(symbol, settings)
                view = self.view.get_coin(coin=data, settings=settings, in_wallet=True)
            elif "search" in command:
                self.mongo.update_context(user_id, command)
                view = self.view.get_search(settings)
            else:
                command = command.split()
                coin_symbol = command[1]
                from_view = command[2]
                data = self.mongo.get_coin(coin_symbol, settings)

                wallet = self.mongo.get_wallet(user_id)

                i = 0
                in_wallet = False
                while i < len(wallet) and in_wallet is False:
                    if coin_symbol == wallet[i]['symbol']:
                        in_wallet = True
                    else:
                        in_wallet = False
                    i += 1
                view = self.view.get_coin(from_view=from_view, coin=data, settings=settings, in_wallet=in_wallet)
        elif "hour_graph" in command:
            symbol = command.split()[1]
            if settings['language'] == 'ESP':
                text_title = "Última hora"
            else:
                text_title = "Last hour"
            self.save_last_hour_graph_png(user_id, symbol, settings['currency'], text_title)
            keyb = self.view.get_hide_button(settings)
            bot.send_photo(chat_id=user_id,
                           photo=open('graphs/' + str(user_id) + '.png', 'rb'),
                           reply_markup=keyb)
            silentremove('graphs/'+str(user_id)+'.png')
        elif "day_graph" in command:
            symbol = command.split()[1]
            if settings['language'] == 'ESP':
                text_title = "Últimas 24h"
            else:
                text_title = "Last 24h"
            self.save_last_24h_graph_png(user_id, symbol, settings['currency'], text_title)
            keyb = self.view.get_hide_button(settings)
            bot.send_photo(chat_id=user_id,
                           photo=open('graphs/' + str(user_id) + '.png', 'rb'),
                           reply_markup=keyb)
            silentremove('graphs/'+str(user_id)+'.png')
        elif "week_graph" in command:
            symbol = command.split()[1]
            if settings['language'] == 'ESP':
                text_title = "Última semana"
            else:
                text_title = "Last week"
            self.save_last_week_graph_png(user_id, symbol, settings['currency'], text_title)
            keyb = self.view.get_hide_button(settings)
            bot.send_photo(chat_id=user_id,
                           photo=open('graphs/' + str(user_id) + '.png', 'rb'),
                           reply_markup=keyb)
            silentremove('graphs/'+str(user_id)+'.png')
        elif "month_graph" in command:
            symbol = command.split()[1]
            if settings['language'] == 'ESP':
                text_title = "Último mes"
            else:
                text_title = "Last month"
            self.save_last_month_graph_png(user_id, symbol, settings['currency'], text_title)
            keyb = self.view.get_hide_button(settings)
            bot.send_photo(chat_id=user_id,
                           photo=open('graphs/' + str(user_id) + '.png', 'rb'),
                           reply_markup=keyb)
            silentremove('graphs/'+str(user_id)+'.png')
        elif command == 'hide':
            bot.delete_message(chat_id=user_id,
                               message_id=query.message.message_id)
        elif command == "top_10":
            data = self.mongo.get_top_10()
            view = self.view.get_top_10(command=command, data=data, settings=settings)
        elif command == "wallet":
            data = self.mongo.get_wallet(user_id)
            view = self.view.get_wallet(command=command, data=data, settings=settings)
        elif command == "settings":
            view = self.view.get_settings(settings)
        elif command == "language":
            view = self.view.get_languaje(settings)
        elif command == "currency":
            view = self.view.get_currency(settings)
        elif 'to_wallet' in command:
            symbol = command.split()[1]
            coin = self.mongo.get_db_coin(symbol)
            self.mongo.add_coin_to_user(user_id, coin)

            data = self.mongo.get_coin(symbol, settings)
            view = self.view.get_coin(coin=data, settings=settings, in_wallet=True)
        elif 'db' in command:
            attribute = command.split()[1]
            value = command.split()[2]
            self.mongo.update_settings(user_id, attribute, value)
            settings = self.mongo.get_user_settings(user_id)
            view = self.view.get_settings(settings)
        elif command == "start" or "cancel_search":
            settings = self.mongo.get_user_settings(user_id)
            view = self.view.get_start(settings)
        else:
            data = ""

        if view is not None and old_text != view.text:
            bot.edit_message_text(text=view.text, chat_id=user_id,
                                  message_id=query.message.message_id, reply_markup=view.keyboard)
        bot.answer_callback_query(query.id)

    def save_last_hour_graph_png(self, user_id, symbol, currency, text_title):
        list_values, list_dates, max_value, min_value, max_date, min_date = \
        self.mongo.get_graph_data('hour', symbol, currency)
        fig, ax = plt.subplots()
        ax.plot(list_dates, list_values)
        plt.ylabel(currency)

        ax.xaxis.set_major_locator(MinuteLocator(interval=10))
        # range -> (0 -24) hours 6 by 6
        ax.xaxis.set_minor_locator(MinuteLocator())
        # date format in graph
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

        # beautify the x-labels
        plt.gcf().autofmt_xdate()
        plt.title(text_title + ' (' + symbol + ')')
        if not os.path.exists('graphs'):
            os.makedirs('graphs')
        fig.savefig('graphs/' + str(user_id) + '.png')
    
    def save_last_24h_graph_png(self, user_id, symbol, currency, text_title):
        list_values, list_dates, max_value, min_value, max_date, min_date = \
            self.mongo.get_graph_data('24h', symbol, currency)

        fig, ax = plt.subplots()
        ax.plot(list_dates, list_values)

        plt.ylabel(currency)

        ax.xaxis.set_major_locator(HourLocator(interval=2))
        # range -> (0 -24) hours 6 by 6
        ax.xaxis.set_minor_locator(HourLocator())
        # date format in graph
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

        # beautify the x-labels
        plt.gcf().autofmt_xdate()
        plt.title(text_title + ' (' + symbol + ')')

        if not os.path.exists('graphs'):
            os.makedirs('graphs')

        fig.savefig('graphs/' + str(user_id) + '.png')

    def save_last_week_graph_png(self, user_id, symbol, currency, text_title):
        list_values, list_dates, max_value, min_value, max_date, min_date = \
            self.mongo.get_graph_data('week', symbol, currency)

        fig, ax = plt.subplots()
        ax.plot(list_dates, list_values)

        plt.ylabel(currency)

        ax.xaxis.set_major_locator(DayLocator())
        # range -> (0h -> 24h) hours 6 by 6
        ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
        # date format in graph
        ax.xaxis.set_major_formatter(DateFormatter('%d %b'))

        # beautify the x-labels
        plt.gcf().autofmt_xdate()
        plt.title(text_title + ' (' + symbol + ')')

        if not os.path.exists('graphs'):
            os.makedirs('graphs')

        fig.savefig('graphs/' + str(user_id) + '.png')

    def save_last_month_graph_png(self, user_id, symbol, currency, text_title):
        list_values, list_dates, max_value, min_value, max_date, min_date = \
            self.mongo.get_graph_data('month', symbol, currency)

        fig, ax = plt.subplots()
        ax.plot(list_dates, list_values)

        plt.ylabel(currency)

        ax.xaxis.set_major_locator(DayLocator(arange(0, 32, 3)))
        # range -> (0 -24) hours 6 by 6
        ax.xaxis.set_minor_locator(DayLocator())
        # date format in graph
        ax.xaxis.set_major_formatter(DateFormatter('%d %b'))

        # beautify the x-labels
        plt.gcf().autofmt_xdate()
        plt.title(text_title + ' (' + symbol + ')')

        if not os.path.exists('graphs'):
            os.makedirs('graphs')

        fig.savefig('graphs/' + str(user_id) + '.png')
