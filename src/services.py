import json
import re

from src.views import PATH_TO_JSON
from utils import *


def function_for_search(user_input: str) -> list:
    default_data = excel_transaction(PATH_TO_EXCEL)
    result = []
    pattern = re.compile(re.escape(user_input), re.IGNORECASE)
    for dicts in default_data:
        categories = str(dicts["Категория"])
        description = str(dicts["Описание"])
        if pattern.search(categories) or pattern.search(description):
            result.append(dicts)
    return result


def categories_with_up_cashback(data, year, month):
    dict_of_categories = {}
    new_list_with_current_data = analyze_for_cashback(data, year, month)
    for dicts in new_list_with_current_data:
        if (
            dicts["Категория"] not in dict_of_categories
            and str(dicts["Кэшбэк"]) != "nan"
        ):
            dict_of_categories[dicts["Категория"]] = int(dicts["Кэшбэк"])
        elif dicts["Категория"] in dict_of_categories and str(dicts["Кэшбэк"]) != "nan":
            dict_of_categories[dicts["Категория"]] += int(dicts["Кэшбэк"])
    return dict_of_categories


def investment_bank(
    month: str, transactions: list[dict[str, any]], limit: float
) -> list:
    sorted_by_date = sort_by_date(transactions)
    new_list = []
    sum_invest = 0.0
    default_date = datetime.datetime.strptime(month, "%m.%Y")
    for dicts in sorted_by_date:
        if str(dicts["Дата платежа"]) != "nan":
            transaction_date = datetime.datetime.strptime(
                str(dicts["Дата платежа"]), "%d.%m.%Y"
            )
            if transaction_date == default_date:
                new_list.append(dicts)
    for dicts in new_list:
        money = float(dicts["Сумма операции"])
        ready_to_invest = limit - money % limit
        sum_invest += ready_to_invest
    return abs(sum_invest)


def main():
    user_input = input(
        """Выберете сервис который вам нужен
    1. Выгодные категории повышенного кэшбэка
    2. Инвесткопилка
    3. Поиск
                       """
    )
    if user_input == "1":
        year = int(
            input("Введите год, который нужно проанализировать на повышенный кешбэк\n")
        )
        month = int(input("Введите месяц\n"))
        with open(PATH_TO_JSON, "w", encoding="utf-8") as f:
            data = categories_with_up_cashback(
                excel_transaction(PATH_TO_EXCEL), year, month
            )
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Ответ записан в JSON-файл!")

    if user_input == "2":
        with open(PATH_TO_JSON, "w", encoding="utf-8") as f:
            month = input(
                "Введите месяц, который нужно проанализировать на инвесткопилку\n"
            )
            limit = int(input("Введите предел округления\n"))
            data = f"Сумма, которую можно было отложить отложить в «Инвесткопилку» {investment_bank(month, excel_transaction(PATH_TO_EXCEL), limit)}"
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Ответ записан в JSON-файл!")

    if user_input == "3":
        with open(PATH_TO_JSON, "w", encoding="utf-8") as f:
            main_input = input("Введите строку для поиска операций\n")
            json.dump(function_for_search(main_input), f, indent=4, ensure_ascii=False)
        print("Ответ записан в JSON-файл!")


main()
