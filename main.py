import telebot
from telebot import types
from extensions import APIException, Convertor
from config import *

conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
currencies = []
for val in exchanges.keys():
    buttons.append(types.KeyboardButton(val.capitalize()))
    currencies.append(val.capitalize())

conv_markup.add(*buttons)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Приветствую! {message.chat.username}"
                                      f"\nЭто Telegram-бот, который производит конвертацию валют."
                                      f"\nДля отображения доступных к конвертации валют введите команду /values."
                                      f"\nДля конвертации валют введите команду /convert.")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    bot.send_message(message.chat.id, f" Доступные для конвертации валюты: {', '.join(currencies)}.")

@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    text = 'Выберите валюту, из которой будет производится конвертация'
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'Выберите валюту, в которую будет производится конвертация'
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = 'Введите количество конвертируемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        text = Convertor.get_price(base, sym, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: \n{e}")
    else:
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)