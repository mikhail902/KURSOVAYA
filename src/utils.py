import datetime
import os
from collections import defaultdict
from datetime import datetime, timedelta

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
PATH_TO_EXCEL = "/Users/anastas2006/Downloads/KURSOVAYA/data/operations.xlsx"
API_KEY1 = "tP6pidXH3QMCPZmCOPfsyXE8CQxsvxMk"


def conversion(dictionary: dict) -> any:
    """Считывания курса валюты через API"""
    try:
        url = "https://api.apilayer.com/exchangerates_data/convert"
        payload = {
            "amount": dictionary["operationAmount"]["amount"],
            "from": dictionary["operationAmount"]["currency"]["code"],
            "to": "RUB",
        }
        headers = {"apikey": API_KEY1}
        response = requests.get(url, headers=headers, params=payload).json()
        return response["result"]
    except KeyError:
        return "Ошибка конвертации, закончился лимит запросов на перевод валюты"


def excel_transaction(file_path: str) -> list:
    """Функция считывающая строки из эксель файла и превращающая в список словарей из строк файла"""
    try:
        df = pd.read_excel(file_path)
        list_of_dicts = df.to_dict(orient="records")
        return list_of_dicts
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {file_path}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def get_transactions_by_card(file_path: str) -> dict:
    """Вывод из экселя"""
    df = pd.read_excel(file_path)
    transactions_by_card = {}
    for index, row in df.iterrows():
        card_number = str(row["Номер карты"])
        transaction_amount = float(row["Сумма операции с округлением"])
        if card_number in transactions_by_card:
            if card_number != "nan":
                transactions_by_card[card_number] += transaction_amount
        else:
            if card_number != "nan":
                transactions_by_card[card_number] = transaction_amount
    return transactions_by_card


def time_of_day():
    """Функция считывания времени суток"""
    time_now = datetime.now()
    h = int(time_now.strftime("%H"))
    if h < 18 | h > 12:
        now_time = "Добрый день"
    elif h > 18 | h < 22:
        now_time = "Добрый вечер"
    elif h > 4 | h < 12:
        now_time = "Доброе утро"
    else:
        now_time = "Доброй ночи"
    return now_time


def sort_transactions_by_amount(transactions_dict: dict, reverse=True) -> list:
    """Функция сортировки и вывод платежей"""
    new_list = [{}, {}, {}, {}, {}]
    k = 0
    sorted_transactions = dict(
        sorted(transactions_dict.items(), key=lambda item: item[1], reverse=reverse)
    )
    for i, j in sorted_transactions.items():
        new_list[k]["last_digit"] = i
        new_list[k]["total_spent"] = j
        new_list[k]["cashback"] = j / 100
        k += 1
        if k > 4:
            break
    return new_list


def sort_list_of_dictionaries(path, key="Сумма операции", reverse=False):
    """Функция сортировки и вывод топ 5 платежей"""
    new_list = []
    some_dict = {}
    list_of_dicts = excel_transaction(path)
    sorted_list = sorted(
        list_of_dicts, key=lambda item: item.get(key, 0), reverse=reverse
    )
    for k in sorted_list:
        for i, j in k.items():
            if (
                i == "Дата платежа"
                or i == "Сумма операции"
                or i == "Категория"
                or i == "Описание"
            ):
                some_dict[i] = j
        new_list.append(some_dict)
        new_list = new_list[:5]
    return new_list


def sort_by_date(list_of_dicts: list, key="Дата операции") -> list:
    """Функция сортировки по возрастанию списка эксель_файла по дате"""
    sorted_list = sorted(
        list_of_dicts, key=lambda item: item.get(key, 0), reverse=False
    )
    return sorted_list


