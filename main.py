import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('token')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome! Write amount you want to convert:')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Error! Please enter correct value')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD to EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR to USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD to GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Others', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Choose currency', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Error! Value must be greater than zero. Try again')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        result = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Result: {round(result, 2)}\n You may send another value to continue')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Enter pair of currency you want to convert via /.')
        bot.register_next_step_handler(call.message, user_currency)


def user_currency(message):
    try:
        values = message.text.upper().split('/')
        result = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Result: {round(result, 2)}\n You may send another value to continue')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Error! Wrong currency. Try again. Example: eur/usd')
        bot.register_next_step_handler(message, user_currency)

bot.polling(none_stop=True)
