import requests
import json
from pymongo import MongoClient
import config as conf
from datetime import datetime

class Mongodb:

    coins = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=10").json()

    def __init__(self):

        self.coins = self.cleanJson()

        self.db = MongoClient(
                host = conf.host,
                username = conf.username,
                password = conf.password,
                authSource = conf.authSource
                )[conf.authSource]
        try:
            self.db.coins.insert(self.coins)
        except Exception as e:
            print("DB Error: ", str(e))
        finally:
            self.coinList = self.db.coins.find()

    def cleanJson(self):
        coinList = []

        for coin in self.coins:
            my_dict = {}
            my_dict['_id'] = coin['id']
            my_dict['name'] = coin['name']
            my_dict['symbol'] = coin['symbol']
            coinList.append(my_dict)

        return coinList


    def urlGenerator(self, symbol):
        if symbol == 'MIOTA':
            symbol = 'IOT'
        return "https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+symbol+"&tsyms=USD", symbol

    def getCoinList(self):
        return self.coinList





