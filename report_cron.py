from telegram.ext import Updater
from config import TOKEN
import config as conf
from pymongo import MongoClient


db = MongoClient(
            host=conf.host,
            username=conf.username,
            password=conf.password,
            authSource=conf.authSource
        )[conf.authSource]


updater = Updater(token=TOKEN)
