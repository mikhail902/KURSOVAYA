from datetime import datetime, timedelta
from typing import Optional
import datetime
import pandas as pd
import functools


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list:
    """Функция трат по категория"""
    new_list = []
    if date == "":
        dates = datetime.datetime.now()
    else:
        dates = datetime.datetime.strptime(date, "%d.%m.%Y")
    list_of_dicts = transactions.to_dict(orient="records")
    for dicts in list_of_dicts:
        if str(dicts["Категория"]) == category:
            transaction_date = datetime.datetime.strptime(str(dicts["Дата платежа"]), "%d.%m.%Y")
            if (transaction_date >= dates) and (transaction_date <= (dates + datetime.timedelta(weeks=13))):
                new_list.append(dicts)
    for i in new_list:
        if type(i["Кэшбэк"]) == float:
            i["Кэшбэк"] = 0
    return new_list


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    """Функция трат по дням недели"""
    new_dict = {}
    if date == "":
        dates = datetime.datetime.now()
    else:
        dates = datetime.datetime.strptime(date, "%d.%m.%Y")
    list_of_dicts = transactions.to_dict(orient="records")
    for dicts in list_of_dicts:
        if str(dicts["Дата платежа"]) != "nan":
            transaction_date = datetime.datetime.strptime(str(dicts["Дата платежа"]), "%d.%m.%Y")
            if (transaction_date >= dates) and (transaction_date <= (dates + datetime.timedelta(weeks=13))):
                if transaction_date not in new_dict:
                    new_dict[f"{transaction_date}"] = float(abs(dicts["Сумма операции"]))
                else:
                    new_dict[f"{transaction_date}"] += float(abs(dicts["Сумма операции"]))
    return new_dict


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    """Функция трат по выходным и рабочим дням"""
    sum_workday, sum_weekday = 0, 0
    count_sum_workday, count_sum_weekday = 0, 0
    if date == "":
        dates = datetime.datetime.now()
    else:
        dates = datetime.datetime.strptime(date, "%d.%m.%Y")
    list_of_dicts = transactions.to_dict(orient="records")
    for dicts in list_of_dicts:
        if str(dicts["Дата платежа"]) != "nan":
            transaction_date = datetime.datetime.strptime(str(dicts["Дата платежа"]), "%d.%m.%Y")
            if (transaction_date >= dates) and (transaction_date <= (dates + datetime.timedelta(weeks=13))):
                int_count_date = transaction_date.weekday()
                if (int_count_date >= 0) and (int_count_date < 6):
                    sum_workday += abs(int(dicts["Сумма операции"]))
                    count_sum_workday += 1
                else:
                    sum_weekday += abs(int(dicts["Сумма операции"]))
                    count_sum_weekday += 1
    new_dict = {
        "Рабочий день": round(sum_workday / count_sum_workday, 2),
        "Выходной день": round(sum_weekday / count_sum_weekday, 2),
    }
    return new_dict


def save_report_to_file(file_path):
    """Декоратор для функций-отчетов, который записывает результат выполнения функции в файл"""

    def decorator_report(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report_text = f"Отчет сгенерирован: {now}\n\n{result}\n{'-' * 40}\n"

            with open(file_path, "a", encoding="utf-8") as f:
                f.write(report_text)

            return result

        return wrapper

    return decorator_report


@save_report_to_file("answer.json")
def generate_report():
    return save_report_to_file("answer.json")
