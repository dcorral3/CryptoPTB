import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, MinuteLocator, DateFormatter
import os

class Graph:

    def __init__(self, title=None, graph_type=None, symbol=None, currency=None, list_values=[], list_dates=[], max_value=None, min_value=None, max_date=None, min_date=None):
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