from views import View
from services import Mongodb


def clean_wallet(wallet):
    new_wallet = []
    for coin in wallet:
        if 'id' in coin:
            my_dict = {'id': coin['id'], 'name': coin['name'], 'symbol': coin['symbol']}
            new_wallet.append(my_dict)
        else:
            new_wallet.append(coin)
    return new_wallet


class Controller:

    def __init__(self):
        self.view = View()
        self.mongo = Mongodb()

    # Commands
    def start(self, bot, update):
        user_id = update.message.chat_id
        settings = self.mongo.get_user_settings(user_id)
        view = self.view.get_start(settings)
        user = self.mongo.get_user_id(update.message.chat_id)

        if not user:
            wallet = []
            settings = {'language': 'ENG', 'currency': 'USD'}
        else:
            wallet = user["wallet"]
            wallet = clean_wallet(wallet)
            if 'settings' not in user:
                settings = {'language:': 'ENG', 'currency': 'USD'}
            else:
                settings = user['settings']

        self.mongo.insert_or_update_user(update.message.chat_id, wallet, settings)
        update.message.reply_text(view.text, reply_markup=view.keyboard)

    def text_messages(self, bot, update):
        user_id = update.message.chat_id
        settings = self.mongo.get_user_settings(user_id)

        if self.mongo.is_add_coin(user_id=user_id):
            symbol = update.message.text.upper()
            try:
                if self.mongo.coin_exist(symbol):
                    coin = self.mongo.get_db_coin(symbol)
                    self.mongo.add_coin_to_user(user_id, coin)
                    data = self.mongo.get_wallet(user_id)
                    view = self.view.get_wallet(command="wallet", data=data, settings=settings)
                else:
                    view = self.view.get_search_error(command="add_coin", settings=settings)
                self.mongo.update_context(user_id, "add_coin")
                update.message.reply_text(view.text, reply_markup=view.keyboard)
            except Exception as e:
                print("EXCEPTION ADDING COIN")
                print(str(e))

        elif self.mongo.is_search(user_id=user_id):
            symbol = update.message.text.upper()
            try:
                if self.mongo.coin_exist(symbol):
                    data = self.mongo.get_coin(symbol, settings)
                    view = self.view.get_coin("start", data, settings)
                else:
                    view = self.view.get_search_error(command="search_coin", settings=settings)
                self.mongo.update_context(user_id, "search_coin")
                update.message.reply_text(view.text, reply_markup=view.keyboard)
            except Exception as e:
                print("EXCEPTION SEARCHING")
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
        settings = self.mongo.get_user_settings(user_id)

        if "coin" in command:
            if command == "add_coin":
                self.mongo.update_context(user_id, command)
                view = self.view.get_add_coin(settings)
            elif "cancel" in command:
                command = command.split()
                self.mongo.update_context(command=command[2], user_id=user_id)
                if command[1] == 'wallet':
                    data = self.mongo.get_wallet(user_id)
                    view = self.view.get_wallet(data=data, settings=settings)
                else:
                    view = None
            elif "remove" in command:
                command = command.split()
                symbol = command[1]
                coin = self.mongo.get_db_coin(symbol)
                self.mongo.remove_coin(user_id=user_id, coin=coin)
                data = self.mongo.get_wallet(user_id)
                view = self.view.get_wallet(data=data, settings=settings)
            elif "search" in command:
                self.mongo.update_context(user_id, command)
                view = self.view.get_search(settings)
            else:
                command = command.split()
                coin_symbol = command[1]
                from_view = command[2]
                data = self.mongo.get_coin(coin_symbol, settings)
                view = self.view.get_coin(from_view=from_view, coin=data, settings=settings)
        elif command == "top_10":
            data = self.mongo.get_top_10()
            view = self.view.get_top_10(command=command, data=data, settings=settings)
        elif command == "wallet":
            data = self.mongo.get_wallet(user_id)
            view = self.view.get_wallet(command=command, data=data, settings=settings)
        elif command == "settings":
            view = self.view.get_settings(settings)
        elif command == "language":
            view = self.view.get_languaje(settings)
        elif command == "currency":
            view = self.view.get_currency(settings)
        elif 'db' in command:
            attribute = command.split()[1]
            value = command.split()[2]
            self.mongo.update_settings(user_id, attribute, value)
            settings = self.mongo.get_user_settings(user_id)
            view = self.view.get_settings(settings)
        elif command == "start" or "cancel_search":
            settings = self.mongo.get_user_settings(user_id)
            view = self.view.get_start(settings)
        else:
            data = ""

        if oldText != view.text:
            bot.edit_message_text(text=view.text, chat_id=user_id,
                                  message_id=query.message.message_id, reply_markup=view.keyboard)
        bot.answer_callback_query(query.id)
