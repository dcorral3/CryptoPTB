from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class View:
    
    back_button = [InlineKeyboardButton("<- Back", callback_data='back')]

    def __init__(self):
        self.keyboard = [[InlineKeyboardButton("Wallet", callback_data='wallet'),
                          InlineKeyboardButton("Top 10", callback_data='top_10')],
                         [InlineKeyboardButton("Add coin", callback_data='add_coin')]]
        print("view loaded")
    
    def getView(self, command = None, data = None):
        if command == 'start':
            keyb = InlineKeyboardMarkup(self.keyboard)
            text = "Main menu:"
        elif command == 'wallet':
            keyb = self.keyboardGenerator(2, cursor=data)
            text = "Wallet:"
        elif command == "top_10":
            keyb = self.keyboardGenerator(2, cursor=data)
            text = "Top 10 coins:"
        elif "coin" in command:
            symbol = command.split()[1]
            keyb = self.coinMainKeyboard(symbol)
            text = self.coinMainTxt(data)
        else:
            text = ""
            keyb = ""
        return text, keyb
        
    def keyboardGenerator(self, columns = 1, cursor = None):
        inline_key = []
        if cursor:
            for i in range(0, cursor.count(), columns):
                raw_buttons = []
                if (cursor.count()-i) < columns:
                    columns = cursor.count()-i 
                for c in range(0, columns, 1):
                    raw_buttons.append(InlineKeyboardButton(text=cursor[i+c]['name'],callback_data='coin ' + cursor[i+c]['symbol']))
                inline_key.append(raw_buttons)
            inline_key.append(self.back_button)
            return InlineKeyboardMarkup(inline_keyboard=inline_key)
        else:
            print("no cursor")
            return ""

    def coinMainKeyboard(self, symbol):
        print(symbol)
        inline_key = [
                      [InlineKeyboardButton(text='update', callback_data='coin ' + str(symbol) + " update"),
                       InlineKeyboardButton(text='<-Back', callback_data='back')]]
        return InlineKeyboardMarkup(inline_keyboard=inline_key)

    def coinMainTxt(self, coin):
        return coin['name']+ ': ' + '     ' + coin['value'] + ' USD\n' + coin['time']
    
