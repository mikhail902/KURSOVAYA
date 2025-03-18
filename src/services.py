import json
import re

from src.views import PATH_TO_JSON
from src.utils import *


def function_for_search(user_input: str) -> list:
    """Фуункция поиска по категориям или описанию"""
    default_data = excel_transaction(PATH_TO_EXCEL)
    result = []
    pattern = re.compile(re.escape(user_input), re.IGNORECASE)
    for dicts in default_data:
        categories = str(dicts["Категория"])
        description = str(dicts["Описание"])
        if pattern.search(categories) or pattern.search(description):
            result.append(dicts)
    for i in result:
        if type(i["Кэшбэк"]) == float:
            i["Кэшбэк"] = 0
    return result


def categories_with_up_cashback(data, year, month):
    """Функция поиска операция с повышенным кэшбеком"""
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
    """Фуекция логики страницы инвесткопилка"""
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
