import json
from datetime import datetime

from src.utils import *

PATH_TO_EXCEL = "/Users/anastas2006/Downloads/KURSOVAYA/data/operations.xlsx"
PATH_TO_JSON = "/Users/anastas2006/Downloads/KURSOVAYA/data/answer.json"


def time_of_day():
    """Функция считывания времени суток"""
    time_now = datetime.datetime.now()
    time_obj = int(time_now.strftime("%H"))
    if time_obj < 18 | time_obj > 12:
        now_time = "Добрый день!"
    elif time_obj > 18 | time_obj < 22:
        now_time = "Добрый вечер!"
    elif time_obj > 4 | time_obj < 12:
        now_time = "Доброе утро!"
    else:
        now_time = "Доброй ночи!"
    return now_time


def home(path: str) -> any:
    """Основная логика страницы главная"""
    try:
        dict_of_excel_file = get_transactions_by_card(PATH_TO_EXCEL)
        sort_list = sort_list_of_dictionaries(PATH_TO_EXCEL)
        with open(path, "w", encoding="utf-8") as f:
            data = {
                "greeting": time_of_day(),
                "cards": sort_transactions_by_amount(dict_of_excel_file),
                "top_transactions": sort_list,
                "currency_rates": {"currency": " ", "rate": " "},
                "stock_prices": {},
            }
            json.dump(data, f, indent=4, ensure_ascii=False)
            return data
    except (FileNotFoundError, TypeError, json.JSONDecodeError) as e:
        return []


def events(path, transactions, target_date_str, range_type="m"):
    """Функция считывающая список платежей, дату и параметр поиска формирующий список"""
    with open(path, "w", encoding="utf-8") as f:
        filtered_list_by_date = filter_transactions_by_range(
            transactions, target_date_str
        )
        data = {
            "expenses": {
                "total_amount": total_amount(filtered_list_by_date),
                "main": calculate_expenses_by_category(filtered_list_by_date),
            },
            "transfers_and_cash": sum_for_two_categories(filtered_list_by_date),
            "income": sum_for_ap_categories(filtered_list_by_date),
            "currency_rate": [],
        }
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    trans_list = excel_transaction(PATH_TO_EXCEL)
    str_user = input(
        f"""Какую страницу открыть?
1. Главная              2. События 
                \n"""
    )
    if str_user == "1":
        home(PATH_TO_JSON)

    elif str_user == "2":
        str_data = input("Введите дату для поиска\n")
        events(PATH_TO_JSON, trans_list, str_data)

    print("Ответ успешно записан в JSON-файл!")
