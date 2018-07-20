from views import View
from services import Mongodb

class Controller:
    
    def __init__(self):
        self.view = View()
        self.mongo = Mongodb()
        self.commandStack = []

    def start(self, bot, update):
        text, keyboard = self.view.getView('start')
        update.message.reply_text(text, reply_markup=keyboard)
        self.commandStack.append('start')

    def button(self, bot, update):
        query = update.callback_query
        if query.data == 'back':
            self.commandStack.pop()
            query.data = self.commandStack.pop()   

        data = self.mongo.getData(command=query.data)
        text, keyboard = self.view.getView(command=query.data, data=data)
        bot.edit_message_text(text=text, chat_id=query.message.chat_id, message_id=query.message.message_id ,reply_markup=keyboard)
        bot.answer_callback_query(query.id)
        if "update" not in query.data: 
            self.commandStack.append(query.data)