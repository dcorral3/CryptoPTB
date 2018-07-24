from views import View
from services import Mongodb


class Controller:

    def __init__(self):
        self.view = View()
        self.mongo = Mongodb()

    def start(self, bot, update):
        view = self.view.get_start()
        user = self.mongo.get_user_id(update.message.chat_id)
        if not user.count():
            self.mongo.insert_user(update.message.chat_id, [])
        update.message.reply_text(view["text"], reply_markup=view["keyboard"])
    
    def add_coin(self, bot, update):
        coin = {
            "_id": 1,
            "name": "Bitcoin",
            "symbol": "BTC" 
        }
        try:
            user = self.mongo.get_user_id(update.message.chat_id).next()
            if not user:
                self.mongo.insert_user(update.message.chat_id, [])
            self.mongo.add_coin_to_user(user["_id"], coin)
            data = self.mongo.get_wallet(user["_id"])
        except Exception as e:
            print("DB Error: ", str(e))
        view = self.view.get_wallet(command='wallet', data=data)
        update.message.reply_text(view["text"], reply_markup=view["keyboard"])

    def button(self, bot, update):
        query = update.callback_query
        command = query.data
        user_id = query.message.chat_id
        oldText = query.message.text

        if "coin" in command:
            command = command.split()
            coin_symbol = command[1]
            from_view = command[2]
            data = self.mongo.get_coin(coin_symbol)
            view = self.view.get_coin(from_view=from_view, coin=data)
        elif command == "top_10":
            data = self.mongo.get_top_10()
            view = self.view.get_top_10(command=command, data=data)
        elif command == "wallet":
            data = self.mongo.get_wallet(user_id)
            view = self.view.get_wallet(command=command, data=data)
        elif command == "start":
            view = self.view.get_start()
        elif command == "add":
            view = self.view.get_add_coin()
        else:
            data = ""

        if oldText is not view['text']:
            bot.edit_message_text(text=view["text"], chat_id=user_id,
                              message_id=query.message.message_id, reply_markup=view["keyboard"])
        bot.answer_callback_query(query.id)
