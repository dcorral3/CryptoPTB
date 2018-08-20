import requests
import json
from pymongo import MongoClient
import config as conf
from datetime import datetime
from graph import Graph


def clear_coin_list(coins=None):
    coin_list = []
    for coin in coins:
        my_dict = {'_id': coin['id'], 'name': coin['name'], 'symbol': coin['symbol']}
        coin_list.append(my_dict)
    return coin_list


def url_generator(coin=None, ):
    # https://api.coinmarketcap.com/v2/ticker/1/?convert=EUR
    url = "https://api.coinmarketcap.com/v2/ticker/" + str(coin["_id"]) + "/?convert=EUR"
    return url, coin["symbol"]


class Mongodb:

    def __init__(self):
        self.coinsTop10 = requests.get("https://api.coinmarketcap.com/v2/ticker/?structure=array&limit=10").json()["data"]
        self.coins = requests.get("https://api.coinmarketcap.com/v2/listings/").json()["data"]
        self.coinsTop10 = clear_coin_list(self.coinsTop10)
        self.coins = clear_coin_list(self.coins)
        self.db = MongoClient(
            host=conf.host,
            username=conf.username,
            password=conf.password,
            authSource=conf.authSource
        )[conf.authSource]

        try:
            self.db.coinsTop10.drop()
            self.db.coinsTop10.insert(self.coinsTop10)
            self.db.coins.drop()
            self.db.coins.insert(self.coins)
        except Exception as e:
            print("DB Error: ", str(e))
        finally:
            self.top10coins = list(self.db.coinsTop10.find())
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
        return self.top10coins

    def get_all_coins(self):
        return self.coinList

    def get_wallet(self, user_id=None):
        data = self.db.users.find({"_id": user_id}, {"_id": 0})
        data = data[0]["wallet"]
        return data

    def get_db_coin(self, symbol):
        return self.db.coins.find_one({"symbol": symbol})

    def get_coin(self, symbol, settings):
        coin_obj = self.db.coins.find_one({'symbol': symbol})
        url, symbol = url_generator(coin=coin_obj)
        req = requests.get(url)
        data = req.json()["data"]
        if req.status_code == 200 and coin_obj:
            if settings['currency'] == 'EUR':
                value = data['quotes']['EUR']['price']
            else:
                value = data['quotes']['USD']['price']
            percent_change_1h = data['quotes']['USD']['percent_change_1h']
            percent_change_24h = data['quotes']['USD']['percent_change_24h']
            percent_change_7d = data['quotes']['USD']['percent_change_7d']
            update_time = datetime.fromtimestamp(
                data['last_updated']
            ).strftime("%H:%M:%S")
            coin = {'name': coin_obj['name'],
                    'symbol': symbol,
                    'value': str(value),
                    'time': update_time,
                    'percent_change_1h': percent_change_1h,
                    'percent_change_24h': percent_change_24h,
                    'percent_change_7d': percent_change_7d}
        else:
            coin = None
        return coin

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
        url = {
            'hour_graph'  : "https://min-api.cryptocompare.com/data/histominute?fsym="+symbol+"&tsym="+currency+"&limit=59",
            'day_graph'   : "https://min-api.cryptocompare.com/data/histominute?fsym="+symbol+"&tsym="+currency+"&limit=1440",
            'week_graph'  : "https://min-api.cryptocompare.com/data/histohour?fsym="+symbol+"&tsym="+currency+"&limit=168",
            'month_graph' : "https://min-api.cryptocompare.com/data/histohour?fsym="+symbol+"&tsym="+currency+"&limit=720"
        }

        data = requests.get(url[graph_type]).json()['Data']
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

    def in_wallet(self, user_id, coin):
        wallet=self.db.users.find_one({'_id': user_id}, {'_id': 0, 'wallet': {'$elemMatch': {'symbol': coin['symbol']}}})
        return wallet != {}