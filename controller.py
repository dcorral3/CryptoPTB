from views import View
from services import Mongodb

class Controller:
    
    def __init__(self):
        self.view = View()
        self.mongo = Mongodb()
        
    def start(self, bot, update):
        text, keyboard = self.view.getView('start')
        print(keyboard, text)
        update.message.reply_text(text, reply_markup=keyboard)

    def button(self, bot, update):
        query = update.callback_query
        data = self.mongo.getCoinList()
        text, keyboard = self.view.getView(command=query.data, cursor=data)
        bot.edit_message_text(text=text, chat_id=query.message.chat_id, message_id=query.message.message_id ,reply_markup=keyboard)
        bot.answer_callback_query(query.id)

    def wallet(self):
        return "wallet"
