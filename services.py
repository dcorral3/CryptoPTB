import requests
import json
from pymongo import MongoClient
import config as conf
from graph import Graph
import service_utils as su
from datetime import datetime
from pprint import pprint
import pandas as pd
from stockstats import StockDataFrame

class Mongodb:

    def __init__(self):
        self.coins = requests.get(su.url_generator(url_type='all_coins')).json()['data']
        self.coins = su.clear_cmc_list(self.coins)
        self.db = MongoClient(
            host=conf.host,
            username=conf.username,
            password=conf.password,
            authSource=conf.authSource
        )[conf.authSource]
        try:
            self.db.coins.drop()
            self.db.coins.insert(self.coins)
        except Exception as e:
            print("DB Error: ", str(e))
        finally:
            self.coinList = list(self.db.coins.find())


    def get_user_id(self, user_id):
        return self.db.users.find_one({"_id": user_id})

    def insert_or_update_user(self, user_id, wallet, settings):
        context = {"add_coin": False, "search_coin": False}
        user = {"_id": user_id, 'wallet': wallet, "context": context, 'settings': settings}
        self.db.users.update({'_id': user_id}, user, upsert=True)

    def coin_exist(self, symbol=None):
        return self.db.coins.find_one({"symbol": symbol})

    def add_coin_to_user(self, user_id=None, coin=None):
        self.db.users.update_one({'_id': user_id}, {'$addToSet': {'wallet': coin}}, upsert=True)

    def get_top_10(self):
        data = requests.get(su.url_generator(url_type='top_10')).json()["data"]
        return su.clear_cmc_list(data)

    def get_wallet(self, user_id=None):
        data = self.db.users.find({"_id": user_id}, {"_id": 0})
        data = data[0]["wallet"]
        return data

    def get_db_coin(self, symbol):
        return self.db.coins.find_one({"symbol": symbol})

    def get_coin(self, symbol, settings):
        currency = settings['currency']
        # CryptoCompare
        url_cc = su.url_generator(url_type='cc_single_coin', symbol=symbol, currency=currency)
        req_cc = requests.get(url_cc)
        data_cc = req_cc.json()["RAW"][symbol][currency]

        # CoinMarketCap
        coin_obj = self.db.coins.find_one({'symbol': symbol})
        coin_id = coin_obj['_id']
        url_cmc = su.url_generator(url_type='cmc_single_coin', coin_id=coin_id, currency=currency)
        req_cmc = requests.get(url_cmc)
        data_cmc = req_cmc.json()['data']

        if req_cc.status_code == 200 and req_cmc.status_code == 200:
            coin_cc = su.parse_coin_cc(data=data_cc, currency=currency)
            coin_cmc = su.parse_coin_cmc(data=data_cmc, currency=currency)
            coin = coin_cc
            coin.update(coin_cmc)
            return coin
        else:
            print("error coin")
            return None

    def remove_coin(self, user_id=None, coin=None):
        self.db.users.update_one({'_id': user_id}, {'$pull': {'wallet': coin}})

    # Context utils
    def update_context(self, user_id=None, command=None):
        user = self.db.users.find_one({"_id": user_id})
        context = user["context"]
        if command:
            if command == "add_coin":
                self.db.users.update_one({"_id": user_id}, {"$set": {"context.add_coin": not context[command]}})
            elif command == "search_coin":
                self.db.users.update_one({"_id": user_id}, {"$set": {"context.search_coin": not context[command]}})
            else:
                print("update context error")
        else:
            self.db.users.update_one({"_id": user_id}, {"$set": {"context.add_coin": False}})
            self.db.users.update_one({"_id": user_id}, {"$set": {"context.search_coin": False}})

    def reset_context(self, user_id=None):
        self.db.users.update_one({"_id": user_id}, {"$set": {"context.add_coin": False}})
        self.db.users.update_one({"_id": user_id}, {"$set": {"context.search_coin": False}})


    def is_add_coin(self, user_id=None):
        return self.db.users.find_one({"_id": user_id})["context"]["add_coin"]

    def is_search(self, user_id):
        return self.db.users.find_one({"_id": user_id})["context"]["search_coin"]

    def update_settings(self, user_id, attribute, value):
        self.db.users.update_one({"_id": user_id}, {"$set": {"settings."+str(attribute): str(value)}})

    def get_user_settings(self, user_id):
        data = self.db.users.find({"_id": user_id}, {"_id": 0})
        data = data[0]["settings"]
        return data

    def get_graph(self, graph_type, symbol, currency):
        data = requests.get(su.url_generator(url_type=graph_type, symbol=symbol, currency=currency)).json()['Data']
        list_values = []
        list_dates = []
        max_value = min_value = max_date = min_date = None

        for item in data:
            list_values.append(item['close'])
            if max_value is None or item['close'] > max_value:
                max_value = item['close']
            if min_value is None or item['close'] < min_value:
                min_value = item['close']

            list_dates.append(datetime.fromtimestamp(item['time']))
            if max_date is None or item['time'] > max_date:
                max_date = item['time']
            if min_date is None or item['time'] < min_date:
                min_date = item['time']

        return Graph(graph_type=graph_type, symbol=symbol, currency=currency,
                     list_values=list_values, list_dates=list_dates, max_value=max_value,
                     min_value=min_value, max_date=max_date, min_date=min_date)

    def get_advanced_graph(self, graph_type, symbol, currency):
        data = requests.get(su.url_generator(url_type=graph_type, symbol=symbol, currency=currency)).json()
        df = pd.io.json.json_normalize(data, ['Data'])
        df['datetime'] = pd.to_datetime(df.time, unit='s')
        df = df[['datetime', 'low', 'high', 'open',
                 'close', 'volumefrom', 'volumeto']]

        df = StockDataFrame.retype(df)
        df['macd'] = df.get('macd')  # calculate MACD
        df.head()

        return Graph(graph_type=graph_type, symbol=symbol, currency=currency, data_frame=df)


    def in_wallet(self, user_id, coin):
        wallet=self.db.users.find_one({'_id': user_id}, {'_id': 0, 'wallet': {'$elemMatch': {'symbol': coin['symbol']}}})
        return wallet != {}

    def get_all_users(self):
        users = self.db.users.find()
        return list(users)

    def get_coins_data(self, wallet, settings):
        print('Wallet:{}, {}\nSettings:{}, {}'.format(type(wallet), wallet, type(settings), settings))
        symbols = ''
        for coin in wallet:
            symbols += coin['symbol'] + ','
        data = requests.get(su.url_generator(url_type='cc_multiple_coin',
                                             symbol=symbols,
                                             currency=settings['currency'])).json()['RAW']
        return data

    def add_user_report(self, user_id):
        self.db.report.insert_one({'_id': user_id})

    def del_user_report(self, user_id):
        self.db.report.remove({'_id': user_id})

    def is_in_report(self, user_id):
        user = self.db.report.find_one({"_id": user_id})
        return user is not None

    def get_users_report(self):
        users = self.db.report.find()
        return list(users)