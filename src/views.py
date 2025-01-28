import json

from src.utils import *

PATH_TO_EXCEL = "C:/Users/Sator/PycharmProjects/KURSOVAYA/data/operations.xlsx"
PATH_TO_JSON = "C:/Users/Sator/PycharmProjects/KURSOVAYA/data/answer.json"


def home(url:str)->any:
    """Основная логика страницы главная"""
    try:
        a = get_transactions_by_card(PATH_TO_EXCEL)
        b = sort_list_of_dictionaries(PATH_TO_EXCEL)
        with open(url, "w", encoding="utf-8") as f:
            times = time_of_day()
            data = {
                "greeting": times,
                "cards": sort_transactions_by_amount(a),
                "top_transactions": b,
                "currency_rates": {"currency": " ", "rate": " "},
                "stock_prices": {},
            }
            json.dump(data, f, indent=4)
            return data
    except (FileNotFoundError, TypeError, json.JSONDecodeError) as e:
        return []

def events()->any:
    """Основная логика страницы события"""
    pass


if __name__ == "__main__":
    home(PATH_TO_JSON)
    print("Ответ успешно записан в JSON-файл!")
