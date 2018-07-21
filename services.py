import requests
import json
from pymongo import MongoClient
import config as conf
from datetime import datetime
from pprint import pprint


class Mongodb:

    def __init__(self):
        self.coins = requests.get("https://api.coinmarketcap.com/v2/ticker/?structure=array&limit=10").json()
        self.coins = self.cleanJson()
        self.db = MongoClient(
            host=conf.host,
            username=conf.username,
            password=conf.password,
            authSource=conf.authSource
        )[conf.authSource]
        try:
            self.db.coins.insert(self.coins)
        except Exception as e:
            print("DB Error: ", str(e))
        finally:
            self.coinList = self.db.coins.find()

    def cleanJson(self):
        coinList = []

        for coin in self.coins["data"]:
            my_dict = {'_id': coin['id'], 'name': coin['name'], 'symbol': coin['symbol']}
            coinList.append(my_dict)
        return coinList

    def get_user_from_db(self, user_id):
        result = self.db.users.find_one({"_id": user_id})
        return result

    def insert_user_in_db(self, user_id, wallet):
        user = {"_id": user_id, "wallet": wallet}
        self.db.users.insert(user)
        print("user inserted in DB")

    def update_user_in_db(self, user_id, coin):
        self.db.users.update_one({'_id': user_id},
                                 {'$push': {'wallet': coin}})
        print("user updated in DB")

    def urlGenerator(self, symbol):
        if symbol == 'MIOTA':
            symbol = 'IOT'
        return "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + symbol + "&tsyms=USD", symbol

    def getTop10(self):
        return self.coinList

    def getCoin(self, symbol):
        coinObj = self.db.coins.find_one({'symbol': symbol})
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

    def getData(self, command=None):
        if "coin" in command:
            data = self.getCoin(command.split()[1])
        elif command == "top_10":
            data = self.getTop10()
        else:
            data = ""
        return data
