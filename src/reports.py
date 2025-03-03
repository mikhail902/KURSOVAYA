from typing import Optional

import pandas as pd


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    pass


def spending_by_weekday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    pass


def spending_by_workday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    pass
