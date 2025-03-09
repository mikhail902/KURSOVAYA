from src.services import *


def test_service(spending_test):
    assert function_for_search("Каршеринг") == spending_test
    assert categories_with_up_cashback(excel_transaction(PATH_TO_EXCEL), 2020, 7) == {'Аптеки': 9, 'Красота': 0, 'Транспорт': 4}