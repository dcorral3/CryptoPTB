from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class viewObject:
    def __init__(self, text=None, keyboard=None):
        self.text = text
        self.keyboard = keyboard

class View:
    back_buttons = {
        "start": [InlineKeyboardButton(text="<< Back to Main menu", callback_data='start')],
        "top_10": [InlineKeyboardButton(text='<< Back to Top 10', callback_data='top_10')],
        "wallet": [InlineKeyboardButton(text='<< Back to Wallet', callback_data='wallet')]
    }
    add_coin_button = [InlineKeyboardButton(text="Add coin", callback_data='add_coin')]

    def __init__(self):
        self.keyboard = [[InlineKeyboardButton("Wallet", callback_data='wallet'),
                          InlineKeyboardButton("Top 10", callback_data='top_10'),
                          InlineKeyboardButton("Search coin", callback_data='search_coin')]]

    def get_start(self):
        keyb = InlineKeyboardMarkup(self.keyboard)
        text = "Main Menu"
        return viewObject(text=text, keyboard=keyb)

    def get_wallet(self, command='wallet', data=None):
        if len(data) > 3:
            keyb = self.keyboard_generator(columns=2, command=command, myList=data)
        else:
            keyb = self.keyboard_generator(columns=1, command=command, myList=data)
        text = "Wallet:"
        return viewObject(text=text, keyboard=keyb)

    def get_top_10(self, command='top_10', data=None):
        keyb = self.keyboard_generator(columns=2, command=command, myList=data)
        text = "Top 10 coins:"
        return viewObject(text=text, keyboard=keyb)

    def get_search(self):
        text = 'Send me the coin short name, please. (e.j: BTC)'
        inline_key = [[InlineKeyboardButton(text='Cancel', callback_data='cancel_search')]]
        keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return viewObject(text=text, keyboard=keyb)

    def get_search_error(self):
        text = '⚠️ Oops! I cant find this coin.'
        inline_key = [[InlineKeyboardButton(text='Retry', callback_data='search_coin')],
                      [InlineKeyboardButton(text='Cancel', callback_data='cancel_search')]]
        keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return viewObject(text=text, keyboard=keyb)

    def get_coin(self, from_view='wallet', coin=None):
        inline_key = []
        inline_key.append([InlineKeyboardButton(text='Update', callback_data='coin ' + str(coin['symbol']) + ' ' + from_view)])
        # añade opcion remover solo si estas en wallet
        if from_view == "wallet":
            inline_key[0].append(InlineKeyboardButton(text="Remove coin", callback_data="remove_coin " + str(coin['symbol'])))
        inline_key.append(self.back_buttons[from_view])
        keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        text = coin['name'] + ': ' + '     ' + coin['value'] + ' USD\n' + coin['time']
        return viewObject(text=text, keyboard=keyb)

    def get_add_coin(self):
        text = 'Send me the coin short name, please. (e.j: BTC)'
        inline_key = [[InlineKeyboardButton(text='Cancel', callback_data='cancel wallet add_coin')]]
        keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return viewObject(text=text, keyboard=keyb)

    def keyboard_generator(self, columns=1, command=None, myList=None):
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
            inline_key.append(self.back_buttons["start"])
        elif command == 'wallet':
            inline_key.append(self.add_coin_button)
            inline_key.append(self.back_buttons["start"])
        return InlineKeyboardMarkup(inline_keyboard=inline_key)

    def get_help(self):
        return viewObject(text="help")