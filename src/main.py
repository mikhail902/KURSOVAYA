import json

import requests

from reports import *
from services import *
from utils import *
from views import *


def get_usd_exchange_rate(api_key1, base_currency="USD", target_currency="RUB"):
    """Функция обмена валюты по курсу"""
    path = "https://api.apilayer.com/currency_data/live"
    headers = {"apikey": api_key}
    params = {"currencies": target_currency, "source": base_currency}
    try:
        response = requests.get(path, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data and data.get("success"):
            rates = data.get("quotes")
            if rates:
                rate_key = f"{base_currency}{target_currency}"
                exchange_rate = rates.get(rate_key)
                if exchange_rate:
                    return exchange_rate
                else:
                    print(f"Ошибка: Не удалось найти курс для {rate_key} в ответе API.")
                    return None
            else:
                print("Ошибка: Ключ 'quotes' не найден в ответе API.")
                return None
        else:
            print(f"Ошибка: Не удалось получить курс обмена. Ответ API: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса API: {e}")
        return None
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат ответа API (ожидался JSON).")
        return None


if __name__ == "__main__":
    user_input = input(
        f"""Выберете, что вас интересует
1. Веб-страницы
2. Сервисы
3. Отчеты
"""
    )
    if user_input == "1":
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

    elif user_input == "2":
        user_input = input(
            """Выберете сервис который вам нужен
        1. Выгодные категории повышенного кэшбэка
        2. Инвесткопилка
        3. Поиск
                           """
        )
        if user_input == "1":
            year = int(
                input(
                    "Введите год, который нужно проанализировать на повышенный кешбэк\n"
                )
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
                json.dump(
                    function_for_search(main_input), f, indent=4, ensure_ascii=False
                )
            print("Ответ записан в JSON-файл!")

    elif user_input == "3":
        df = pd.read_excel(PATH_TO_EXCEL)
        user_input = input(
            """\n1. Траты по категориям
2. Траты по дням недели
3. Траты в рабочий/выходной день\n"""
        )
        if user_input == "1":
            with open(PATH_TO_JSON, "w", encoding="utf-8") as f:
                json.dump(
                    spending_by_category(df, "Каршеринг", "23.07.2021"),
                    f,
                    indent=4,
                    ensure_ascii=False,
                )
                print("Ответ записан в JSON-файл!")

        elif user_input == "2":
            with open(PATH_TO_JSON, "w", encoding="utf-8") as f:
                json.dump(
                    spending_by_weekday(df, "23.07.2021"),
                    f,
                    indent=4,
                    ensure_ascii=False,
                )
                print("Ответ записан в JSON-файл!")

        elif user_input == "3":
            with open(PATH_TO_JSON, "w", encoding="utf-8") as f:
                json.dump(
                    spending_by_workday(df, "23.07.2021"),
                    f,
                    indent=4,
                    ensure_ascii=False,
                )
                print("Ответ записан в JSON-файл!")
