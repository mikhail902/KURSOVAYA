import json

from reports import *
from services import *
from utils import *
from views import *

import requests

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
        user_input = input("""\n1. Траты в рабочий/выходной день\n""")
        if user_input == "1":
            with open(PATH_TO_JSON, "w", encoding="utf-8") as f:
                json.dump(
                    spending_by_workday(df, "23.07.2021"),
                    f,
                    indent=4,
                    ensure_ascii=False,
                )
                print("Ответ записан в JSON-файл!")
