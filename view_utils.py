from languages import LANG
from telegram import InlineKeyboardButton

def get_text(obj_id, settings):
    lang = settings['language']
    currency = settings['currency']
    return LANG[lang][obj_id].format(lang, currency)

def coin_to_button(coin, from_view):
    return InlineKeyboardButton(text=coin['name'], callback_data='coin {} {}'.format(coin['symbol'], from_view))

def keyboard_generator(columns=1, from_view=None, myList=None):
    inline_key = []
    for i in range(0, len(myList), columns):
        row = []
        if (len(myList) - i) < columns:
            columns = len(myList) - i
        for c in range(0, columns, 1):
            row.append(coin_to_button(myList[i+c], from_view) )
        inline_key.append(row)
    return inline_key
