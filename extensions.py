import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Валюта "{base}" не найдена!')
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f'Валюта "{sym}" не найдена!')

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}"!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"!')

        r = requests.get(f"https://open.er-api.com/v6/latest/{base_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * amount
        text = f"За {round(amount,2)} {base_key} можно получить {round(new_price,2)} {sym_key}"
        return text
