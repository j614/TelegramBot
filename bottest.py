import telebot
from collections import defaultdict
token ='855074020:AAHsWdVyLjRSDaW9EDfBOxFCFbKyA3J1ArA'

STR,ADR =range(2)
USER_STATE = defaultdict(lambda: STR)
PRODC = defaultdict(list)


bot = telebot.TeleBot(token)


def gate_state(message):
    return USER_STATE[message.chat.id]


def updаte_state(message, state):
    USER_STATE[message.chat.id] = state


def del_product(key):
    PRODC[key]= []


def app_product(user_id,key):
    PRODC[user_id].append(key)



@bot.message_handler(commands=['add'],func=lambda message: gate_state(message) == STR)
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='Напиши адрес')
    updаte_state(message, ADR)


@bot.message_handler(func=lambda message: gate_state(message) == ADR)
def handle_adress(message):
    app_product(message.chat.id, message.text)
    updаte_state(message, STR)



@bot.message_handler(commands=['list'])
def hanlde_list(message):
    if(PRODC[message.chat.id]):
        val = ','.join(PRODC[message.chat.id][-9:])
        bot.send_message(chat_id=message.chat.id, text='Вот твои последние 10 мест :{}'.format(val))
    else:
        bot.send_message(chat_id=message.chat.id, text='Нет мест(')


@bot.message_handler(commands=['reset'])
def handle_reset(message):
    del_product(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='Список очищен')



@bot.message_handler(func=lambda message: gate_state(message) == STR)
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='Набери команду /add-добавить в список, /list-показать весь список, /reset-очистить список')

bot.polling()