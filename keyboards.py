from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import view_utils as vu


def get_button(button=None, settings=None):
    buttons =  {
        'add_coin'      : [InlineKeyboardButton(text=vu.get_text('b_add_coin', settings), callback_data='add_coin')],
        "back_start"    : [InlineKeyboardButton(text=vu.get_text('b_back_start', settings), callback_data='start')],
        "back_top_10"   : [InlineKeyboardButton(text=vu.get_text('b_back_top_10', settings), callback_data='top_10')],
        "back_wallet"   : [InlineKeyboardButton(text=vu.get_text('b_back_wallet', settings), callback_data='wallet')],
        "back_settings" : [InlineKeyboardButton(text=vu.get_text('b_back_settings', settings), callback_data='settings')],
        "cancel_search" : [InlineKeyboardButton(text=vu.get_text('b_cancel', settings), callback_data='cancel_search')],
        "retry"         : [InlineKeyboardButton(text=vu.get_text('b_retry', settings), callback_data='search_coin')],
        "language"      : [InlineKeyboardButton(text=vu.get_text('b_language', settings), callback_data='language')],
        "currency"      : [InlineKeyboardButton(text=vu.get_text('b_currency', settings), callback_data='currency')],
        "cancel_add"    : [InlineKeyboardButton(text=vu.get_text('b_cancel', settings), callback_data='cancel wallet add_coin')],
        # Languages
        "english"       : [InlineKeyboardButton(text=vu.get_text('b_english', settings), callback_data='db language ENG')],
        "spanish"       : [InlineKeyboardButton(text=vu.get_text('b_spanish', settings), callback_data='db language SPA')]
     }
    return buttons[button]

def get_main_menu(settings=None):
    return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text= vu.get_text('b_wallet', settings), callback_data='wallet'),
                    InlineKeyboardButton("🔝 Top 10", callback_data='top_10')
                ],
                [
                    InlineKeyboardButton(vu.get_text('b_search', settings), callback_data='search_coin'),
                    InlineKeyboardButton(vu.get_text('b_settings', settings), callback_data='settings')
                ]
            ]
        )

def get_wallet(command=None, data=None, settings=None):
    columns = 2 if (len(data) > 3) else 1
    coin_key = vu.keyboard_generator(columns=columns, from_view=command, myList=data)
    coin_key.append(get_button('add_coin', settings))
    coin_key.append(get_button('back_start', settings))
    return InlineKeyboardMarkup(inline_keyboard=coin_key)

def get_top_10(command=None, data=None, settings=None):
    columns = 2 if (len(data) > 3) else 1
    coin_key = vu.keyboard_generator(columns=columns, from_view=command, myList=data)
    coin_key.append(get_button('back_start', settings))
    return InlineKeyboardMarkup(inline_keyboard=coin_key)

def get_search(settings=None):
    keyboard=[]
    keyboard.append(get_button('cancel_search', settings))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_search_error(command=None, settings=None):
    keyboard=[]
    keyboard.append(get_button('retry', settings))
    keyboard.append(get_button('cancel_search', settings))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_settings(settings=None):
    keyboard=[]
    keyboard.append(get_button('language', settings))
    keyboard.append(get_button('currency', settings))
    keyboard.append(get_button('back_start', settings))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_add_coin(settings=None):
    keyboard=[]
    keyboard.append(get_button('cancel_add', settings))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_currency(settings):
    keyboard=[
        [
            InlineKeyboardButton(text='USD', callback_data='db currency USD'),
            InlineKeyboardButton(text='EUR', callback_data='db currency EUR')
        ]
    ]
    keyboard.append(get_button('back_settings', settings))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_language(settings):
    keyboard=[]
    keyboard.append(get_button('english', settings))
    keyboard.append(get_button('spanish', settings))
    keyboard.append(get_button('back_settings', settings))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
