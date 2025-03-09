
from datetime import datetime, timedelta
from typing import Optional
import datetime
import pandas as pd


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> list:
    new_list = []
    if date == "":
        dates = datetime.datetime.now()
    else:
        dates = datetime.datetime.strptime(date, "%d.%m.%Y")
    list_of_dicts = transactions.to_dict(orient="records")
    for dicts in list_of_dicts:
        if str(dicts["Категория"]) == category:
            transaction_date = datetime.datetime.strptime(
                str(dicts["Дата платежа"]), "%d.%m.%Y"
            )
            if (transaction_date >= dates) and (
                transaction_date <= (dates + datetime.timedelta(weeks=13))
            ):
                new_list.append(dicts)
    for i in new_list:
        if type(i["Кэшбэк"]) == float:
            i["Кэшбэк"] = 0
    return new_list


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    new_dict = {}
    if date == "":
        dates = datetime.datetime.now()
    else:
        dates = datetime.datetime.strptime(date, "%d.%m.%Y")
    list_of_dicts = transactions.to_dict(orient="records")
    for dicts in list_of_dicts:
        if str(dicts["Дата платежа"]) != "nan":
            transaction_date = datetime.datetime.strptime(
                str(dicts["Дата платежа"]), "%d.%m.%Y"
            )
            if (transaction_date >= dates) and (
                transaction_date <= (dates + datetime.timedelta(weeks=13))
            ):
                if transaction_date not in new_dict:
                    new_dict[f"{transaction_date}"] = float(
                        abs(dicts["Сумма операции"])
                    )
                else:
                    new_dict[f"{transaction_date}"] += float(
                        abs(dicts["Сумма операции"])
                    )
    return new_dict


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    sum_workday, sum_weekday = 0, 0
    count_sum_workday, count_sum_weekday = 0, 0
    if date == "":
        dates = datetime.datetime.now()
    else:
        dates = datetime.datetime.strptime(date, "%d.%m.%Y")
    list_of_dicts = transactions.to_dict(orient="records")
    for dicts in list_of_dicts:
        if str(dicts["Дата платежа"]) != "nan":
            transaction_date = datetime.datetime.strptime(
                str(dicts["Дата платежа"]), "%d.%m.%Y"
            )
            if (transaction_date >= dates) and (
                transaction_date <= (dates + datetime.timedelta(weeks=13))
            ):
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
