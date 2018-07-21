from views import View
from services import Mongodb


class Controller:

    def __init__(self):
        self.view = View()
        self.mongo = Mongodb()

    def start(self, bot, update):
        text, keyboard = self.view.getView('start')
        user = self.mongo.get_user_from_db(update.message.chat_id)
        if user is None:
            self.mongo.insert_user_in_db(update.message.chat_id, [])
        update.message.reply_text(text, reply_markup=keyboard)

    def button(self, bot, update):
        query = update.callback_query

        if query.data == 'add_coin':
            user = self.mongo.get_user_from_db(query.message.chat_id)
            if user is not None:
                self.mongo.update_user_in_db(query.message.chat_id, 'BTC')

        data = self.mongo.getData(command=query.data)
        text, keyboard = self.view.getView(command=query.data, data=data)
        bot.edit_message_text(text=text, chat_id=query.message.chat_id,
                              message_id=query.message.message_id, reply_markup=keyboard)
        bot.answer_callback_query(query.id)