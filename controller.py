from views import View
from services import Mongodb


class Controller:

    def __init__(self):
        self.view = View()
        self.mongo = Mongodb()
    
    # Commands 
    def start(self, bot, update):
        view = self.view.get_start()
        user = self.mongo.get_user_id(update.message.chat_id)
        if not user:
            self.mongo.insert_user(update.message.chat_id, [])
        update.message.reply_text(view.text, reply_markup=view.keyboard)
    
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
        update.message.reply_text(view.text, reply_markup=view.keyboard)
    
    def textMessages(self, bot, update):
        user_id = update.message.chat_id
        if self.mongo.is_add_coin(user_id=user_id):
            symbol = update.message.text
            try:
                self.mongo.add_coin_to_user(user_id, symbol)
                data = self.mongo.get_wallet(user_id) 
                view = self.view.get_wallet(command="wallet", data=data)
                self.mongo.update_context(user_id=user_id)
            except Exception as e:
                print(str(e))

        else:    
            view = self.view.get_help()
        
        update.message.reply_text(view.text, reply_markup=view.keyboard)

    # Buttons
    def button(self, bot, update):
        query = update.callback_query
        command = query.data
        user_id = query.message.chat_id
        oldText = query.message.text
        if "coin" in command:
            if command == "add_coin":
                self.mongo.update_context(user_id, command)
                view = self.view.get_add_coin()
            elif "cancel" in command:
                print(command)
                command = command.split()
                self.mongo.update_context(command=command[2], user_id=user_id)
                if command[1] == 'wallet':
                    data = self.mongo.get_wallet(user_id)
                    view = self.view.get_wallet(command=command[1], data=data)
                else:
                    view = None
            else:
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
        else:
            data = ""

        if oldText != view.text:
            bot.edit_message_text(text=view.text, chat_id=user_id,
                              message_id=query.message.message_id, reply_markup=view.keyboard)
        bot.answer_callback_query(query.id)
