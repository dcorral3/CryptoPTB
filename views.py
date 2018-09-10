# coding=utf-8
from languages import LANG
import view_utils as vu
import keyboards


class ViewObject:
    def __init__(self, text=None, keyboard=None, feedback=None):
        self.text = text
        self.keyboard = keyboard
        self.feedback = feedback


class View:
    def get_start(self, settings):
        keyb = keyboards.get_main_menu(settings)
        text = vu.get_text('start', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_wallet(self, command='wallet', data=None, settings=None):
        keyb = keyboards.get_wallet(command=command, data=data, settings=settings)
        text = vu.get_text(command, settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_top_10(self, command='top_10', data=None, settings=None):
        keyb = keyboards.get_top_10(command=command, data=data, settings=settings)
        text = vu.get_text(command, settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_search(self, settings):
        keyb = keyboards.get_search(settings=settings)
        text = vu.get_text('search', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_search_error(self, command=None, settings=None):
        keyb = keyboards.get_search_error(command=command, settings=settings)
        text = vu.get_text('search_error', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_settings(self, settings):
        keyb = keyboards.get_settings(settings)
        text = vu.get_text('settings', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_add_coin(self, settings):
        keyb = keyboards.get_add_coin(settings)
        text = vu.get_text('search', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_currency(self, settings):
        keyb = keyboards.get_currency(settings)
        text = vu.get_text('currency', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_languaje(self, settings):
        keyb = keyboards.get_language(settings)
        text = vu.get_text('language', settings)
        return ViewObject(text=text, keyboard=keyb)

    def get_coin(self, from_view=None, coin=None, settings=None, in_wallet=None, feedback=None):
        keyb        = keyboards.get_coin(from_view, coin, settings, in_wallet)
        up_icon     = '😃'
        down_icon   = '😡'
        last_1h     = coin['percent_change_1h']
        last_24h    = coin['percent_change_24h']
        last_week   = coin['percent_change_7d']
        last_1h_i   = down_icon if last_1h < 0 else up_icon
        last_24h_i  = down_icon if last_24h < 0 else up_icon
        last_week_i = down_icon if last_week < 0 else up_icon
        text = vu.get_text('coin', settings, coin, last_1h_i, last_24h_i, last_week_i)
        if feedback:
            feedback = vu.get_text(feedback, settings)
        return ViewObject(text=text, keyboard=keyb, feedback=feedback)

    def get_hide_button(self, settings):
        return keyboards.get_hide_button(settings)

    def get_help(self, settings):
        return ViewObject(text=vu.get_text('help', settings))

    def get_report(self, wallet, coins_data, settings):
        keyb = keyboards.get_hide_button(settings)
        up_icon = '😃'
        down_icon = '😡'
        report = []
        for coin in wallet:
            percentaje = coins_data[coin['symbol']][settings['currency']]['CHANGEPCT24HOUR']
            last_24h_i = down_icon if percentaje < 0 else up_icon
            item = {
                'symbol': coin['symbol'],
                'percentaje': str('%.3f' % round(percentaje, 3)),
                'icon': last_24h_i
            }
            report.append(item)
        text = vu.get_text('report', settings=settings, report=report)
        return ViewObject(text=text, keyboard=keyb)
