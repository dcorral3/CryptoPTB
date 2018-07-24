from views import View
from services import Mongodb


class Controller:

    def __init__(self):
        self.view = View()
        self.mongo = Mongodb()

    def start(self, bot, update):
        view = self.view.getStart()
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
            data = self.mongo.getWallet(user["_id"])
        except Exception as e:
            print("DB Error: ", str(e))
        view = self.view.getWallet(command='wallet', data=data)
        update.message.reply_text(view["text"], reply_markup=view["keyboard"])

    def button(self, bot, update):
        query = update.callback_query
        command = query.data
        user_id = query.message.chat_id        
        if "coin" in command:
            command = command.split()
            coin_symbol = command[1]
            from_view = command[2]
            data = self.mongo.getCoin(coin_symbol)
            view = self.view.getCoin(from_view=from_view, coin=data)
        elif command == "top_10":
            data = self.mongo.getTop10()
            view = self.view.getTop10(command=command, data=data)
        elif command == "wallet":
            data = self.mongo.getWallet(user_id)
            view = self.view.getWallet(command=command, data=data)
        elif command == "start":
            view = self.view.getStart()
        else:
            data = ""
        bot.edit_message_text(text=view["text"], chat_id=user_id,
                              message_id=query.message.message_id, reply_markup=view["keyboard"])
        bot.answer_callback_query(query.id)

    