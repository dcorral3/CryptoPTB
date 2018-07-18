from views import menu

def start(bot, update):
    update.message.reply_text('Please choose:', reply_markup=menu())

def button(bot, update):
    query = update.callback_query
    if query.data == 'wallet':
        res = wallet()
    elif query.data == "top_10":
        res = "Top 10"
    elif query.data == "add_coin":
        res = "Add coin"
    else:
        res = "Default"
    bot.send_message(chat_id=query.message.chat_id, text=res)
    bot.answer_callback_query(query.id)

def wallet():
    return "wallet"
