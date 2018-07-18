from telegram import InlineKeyboardButton, InlineKeyboardMarkup
def menu():
    keyboard = [[InlineKeyboardButton("Wallet", callback_data='wallet'),
                 InlineKeyboardButton("Top 10", callback_data='top_10')],
                [InlineKeyboardButton("Add coin", callback_data='add_coin')]
               ]
    return InlineKeyboardMarkup(keyboard)

def keyBoardGenerator(columns = 1, cursor = None):
    inline_key = []
    if cursor:
        for i in range(0, cursor.count(), columns):
            raw_buttons = []
            if (cursor.count()-i) < columns:
                columns = cursor.count()-i
            for c in range(0, columns, 1):
                raw_buttons.append(
                            InlineKeyboardButton(
                                text=cursor[i+c]['name'],
                                callback_data='coin ' + cursor[i+c]['symbol']
                            )
                        )
            inline_key.append(raw_buttons)
        return InlineKeyboardMarkup(inline_keyboard=inline_key)
