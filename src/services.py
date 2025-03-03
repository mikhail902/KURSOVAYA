import json

from src.views import PATH_TO_JSON
from utils import *

def categories_with_up_cashback(data, year, month):
    dict_of_categories = {}
    new_list_with_current_data = analyze_for_cashback(data, year, month)
    for dicts in new_list_with_current_data:
        if dicts['Категория'] not in dict_of_categories and str(dicts['Кэшбэк']) != 'nan':
            dict_of_categories[dicts['Категория']] = int(dicts['Кэшбэк'])
        elif dicts['Категория'] in dict_of_categories and str(dicts['Кэшбэк']) != 'nan':
            dict_of_categories[dicts['Категория']] += int(dicts['Кэшбэк'])
    return dict_of_categories


def investment_bank(month: str, transactions: list[dict[str, any]], limit: int)-> float:
    sorted_by_date = sort_by_date(transactions)
    new_list = []
    default_date = datetime.datetime.strptime(month, "%m.%Y")
    for dicts in sorted_by_date:
        transaction_date = datetime.datetime.strptime(str(dicts['Дата платежа']), "%d.%m.%Y")
        if transaction_date == default_date:
            new_list.append(dicts)





def main():
    user_input = input("""Выберете сервис который вам нужен
    1. Выгодные категории повышенного кэшбэка
    2. Инвесткопилка
                       """)
    if user_input == "1":
        year = int(input("Введите год, который нужно проанализировать на повышенный кешбэк\n"))
        month = int(input("Введите месяц\n"))
        with open(PATH_TO_JSON, "w", encoding="utf-8") as f:
            data = categories_with_up_cashback(excel_transaction(PATH_TO_EXCEL), year, month)
            json.dump(data, f, indent=4)
        print("Ответ записан в JSON-файл!")

    if user_input == "2":
        with open(PATH_TO_JSON, "w", encoding="utf-8") as f:
            month = input("Введите месяц, который нужно проанализировать на инвесткопилку\n")
            limit = int(input("Введите предел округления\n"))
            data = investment_bank(month, excel_transaction(PATH_TO_EXCEL), limit)
            json.dump(data, f, indent=4)

main()
