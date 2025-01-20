import os

import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")


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



a={
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
      "amount": "8221.37",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560"
  }
print(conversion(a))