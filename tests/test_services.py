from src.services import *


def test_service(search):
    assert function_for_search("Каршеринг") == search
    assert categories_with_up_cashback(excel_transaction(PATH_TO_EXCEL), 2020, 7) == {
        "Аптеки": 9,
        "Красота": 0,
        "Транспорт": 4,
    }
    assert investment_bank("02.2020", excel_transaction(PATH_TO_EXCEL), 50) == 177.15
