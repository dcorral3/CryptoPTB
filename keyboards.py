from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import view_utils as vu

def get_main_menu(settings=None):
    button={
        "wallet"     : InlineKeyboardButton(text=vu.get_text('b_wallet', settings), callback_data='wallet'),
        "top_10"     : InlineKeyboardButton(text="🔝 Top 10", callback_data='top_10'),
        "search_coin": InlineKeyboardButton(text=vu.get_text('b_search', settings), callback_data='search_coin'),
        "settings"   : InlineKeyboardButton(text=vu.get_text('b_settings', settings), callback_data='settings')
    }
    keyboard=[
                [button['wallet'], button['top_10']],
                [button['search_coin'], button['settings']]
             ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_wallet(command=None, data=None, settings=None):
    button={
        'add_coin'      : InlineKeyboardButton(text=vu.get_text('b_add_coin', settings), callback_data='add_coin'),
        "back_start"    : InlineKeyboardButton(text=vu.get_text('b_back_start', settings), callback_data='start')
    }
    columns = 2 if (len(data) > 3) else 1
    coin_key = vu.keyboard_generator(columns=columns, from_view=command, myList=data)
    coin_key.append([button['add_coin']])
    coin_key.append([button['back_start']])
    return InlineKeyboardMarkup(inline_keyboard=coin_key)

def get_top_10(command=None, data=None, settings=None):
    button={
        "back_start"    : InlineKeyboardButton(text=vu.get_text('b_back_start', settings), callback_data='start')
    }
    columns = 2 if (len(data) > 3) else 1
    coin_key = vu.keyboard_generator(columns=columns, from_view=command, myList=data)
    coin_key.append([button['back_start']])
    return InlineKeyboardMarkup(inline_keyboard=coin_key)

def get_search(settings=None):
    button={
        "cancel_search" : InlineKeyboardButton(text=vu.get_text('b_cancel', settings), callback_data='cancel_search')
    }
    keyboard=[
                [button['cancel_search']]
             ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_search_error(command=None, settings=None):
    button={
        "cancel_search" : InlineKeyboardButton(text=vu.get_text('b_cancel', settings), callback_data='cancel_search'),
        "retry"         : InlineKeyboardButton(text=vu.get_text('b_retry', settings), callback_data='search_coin')
    }
    keyboard=[
                [button['retry']],
                [button['cancel_search']]
            ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_settings(settings=None):
    button={
        "language"      : InlineKeyboardButton(text=vu.get_text('b_language', settings), callback_data='language'),
        "currency"      : InlineKeyboardButton(text=vu.get_text('b_currency', settings), callback_data='currency'),
        "back_start"    : InlineKeyboardButton(text=vu.get_text('b_back_start', settings), callback_data='start')
    }
    keyboard=[
                [button['language'], button['currency']],
                [button['back_start']]
            ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_add_coin(settings=None):
    button={
        "cancel_add"    : InlineKeyboardButton(text=vu.get_text('b_cancel', settings), callback_data='cancel wallet add_coin')
    }
    keyboard=[
                [button['cancel_add']]
             ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_currency(settings):
    button={
        'usd'           : InlineKeyboardButton(text='USD', callback_data='db currency USD'),
        'eur'           : InlineKeyboardButton(text='EUR', callback_data='db currency EUR'),
        'gbp'           : InlineKeyboardButton(text='GBP', callback_data='db currency GBP'),
        'jpy'           : InlineKeyboardButton(text='JPY', callback_data='db currency JPY'),
        'aud'           : InlineKeyboardButton(text='AUD', callback_data='db currency AUD'),
        'hkd'           : InlineKeyboardButton(text='HKD', callback_data='db currency HKD'),
        "back_settings" : InlineKeyboardButton(text=vu.get_text('b_back_settings', settings), callback_data='settings')
    }
    keyboard=[
                [button['usd'], button['eur'], button['gbp']],
                [button['jpy'], button['aud'], button['hkd']],
                [button['back_settings']]
             ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_language(settings):
    button={
        "english"       : InlineKeyboardButton(text=vu.get_text('b_english', settings), callback_data='db language ENG'),
        "spanish"       : InlineKeyboardButton(text=vu.get_text('b_spanish', settings), callback_data='db language SPA'),
        "back_settings" : InlineKeyboardButton(text=vu.get_text('b_back_settings', settings), callback_data='settings')
    }
    keyboard=[
                [button['english'], button['spanish']],
                [button['back_settings']]
             ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_coin(from_view=None, coin=None, settings=None, in_wallet=None):
    button={
        'hour'    : InlineKeyboardButton(text=vu.get_text('b_hour_graph', settings), callback_data='hour_graph {}'.format(str(coin['symbol']))),
        'day'     : InlineKeyboardButton(text=vu.get_text('b_day_graph', settings), callback_data='day_graph {}'.format(str(coin['symbol']))),
        'week'    : InlineKeyboardButton(text=vu.get_text('b_week_graph', settings), callback_data='week_graph {}'.format(str(coin['symbol']))),
        'month'   : InlineKeyboardButton(text=vu.get_text('b_month_graph', settings), callback_data='month_graph {}'.format(str(coin['symbol']))),
        'del_coin': InlineKeyboardButton(text=vu.get_text('b_del_coin', settings), callback_data="remove_coin {} {}".format(str(coin['symbol']), from_view)),
        'add_coin': InlineKeyboardButton(text=vu.get_text('b_add_coin', settings), callback_data="add_to_wallet {} {}".format(str(coin['symbol']), from_view)),
        'update'  : InlineKeyboardButton(text=vu.get_text('b_update', settings), callback_data="coin {} {}".format(str(coin['symbol']), from_view)),
        # Back buttons
        "wallet"    : InlineKeyboardButton(text=vu.get_text('b_back_wallet', settings), callback_data='wallet'),
        "top_10"    : InlineKeyboardButton(text=vu.get_text('b_back_top_10', settings), callback_data='top_10'),
        "start"    : InlineKeyboardButton(text=vu.get_text('b_back_start', settings), callback_data='start')
    }
    keyboard=[
                [button['hour'], button['day']],
                [button['week'], button['month']],
                [button['del_coin']],
                [button['update']],
                [button[from_view]]
             ]
    if not in_wallet:
        keyboard[2]=[button['add_coin']]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_hide_button(settings):
    button={
        'hide': InlineKeyboardButton(text=vu.get_text('b_hide', settings), callback_data='hide')
    }
    keyboard=[
                [button['hide']]
             ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)