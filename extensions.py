""" Набор классов для телеграм-бота. """

import json
import requests

from config import VALUES


class APIException(Exception):
    """ Исключение для обработки ошибок ввода пользователя. """


class Converter:
    """ Класс объекта-конвертера валют. """

    @staticmethod
    def get_price(base, quote, amount):
        """
        Получение количества целевой валюты после перевода.
        Аргументы:
        base — имя валюты, цену на которую надо узнать;
        quote — имя валюты, цену в которой надо узнать;
        amount — количество переводимой валюты.
        """
        if base == quote:
            raise APIException('Невозможно перевести одинаковые '
                               f'валюты «{base}».')
        try:
            base_ticker = VALUES[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту «{base}».')
        try:
            quote_ticker = VALUES[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту «{quote}».')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество «{amount}».')

        request = requests.get('https://api.exchangeratesapi.io/latest?'
                               f'base={quote_ticker}')
        exchange_rate = json.loads(request.content)['rates'][base_ticker]
        convereted_value = amount / exchange_rate
        return convereted_value
