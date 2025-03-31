import pytest

from src.reports import *

PATH_TO_EXCEL = "C:/Users/Sator/PycharmProjects/KURSOVAYA/data/operations.xlsx"
df = pd.read_excel(PATH_TO_EXCEL)


def test_spending_by_workday(spending_test, spending_by_category_test):
    assert spending_by_workday(df, "02.02.2020") == {
        "Выходной день": 333.74,
        "Рабочий день": 721.87,
    }
    assert spending_by_weekday(df, "02.02.2020") == spending_test
    assert (
        spending_by_category(df, "Каршеринг", "31.12.2021") == spending_by_category_test
    )
