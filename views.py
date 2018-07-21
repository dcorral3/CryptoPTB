from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class View:
    back_to_start_button = [InlineKeyboardButton("<< Back to Main menu", callback_data='start')]
    back_to_top_10 = [InlineKeyboardButton(text='<< Back to Top 10', callback_data='top_10')]
    back_to_wallet = [InlineKeyboardButton(text='<< Back to Wallet', callback_data='wallet')]

    def __init__(self):
        self.keyboard = [[InlineKeyboardButton("Wallet", callback_data='wallet'),
                          InlineKeyboardButton("Top 10", callback_data='top_10')],
                         [InlineKeyboardButton("Add coin", callback_data='add_coin')]]
        print("view loaded")

    def getView(self, command=None, data=None):
        if command == 'start':
            keyb = InlineKeyboardMarkup(self.keyboard)
            text = "Main menu:"
        elif command == 'wallet':
            keyb = self.keyboardGenerator(command, 2, command, cursor=data)
            text = "Wallet:"
        elif command == "top_10":
            keyb = self.keyboardGenerator(command, 2, command, cursor=data)
            text = "Top 10 coins:"
        elif "coin" in command:
            symbol = command.split()[1]
            from_view = command.split()[2]
            keyb = self.coinMainKeyboard(symbol, from_view)
            text = self.coinMainTxt(data)
        else:
            text = ""
            keyb = ""
        return text, keyb

    def keyboardGenerator(self, from_view, columns=1, command=None, cursor=None):
        inline_key = []
        if cursor:
            for i in range(0, cursor.count(), columns):
                raw_buttons = []
                if (cursor.count() - i) < columns:
                    columns = cursor.count() - i
                for c in range(0, columns, 1):
                    raw_buttons.append(InlineKeyboardButton(text=cursor[i + c]['name'],
                                                            callback_data='coin '
                                                                          + cursor[i + c]['symbol'] + ' '
                                                                          + from_view))
                inline_key.append(raw_buttons)
            if command == 'top_10' or command == 'wallet':
                inline_key.append(self.back_to_start_button)
            return InlineKeyboardMarkup(inline_keyboard=inline_key)
        else:
            print("no cursor")
            return ""

    def coinMainKeyboard(self, symbol, from_view):
        print(symbol)
        inline_key = []
        inline_key.append([InlineKeyboardButton(text='Update', callback_data='coin ' + str(symbol) + ' update')])

        if from_view == 'top_10':
            inline_key.append(self.back_to_top_10)
        elif from_view == 'wallet':
            inline_key.append(self.back_to_wallet)

        return InlineKeyboardMarkup(inline_keyboard=inline_key)

    def coinMainTxt(self, coin):
        return coin['name'] + ': ' + '     ' + coin['value'] + ' USD\n' + coin['time']
