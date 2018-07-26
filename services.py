import requests
import json
from pymongo import MongoClient
import config as conf
from datetime import datetime
from pprint import pprint


def clean_top_10_json(coins=None):
    coinList = []
    for coin in coins:
        my_dict = {'_id': coin['id'], 'name': coin['name'], 'symbol': coin['symbol']}
        coinList.append(my_dict)
    return coinList

class Mongodb:

    def __init__(self):
        self.coinsTop10 = requests.get("https://api.coinmarketcap.com/v2/ticker/?structure=array&limit=10").json()
        self.coins = requests.get("https://api.coinmarketcap.com/v2/listings/").json()["data"]
        self.coinsTop10 = clean_top_10_json(self.coinsTop10["data"])
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
            self.top10coins = list(self.db.coinsTop10.find())

        try:
            self.db.coins.insert(self.coins)
        except Exception as e:
            print("DB Error: ", str(e))
        finally:
            self.coinList = list(self.db.coins.find())

    def get_user_id(self, user_id):
        return self.db.users.find_one({"_id": user_id})

    def insert_user(self, user_id, wallet):
        context = {"add_coin": False, "search_coin": False}
        user = {"_id": user_id, 'wallet': wallet, "context": context}
        self.db.users.insert(user)
        print("user inserted in DB")

    def add_coin_to_user(self, user_id=None, symbol=None):
        coin = self.db.coins.find_one({"symbol": symbol})
        self.db.users.update_one({'_id': user_id}, {'$addToSet': {'wallet': coin}}, upsert=True)
        print("user updated in DB")

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

    def get_coin(self, symbol):
        coinObj = self.db.coins.find_one({'symbol': symbol})
        url, symbol = self.url_generator(coin=coinObj)
        req = requests.get(url)
        data = req.json()["data"]
        if req.status_code == 200 and coinObj:
            value = data['quotes']['USD']['price']
            update_time = datetime.fromtimestamp(
                data['last_updated']
            ).strftime("%H:%M:%S")
            coin = {'name': coinObj['name'],
                    'symbol': symbol,
                    'value': str(value),
                    'time': update_time}
        else:
            coin = None
        return coin

    def url_generator(self, coin=None):
        return "https://api.coinmarketcap.com/v2/ticker/"+str(coin["id"]), coin["symbol"]

    def remove_coin(self, user_id=None, coin=None):
        self.db.users.update_one({'_id': user_id},{'$pull': {'wallet': coin}})

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
