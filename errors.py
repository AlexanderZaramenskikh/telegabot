import requests
import json
from cfg import keys


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def converter(base,quote,amount):
        if base == quote:
            raise APIException("Валюты равны,нечего конвертировать")

        if base not in keys or quote not in keys:
            raise APIException("Бот не обрабатывает данную валюту")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Неверный формат количества -->({amount})<--")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}")
        total = json.loads(r.content)[keys[quote]]

        return total