def top_of_category(file_path: str) -> dict:
    """Функция которая предоставляет топ 7 платежей по категориям"""
    try:
        k = 0
        sum_operations = 0
        new_dict = {}
        df = pd.read_excel(file_path)
        transactions_by_card = {}
        for index, row in df.iterrows():
            card_number = str(row["Категория"])
            transaction_amount = float(row["Сумма операции с округлением"])
            if card_number in transactions_by_card:
                transactions_by_card[card_number] += transaction_amount
            else:
                transactions_by_card[card_number] = transaction_amount
        for i, j in transactions_by_card.items():
            new_dict[i] = j
            k += 1
            if k > 6:
                sum_operations += int(j)
                break
        new_dict["Остальные"] = sum_operations
        return new_dict
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути '{file_path}'")


def total_amount(list_of_dicts: list) -> int:
    """Функция считающая общую сумму трат"""
    suma = 0
    for i in list_of_dicts:
        for key, value in i.items():
            if key == "Сумма операции с округлением":
                suma += int(value)
    return suma


def filter_transactions_by_range(
    transactions: list, target_date_str: str, range_type: str = "m"
) -> list:
    """Функция фильтрации операций по дате с диапазоном"""
    try:
        target_date = datetime.strptime(target_date_str, "%d.%m.%Y").date()
    except ValueError:
        print("Ошибка: Неверный формат целевой даты. Используйте формат 'DD.MM.YYYY'.")
        return []
    filtered_transactions = []
    for transaction in transactions:
        if "Дата платежа" not in transaction:
            continue
        try:
            transaction_date_str = transaction["Дата платежа"]
            transaction_date = datetime.strptime(
                str(transaction_date_str), "%d.%m.%Y"
            ).date()
        except ValueError:
            continue
        if range_type == "w":
            target_week_start = target_date - timedelta(days=target_date.weekday())
            target_week_end = target_week_start + timedelta(days=6)
            if target_week_start <= transaction_date <= target_week_end:
                filtered_transactions.append(transaction)
        elif range_type == "m":
            if (
                transaction_date.year == target_date.year
                and transaction_date.month == target_date.month
            ):
                filtered_transactions.append(transaction)
        elif range_type == "y":
            if transaction_date.year == target_date.year:
                filtered_transactions.append(transaction)
        else:
            print("Ошибка: Неверный тип диапазона. Используйте 'w', 'm' или 'y'.")
            return []
    return filtered_transactions


def calculate_expenses_by_category(transactions: list) -> list:
    """Функция собирающая со списка все категории и траты"""
    category_expenses = defaultdict(float)
    for transaction in transactions:
        if "Категория" not in transaction or "Сумма операции" not in transaction:
            continue
        try:
            amount = float(transaction["Сумма операции"])
        except ValueError:
            print(
                f"Предупреждение: Неверный формат суммы '{transaction['Сумма операции']}'. Пропускаю: {transaction}"
            )
            continue
        category = transaction["Категория"]
        if amount < 0:
            category_expenses[category] += amount
    result_list = []
    for category, total_expense in category_expenses.items():
        result_list.append({"Категория": category, "потрачено": abs(total_expense)})
    return result_list


def sum_for_two_categories(transactions: list) -> list:
    """Функция для подсчета переводов и снятий"""
    nal, per = 0, 0
    new_list = []
    for d in transactions:
        for key, value in d.items():
            if value == "Наличные":
                nal += d["Сумма операции"]
            if value == "Переводы":
                per += d["Сумма операции"]
    new_list.append({"category": "Наличные", "amount": abs(nal)})
    new_list.append({"category": "Переводы", "amount": abs(per)})
    return new_list


def sum_for_ap_categories(transactions: list) -> list:
    """Функция для подсчета пополнений"""
    nal, per, pr = 0, 0, 0
    new_list = []
    for d in transactions:
        for key, value in d.items():
            if value == "Пополнения":
                nal += d["Сумма операции"]
            if value == "Кэшбэк за обычные покупки":
                per += d["Сумма операции"]
            if value == "Проценты на остаток":
                pr += d["Сумма операции"]

    new_list.append({"category": "Пополнения", "amount": abs(nal)})
    new_list.append({"category": "Проценты на остаток", "amount": abs(per)})
    new_list.append({"category": "Кэшбэк за обычные покупки", "amount": abs(pr)})
    return new_list
