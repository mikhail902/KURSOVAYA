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
