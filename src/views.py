import json
from idlelib.iomenu import encoding

from src.utils import *
from src.utils2 import *

PATH_TO_EXCEL = "/Users/anastas2006/Downloads/KURSOVAYA/data/operations.xlsx"
PATH_TO_JSON = "/Users/anastas2006/Downloads/KURSOVAYA/data/answer.json"


def home(url: str) -> any:
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


def events(url, transactions, target_date_str, range_type="m"):
    """Функция считывающая список платежей, дату и параметр поиска формирующий список"""
    with open(url, "w", encoding="utf-8") as f:
        b = filter_transactions_by_range(transactions, target_date_str)
        data = {
            "expenses": {
                "total_amount": total_amount(b),
                "main": calculate_expenses_by_category(b),
            },
            "transfers_and_cash": sum_for_two_categories(b),
            "income": sum_for_ap_categories(b),
            "currency_rate": [],
        }
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    a = excel_transaction(PATH_TO_EXCEL)
    str_user = input(
        f"""Какую страницу открыть?
1. Главная              2. События 
                \n"""
    )
    if str_user == "1":
        home(PATH_TO_JSON)

    elif str_user == "2":
        str_data = input("Введите дату для поиска\n")
        events(PATH_TO_JSON, a, str_data)

    print("Ответ успешно записан в JSON-файл!")
