from languages import LANG
from telegram import InlineKeyboardButton


def get_text(obj_id, settings, coin=None, last_1h_i=None, last_24h_i=None, last_week_i=None, report=None):
    lang = settings['language']
    currency = settings['currency']
    if coin:
        return LANG[lang][obj_id].format(
            coin['name'],
            coin['value'],
            settings['currency'],
            coin['percent_change_1h'],
            last_1h_i,
            coin['percent_change_24h'],
            last_24h_i,
            coin['percent_change_7d'],
            last_week_i,
            coin['time']
        )
    if report:
        balance = 0
        text = LANG[lang]['report_header']
        body = ''
        for item in report:
            body += '<b>' + item['symbol'] + '</b>:\n' \
                    + LANG[lang]['report_percentaje'] + ' ' + item['percentaje'] + '% ' + item['icon'] + '\n' \
                    + LANG[lang]['report_price'] + ' ' + str(item['price']) + ' ' + currency + '\n' \
                    + LANG[lang]['report_low24h'] + ' ' + str(item['low24h']) + ' ' + currency + '\n'\
                    + LANG[lang]['report_high24h'] + ' ' + str(item['high24h']) + ' ' + currency + '\n\n'
            balance += float(item['percentaje'])
            str('%.3f' % round(balance, 3))
        if balance > 0:
            return text + body + LANG[lang]['report_balance_up'] + ': ' + str(balance) + '%'
        else:
            return text + body + LANG[lang]['report_balance_down'] + ': ' + str(balance) + '%'

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
            row.append(coin_to_button(myList[i + c], from_view))
        inline_key.append(row)
    return inline_key


def is_positive(value):
    return value > 0
