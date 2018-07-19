from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class View:
    
    def __init__(self):
        self.keyboard = [[InlineKeyboardButton("Wallet", callback_data='wallet'),
                          InlineKeyboardButton("Top 10", callback_data='top_10')],
                         [InlineKeyboardButton("Add coin", callback_data='add_coin')]]
        print("view loaded")
    
    def getView(self, command = None, cursor = None, response_type = None):
        if command == 'start':
            keyb = InlineKeyboardMarkup(self.keyboard)
            text = "Main menu:"
        elif command == 'wallet':
            keyb = self.keyboardGenerator(2, cursor)
            text = "Wallet:"
        elif command == "top_10":
            keyb = self.keyboardGenerator(2, cursor)
            text = "Top 10 coins:"
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
                    columns = count-i 
                for c in range(0, columns, 1):
                    raw_buttons.append(InlineKeyboardButton(text=cursor[i+c]['name'],callback_data='coin ' + cursor[i+c]['symbol']))
                inline_key.append(raw_buttons)
                print(inline_key)
            return InlineKeyboardMarkup(inline_keyboard=inline_key)
        else:
            print("no cursor")
            return ""

