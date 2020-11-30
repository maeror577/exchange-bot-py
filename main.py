"""
Телеграм-бот для перевода валют с округлением до второго знака.
Контрольный проект B10.6 для SkillFactory.
Поддерживаемые валюты: доллар, евро и рубль.
Для получения курса валют используется exchangeratesapi.io.
"""

import telebot
from telebot.types import Message

from config import TOKEN, VALUES
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def get_help(message: Message):
    """ Обработчик вывода справки по работе бота. """
    text = ('Чтобы начать работу, введите команду в следующем формате:\n'
            '<имя валюты> <в какую валюту осуществляется перевод> '
            '<количество валюты>.\n'
            '/values — увидеть список всех доступных валют.')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def get_values(message: Message):
    """ Обработчик вывода доступных валют. """
    text = 'Доступные валюты:'
    for value in VALUES:
        text += f'\n{value}'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: Message):
    """ Обработчик запроса о переводе. """
    try:
        values = message.text.lower().split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество аргументов!')
        base, quote, amount = values
        converted_value = Converter.get_price(base, quote, amount)
    except APIException as error_message:
        bot.reply_to(message, f'Ошибка пользователя:\n{error_message}')
    except Exception as error_message:
        bot.reply_to(message.chat.id,
            f'Не удалось обработать команду:\n{error_message}')
    else:
        text = (f'{amount} {VALUES[base]} ({base}) ≈ '
            + f'{converted_value:.2f} {VALUES[quote]} ({quote})')
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
