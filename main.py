import telebot
from errors import CryptoConverter,APIException
from cfg import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу бота введите команду в таком формате:\n'
            '(Имя валюты)(В какую перевести)(Кол-во)\n'
            'Пример: евро доллар 1\n'
            'Увидеть список всех доступных валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные вылюты:"
    for key in keys.keys():
        text = "\n".join((text , key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
        try:
            values = message.text.split(" ")

            if len(values) != 3:
                raise APIException("Неправильный формат")

            base,quote,amount = values
            total = CryptoConverter.converter(base,quote,amount)
            x = float(amount)
        except APIException as e:
            bot.reply_to(message, f"Ошибка пользователя\n{e}")
        except Exception as e:
            bot.reply_to(message, f"Не удалось обработать команду\n{e}")
        else:
            text = f"Цена {amount} {base} в {quote}: {total*x}"
            bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)