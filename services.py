import requests
import json
from pymongo import MongoClient
import config as conf
from datetime import datetime
from pprint import pprint


class Mongodb:

    def __init__(self):
        self.coinsTop10 = requests.get("https://api.coinmarketcap.com/v2/ticker/?structure=array&limit=10").json()
        self.coinsTop10 = self.cleanJson(self.coinsTop10["data"])
        self.db = MongoClient(
            host=conf.host,
            username=conf.username,
            password=conf.password,
            authSource=conf.authSource
        )[conf.authSource]
        try:
            self.db.coinsTop10.insert(self.coinsTop10)
        except Exception as e:
            print("DB Error: ", str(e))
        finally:
            self.coinList = list(self.db.coinsTop10.find())

    def cleanJson(self, coins=None):
        coinList = []
        for coin in coins:
            my_dict = {'_id': coin['id'], 'name': coin['name'], 'symbol': coin['symbol']}
            coinList.append(my_dict)
        return coinList


    def get_user_id(self, user_id):
        return self.db.users.find({"_id": user_id}, {"wallet": 0})

    def insert_user(self, user_id, wallet):
        user = {"_id": user_id, 'wallet': wallet}
        self.db.users.insert(user)
        print("user inserted in DB")

    def add_coin_to_user(self, user_id, coin):
        self.db.users.update_one({'_id': user_id}, {'$addToSet': {'wallet': coin}}, upsert=True)
        print("user updated in DB")

    def urlGenerator(self, symbol):
        if symbol == 'MIOTA':
            symbol = 'IOT'
        return "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + symbol + "&tsyms=USD", symbol

    def getTop10(self):
        return self.coinList
    
    def getWallet(self, user_id=None):
        data = self.db.users.find({"_id": user_id}, {"_id": 0})
        data = data[0]["wallet"]
        return data

    def getCoin(self, symbol):
        coinObj = self.db.coinsTop10.find_one({'symbol': symbol})
        url, symbol = self.urlGenerator(symbol)
        req = requests.get(url)
        data = req.json()
        if req.status_code == 200 and coinObj:
            value = data['RAW'][symbol]['USD']['PRICE']
            update_time = datetime.fromtimestamp(
                data['RAW'][symbol]['USD']['LASTUPDATE']
            ).strftime("%H:%M:%S")
            coin = {'name': coinObj['name'],
                    'symbol': symbol,
                    'value': str(value),
                    'time': update_time}
        else:
            coin = None
        return coin