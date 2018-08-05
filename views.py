# coding=utf-8
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class viewObject:
    def __init__(self, text=None, keyboard=None):
        self.text = text
        self.keyboard = keyboard


class View:
    back_buttons = {
        "start": [InlineKeyboardButton(text="<< Back to Main menu", callback_data='start')],
        "top_10": [InlineKeyboardButton(text='<< Back to Top 10', callback_data='top_10')],
        "wallet": [InlineKeyboardButton(text='<< Back to Wallet', callback_data='wallet')],
        "settings": [InlineKeyboardButton(text='<< Back to Settings', callback_data='settings')]
    }
    back_buttons_esp = {
        "start": [InlineKeyboardButton(text="<< Volver al Menú principal", callback_data='start')],
        "top_10": [InlineKeyboardButton(text='<< Volver al Top 10', callback_data='top_10')],
        "wallet": [InlineKeyboardButton(text='<< Volver a Wallet', callback_data='wallet')],
        "settings": [InlineKeyboardButton(text='<< Volver a Configuración', callback_data='settings')]
    }

    add_coin_button = [InlineKeyboardButton(text="Add coin", callback_data='add_coin')]
    add_coin_button_esp = [InlineKeyboardButton(text="Añadir moneda", callback_data='add_coin')]

    def __init__(self):
        self.keyboard = [[InlineKeyboardButton("💰 Wallet", callback_data='wallet'),
                          InlineKeyboardButton("🔝 Top 10", callback_data='top_10')],
                         [InlineKeyboardButton("🔍 Search coin", callback_data='search_coin'),
                          InlineKeyboardButton("⚙️ Settings", callback_data='settings')]]

        self.keyboard_esp = [[InlineKeyboardButton("💰 Wallet", callback_data='wallet'),
                              InlineKeyboardButton("🔝 Top 10", callback_data='top_10')],
                             [InlineKeyboardButton("🔍 Buscar moneda", callback_data='search_coin'),
                              InlineKeyboardButton("⚙️ Configuración", callback_data='settings')]]

    def get_start(self, settings):
        if settings['language'] == 'ESP':
            keyb = InlineKeyboardMarkup(self.keyboard_esp)
            text = "Menú principal"
        else:
            keyb = InlineKeyboardMarkup(self.keyboard)
            text = "Main Menu"
        return viewObject(text=text, keyboard=keyb)

    def get_wallet(self, command='wallet', data=None, settings=None):
        if len(data) > 3:
            keyb = self.keyboard_generator(columns=2, command=command, myList=data, settings=settings)
        else:
            keyb = self.keyboard_generator(columns=1, command=command, myList=data, settings=settings)
        text = "Wallet:"
        return viewObject(text=text, keyboard=keyb)

    def get_top_10(self, command='top_10', data=None, settings=None):
        if settings['language'] == 'ESP':
            keyb = self.keyboard_generator(columns=2, command=command, myList=data, settings=settings)
            text = "Monedas en el Top 10:"
        else:
            keyb = self.keyboard_generator(columns=2, command=command, myList=data, settings=settings)
            text = "Top 10 coins:"
        return viewObject(text=text, keyboard=keyb)

    def get_search(self, settings):
        if settings['language'] == 'ESP':
            text = 'Enviamé el nombre corto de la moneda, por favor. (e.j: BTC)'
            inline_key = [[InlineKeyboardButton(text='Cancelar', callback_data='cancel_search')]]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        else:
            text = 'Send me the coin short name, please. (e.j: BTC)'
            inline_key = [[InlineKeyboardButton(text='Cancel', callback_data='cancel_search')]]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return viewObject(text=text, keyboard=keyb)

    def get_search_error(self, command=None, settings=None):
        if settings['language'] == 'ESP':
            text = '⚠️ Oops! No he podido encontrar esa moneda.'
            inline_key = [[InlineKeyboardButton(text='Reintentar', callback_data=command)],
                          [InlineKeyboardButton(text='Cancelar', callback_data='cancel_search')]]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        else:
            text = '⚠️ Oops! I cant find this coin.'
            inline_key = [[InlineKeyboardButton(text='Retry', callback_data=command)],
                          [InlineKeyboardButton(text='Cancel', callback_data='cancel_search')]]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return viewObject(text=text, keyboard=keyb)

    def get_coin(self, from_view='wallet', coin=None, settings=None, in_wallet=None):
        inline_key = []
        if settings['language'] == 'ESP':
            inline_key.append(
                [InlineKeyboardButton(text='Actualizar', callback_data='coin ' + str(coin['symbol']) + ' ' + from_view)])

            # añade opcion remover solo si estas en wallet
            # if from_view == "wallet":
            if in_wallet:
                inline_key[0].append(
                    InlineKeyboardButton(text="Eliminar de Wallet", callback_data="remove_coin " + str(coin['symbol'])))
            else:
                inline_key[0].append(
                    InlineKeyboardButton(text="Añadir a Wallet", callback_data="to_wallet " + str(coin['symbol'])))

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
                [InlineKeyboardButton(text='Update', callback_data='coin ' + str(coin['symbol']) + ' ' + from_view)])

            # añade opcion remover solo si estas en wallet
            if from_view == "wallet":
                inline_key[0].append(
                    InlineKeyboardButton(text="Remove from Wallet", callback_data="remove_coin " + str(coin['symbol'])))

            if in_wallet:
                inline_key[0].append(
                    InlineKeyboardButton(text="Remove from Wallet", callback_data="remove_coin " + str(coin['symbol'])))
            else:
                inline_key[0].append(
                    InlineKeyboardButton(text="Add to Wallet", callback_data="to_wallet " + str(coin['symbol'])))

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

        return viewObject(text=text, keyboard=keyb)

    def get_add_coin(self, settings):
        if settings['language'] == 'ESP':
            text = 'Enviamé el nombre corto de la moneda, por favor. (e.j: BTC)'
            inline_key = [[InlineKeyboardButton(text='Cancel', callback_data='cancel wallet add_coin')]]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        else:
            text = 'Send me the coin short name, please. (e.j: BTC)'
            inline_key = [[InlineKeyboardButton(text='Cancel', callback_data='cancel wallet add_coin')]]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return viewObject(text=text, keyboard=keyb)

    def get_settings(self, settings):
        if settings['language'] == 'ESP':
            text = 'Tu configuración actual es:\n\nIdioma: ' \
                   + str(settings['language']) \
                   + '\nMoneda: ' + str(settings['currency'])
            inline_key = [[InlineKeyboardButton(text='Idioma', callback_data='language')],
                          [InlineKeyboardButton(text='Moneda', callback_data='currency')],
                          self.back_buttons_esp['start']]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        else:
            text = 'Your current settings:\n\nLanguage: ' \
                   + str(settings['language']) \
                   + '\nCurrency: ' + str(settings['currency'])
            inline_key = [[InlineKeyboardButton(text='Language', callback_data='language')],
                          [InlineKeyboardButton(text='Currency', callback_data='currency')],
                          self.back_buttons['start']]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return viewObject(text=text, keyboard=keyb)

    def get_languaje(self, settings):
        if settings['language'] == 'ESP':
            text = 'Elige el idioma en el que quieres que te hable:'
            inline_key = [[InlineKeyboardButton(text='🇬🇧 Inglés', callback_data='db language ENG'),
                           InlineKeyboardButton(text='🇪🇸 Español', callback_data='db language ESP')],
                          self.back_buttons_esp['settings']]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        else:
            text = 'Choose the language in which you want me to speak to you:'
            inline_key = [[InlineKeyboardButton(text='🇬🇧 English', callback_data='db language ENG'),
                           InlineKeyboardButton(text='🇪🇸 Spanish', callback_data='db language ESP')],
                          self.back_buttons['settings']]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return viewObject(text=text, keyboard=keyb)

    def get_currency(self, settings):
        if settings['language'] == 'ESP':
            text = 'Elige la moneda en la que quieres que te envíe los valores:'
            inline_key = [[InlineKeyboardButton(text='USD', callback_data='db currency USD'),
                           InlineKeyboardButton(text='EUR', callback_data='db currency EUR')],
                          self.back_buttons_esp['settings']]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        else:
            text = 'Choose the currency in which you want the values ​​to be sent:'
            inline_key = [[InlineKeyboardButton(text='USD', callback_data='db currency USD'),
                           InlineKeyboardButton(text='EUR', callback_data='db currency EUR')],
                          self.back_buttons['settings']]
            keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return viewObject(text=text, keyboard=keyb)

    def keyboard_generator(self, columns=1, command=None, myList=None, settings=None):
        inline_key = []
        for i in range(0, len(myList), columns):
            raw_buttons = []
            if (len(myList) - i) < columns:
                columns = len(myList) - i
            for c in range(0, columns, 1):
                raw_buttons.append(InlineKeyboardButton(text=myList[i + c]['name'],
                                                        callback_data='coin '
                                                                      + myList[i + c]['symbol'] + ' '
                                                                      + command))
            inline_key.append(raw_buttons)

        if command == 'top_10':
            if settings['language'] == 'ENG':
                inline_key.append(self.back_buttons["start"])
            else:
                inline_key.append(self.back_buttons_esp["start"])

        elif command == 'wallet':
            if settings['language'] == 'ENG':
                inline_key.append(self.add_coin_button)
                inline_key.append(self.back_buttons["start"])
            else:
                inline_key.append(self.add_coin_button_esp)
                inline_key.append(self.back_buttons_esp["start"])

        return InlineKeyboardMarkup(inline_keyboard=inline_key)

    def get_help(self):
        return viewObject(text="help!")
