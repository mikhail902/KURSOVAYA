import datetime

PATH_TO_EXCEL = "C:/Users/Sator/PycharmProjects/KURSOVAYA/data/operations.xlsx"


def time_of_day():
    """Функция считывания времени суток"""
    time_now = datetime.datetime.now()
    h = int(time_now.strftime("%H"))
    if h < 18 | h > 12:
        now_time = "день"
    elif h > 18 | h < 22:
        now_time = "вечер"
    elif h > 4 | h < 12:
        now_time = "утро"
    else:
        now_time = "ночи"
    return now_time


def sort_transactions(excel_file: list) -> list:
    """Функция поиска топ 5 платежей"""
    sorted_list = sorted(excel_file, key=lambda x: x["Сумма операции"], reverse=False)
    return sorted_list[0:6]

def last_four_num()->:
    pass