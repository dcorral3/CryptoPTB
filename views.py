from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class View:
    back_buttons = {
        "start": [InlineKeyboardButton("<< Back to Main menu", callback_data='start')],
        "top_10": [InlineKeyboardButton(text='<< Back to Top 10', callback_data='top_10')],
        "wallet": [InlineKeyboardButton(text='<< Back to Wallet', callback_data='wallet')]
    }
    add_coin_button = [InlineKeyboardButton("Add coin", callback_data='add')]

    def __init__(self):
        self.keyboard = [[InlineKeyboardButton("Wallet", callback_data='wallet'),
                          InlineKeyboardButton("Top 10", callback_data='top_10')]]

    def get_start(self):
        keyb = InlineKeyboardMarkup(self.keyboard)
        text = "Main Menu"
        return {"keyboard": keyb, "text": text}

    def get_wallet(self, command='wallet', data=None):
        if len(data) > 3:
            keyb = self.keyboard_generator(columns=2, command=command, myList=data)
        else:
            keyb = self.keyboard_generator(columns=1, command=command, myList=data)
        text = "Wallet:"
        return {"keyboard": keyb, "text": text}

    def get_top_10(self, command='top_10', data=None):
        keyb = self.keyboard_generator(columns=2, command=command, myList=data)
        text = "Top 10 coins:"
        return {"keyboard": keyb, "text": text}

    def get_coin(self, from_view='wallet', coin=None):
        inline_key = []
        inline_key.append(
            [InlineKeyboardButton(text='Update', callback_data='coin ' + str(coin['symbol']) + ' ' + from_view)])
        inline_key.append(self.back_buttons[from_view])
        keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        text = coin['name'] + ': ' + '     ' + coin['value'] + ' USD\n' + coin['time']
        return {"keyboard": keyb, "text": text}

    def get_add_coin(self):
        text = 'Send me the coin short name, please. (e.j: BTC)'
        inline_key = [[InlineKeyboardButton(text='Cancel', callback_data='wallet')]]
        keyb = InlineKeyboardMarkup(inline_keyboard=inline_key)
        return {"keyboard": keyb, "text": text}

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

