import datetime
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
PATH_TO_EXCEL = "C:/Users/Sator/PycharmProjects/KURSOVAYA/data/operations.xlsx"


def conversion(dictionary: dict) -> any:
    """Считывания курса валюты через API"""
    try:
        url = "https://api.apilayer.com/exchangerates_data/convert"
        payload = {
            "amount": dictionary["operationAmount"]["amount"],
            "from": dictionary["operationAmount"]["currency"]["code"],
            "to": "RUB",
        }
        headers = {"apikey": API_KEY}
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
    time_now = datetime.datetime.now()
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
