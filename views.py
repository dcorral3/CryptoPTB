# coding=utf-8
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from languages import LANG
import view_utils as vu
import keyboards


class ViewObject:
    def __init__(self, text=None, keyboard=None):
        self.text = text
        self.keyboard = keyboard

class View:
    def get_start(self, settings):
        keyb = keyboards.get_main_menu(settings)
        text = vu.get_text('start', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_wallet(self, command='wallet', data=None, settings=None):
        keyb = keyboards.get_wallet(command=command, data=data, settings=settings)
        text = vu.get_text(command, settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_top_10(self, command='top_10', data=None, settings=None):
        keyb = keyboards.get_top_10(command=command, data=data, settings=settings)
        text = vu.get_text(command, settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_search(self, settings):
        keyb = keyboards.get_search(settings=settings)
        text = vu.get_text('search', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_search_error(self, command=None, settings=None):
        keyb = keyboards.get_search_error(command=command, settings=settings)
        text = vu.get_text('search_error', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_settings(self, settings):
        keyb = keyboards.get_settings(settings)
        text = vu.get_text('settings', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_add_coin(self, settings):
        keyb = keyboards.get_add_coin(settings)
        text = vu.get_text('search', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_currency(self, settings):
        keyb = keyboards.get_currency(settings)
        text = vu.get_text('currency', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_languaje(self, settings):
        keyb = keyboards.get_language(settings)
        text = vu.get_text('language', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_coin(self, from_view='wallet', coin=None, settings=None, in_wallet=None):
        inline_key = []
        if settings['language'] == 'SPA':
            inline_key.append(
                [InlineKeyboardButton(text='📈 Última hora', callback_data='hour_graph ' + str(coin['symbol'])),
                 InlineKeyboardButton(text='📈 Últimas 24h', callback_data='day_graph ' + str(coin['symbol']))]
            )
            inline_key.append(
                [InlineKeyboardButton(text='📈 Última semana', callback_data='week_graph ' + str(coin['symbol'])),
                 InlineKeyboardButton(text='📈 Último mes', callback_data='month_graph ' + str(coin['symbol']))]
            )

            # añade opcion remover solo si estas en wallet
            # if from_view == "wallet":
            if in_wallet:
                inline_key.append(
                    [InlineKeyboardButton(text="Eliminar de Wallet", callback_data="remove_coin " + str(coin['symbol']))])
            else:
                inline_key.append(
                    [InlineKeyboardButton(text="Añadir a Wallet", callback_data="to_wallet " + str(coin['symbol']))])

            inline_key.append(
                [InlineKeyboardButton(text='Actualizar',
                                      callback_data='coin ' + str(coin['symbol']) + ' ' + from_view)])

            inline_key.append(self.back_buttons_esp[from_view])
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)

            positive_icon = '🔺'
            negative_icon = '🔻'

            last_1h = coin['percent_change_1h']
            if last_1h < 0:
                last_1h_icon = negative_icon
            else:
                last_1h_icon = positive_icon

            last_24h = coin['percent_change_24h']

            if last_24h < 0:
                last_24h_icon = negative_icon
            else:
                last_24h_icon = positive_icon

            last_week = coin['percent_change_7d']
            if last_week < 0:
                last_week_icon = negative_icon
            else:
                last_week_icon = positive_icon

            text = coin['name'] + ':\t' + coin['value'] + ' ' + settings['currency'] + '\n\n' \
                   + 'Última hora: ' + str(last_1h) + "%" + last_1h_icon + '\n' \
                   + 'Últimas 24 horas: ' + str(last_24h) + "%" + last_24h_icon + '\n' \
                   + 'Última semana: ' + str(last_week) + "%" + last_week_icon + '\n\n' \
                   + 'Última actualización: ' + coin['time']
        else:
            inline_key.append(
                [InlineKeyboardButton(text='📈 Last hour', callback_data='hour_graph ' + str(coin['symbol'])),
                 InlineKeyboardButton(text='📈 Last 24h', callback_data='day_graph ' + str(coin['symbol']))])

            inline_key.append([
                InlineKeyboardButton(text='📈 Last week', callback_data='week_graph ' + str(coin['symbol'])),
                InlineKeyboardButton(text='📈 Last month', callback_data='month_graph ' + str(coin['symbol']))])

            if in_wallet:
                inline_key.append(
                    [InlineKeyboardButton(text="Remove from Wallet", callback_data="remove_coin " + str(coin['symbol']))])
            else:
                inline_key.append(
                    [InlineKeyboardButton(text="Add to Wallet", callback_data="to_wallet " + str(coin['symbol']))])

            inline_key.append(
                [InlineKeyboardButton(text='Update', callback_data='coin ' + str(coin['symbol']) + ' ' + from_view)])

            inline_key.append(self.back_buttons[from_view])
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)

            positive_icon = '🔺'
            negative_icon = '🔻'

            last_1h = coin['percent_change_1h']
            if last_1h < 0:
                last_1h_icon = negative_icon
            else:
                last_1h_icon = positive_icon

            last_24h = coin['percent_change_24h']

            if last_24h < 0:
                last_24h_icon = negative_icon
            else:
                last_24h_icon = positive_icon

            last_week = coin['percent_change_7d']
            if last_week < 0:
                last_week_icon = negative_icon
            else:
                last_week_icon = positive_icon

            text = coin['name'] + ':\t' + coin['value'] + ' ' + settings['currency'] + '\n\n' \
                   + 'Last hour: ' + str(last_1h) + "%" + last_1h_icon + '\n' \
                   + 'Last 24 hour: ' + str(last_24h) + "%" + last_24h_icon + '\n' \
                   + 'Last week: ' + str(last_week) + "%" + last_week_icon + '\n\n' \
                   + 'Last update: ' + coin['time']

        return ViewObject(text=text, keyboard=keyb)

    def get_hide_button(self, settings):
        inline_key = []
        if settings['language'] == 'SPA':
            inline_key.append([InlineKeyboardButton(text='Ocultar', callback_data='hide')])
        else:
            inline_key.append([InlineKeyboardButton(text='Hide', callback_data='hide')])
        return InlineKeyboardMarkup(inline_keyboard=inline_key)

    def get_help(self):
        return ViewObject(text="help!")
