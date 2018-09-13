import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, MinuteLocator, DateFormatter
import os
import matplotlib.lines as mlines
import view_utils as vu

class Graph:

    def __init__(self, title=None, graph_type=None, symbol=None,
                 currency=None, list_values=[], list_dates=[],
                 max_value=None, min_value=None, max_date=None,
                 min_date=None, data_frame=None):
        self.title       = title
        self.type        = graph_type
        self.currency    = currency
        self.symbol      = symbol
        self.list_values = list_values
        self.list_dates  = list_dates
        self.max_value   = max_value
        self.min_value   = min_value
        self.max_date    = max_date
        self.min_date    = min_date
        self.df  = data_frame

    def save_advanced_graph_png(self, user_id):
        fig, ax = plt.subplots()

        plt.plot('datetime', 'macd', data=self.df, color='orange', linewidth=2)
        plt.plot('datetime', 'macds', data=self.df, color='purple', linewidth=2)
        plt.plot('datetime', 'high', data=self.df, color='blue', linewidth=2)

        prev_short_mavg = self.df['macds'].shift(1)
        prev_long_mavg = self.df['macd'].shift(1)
        buys = self.df.ix[(self.df['macds'] <= self.df['macd']) & (prev_short_mavg >= prev_long_mavg)]
        sells = self.df.ix[(self.df['macds'] >= self.df['macd']) & (prev_short_mavg <= prev_long_mavg)]

        plt.ylabel(self.currency)

        for buy in buys['datetime']:
            plt.axvline(buy, color='g', linestyle='dotted')
        for sell in sells['datetime']:
            plt.axvline(sell, color='r', linestyle='dotted')

        plt.plot('datetime', 'macds', '^', data=buys, markersize=5, color='g')
        plt.plot('datetime', 'macds', 'v', data=sells, markersize=5, color='r')

        plt.gcf().autofmt_xdate()
        plt.title(self.title + ' (' + self.symbol + ')')

        dotted_red = mlines.Line2D([], [], color='red', linestyle=':', markersize=15, label='Sell moment')
        dotted_green = mlines.Line2D([], [], color='green', linestyle=':', markersize=15, label='Buy moment')

        plt.legend(handles=[dotted_red, dotted_green])

        if not os.path.exists('graphs'):
            os.makedirs('graphs')

        fig.savefig('graphs/' + str(user_id) + '.png')

    def save_graph_png(self, user_id):

        fig, ax = plt.subplots()
        ax.plot(self.list_dates, self.list_values)
        plt.ylabel(self.currency)

        major_locator, minor_locator, date_format = self.get_graph_config()

        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_minor_locator(minor_locator)
        ax.xaxis.set_major_formatter(DateFormatter(date_format))

        plt.gcf().autofmt_xdate()
        plt.title(self.title + ' (' + self.symbol + ')')

        if not os.path.exists('graphs'):
            os.makedirs('graphs')

        fig.savefig('graphs/' + str(user_id) + '.png')

    def get_graph_config(self):
        if self.type == 'month_graph':
            return DayLocator(range(0,32,3)), DayLocator(), '%d %b'
        elif self.type == 'hour_graph':
            return MinuteLocator(interval=10), MinuteLocator(), '%H:%M'
        elif self.type == 'week_graph':
            return DayLocator(), HourLocator(range(0, 25, 6)), '%d %b'
        elif self.type == 'day_graph':
            return HourLocator(interval=2), HourLocator(), '%H:%M'
        else:
            return None