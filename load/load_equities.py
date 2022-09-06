import pandas as pd
import datetime
from typing import Union


def load_equity(
    ticker: list,
    universe_path: str,
    frequency: str,
    date_start: Union[str, datetime.date],
    date_end: Union[str, datetime.date],
):
    """
    Equity loading function that reads the data from files and returns them in
    a standard format. Ticker can be a string or a list of strings.
    """

    eq_univ = pd.read_feather(universe_path)

    if isinstance(ticker, str):
        ticker = [ticker]

    eq_df_filt = eq_univ[
        (eq_univ.ticker.isin(ticker))
        & (eq_univ.date >= date_start)
        & (eq_univ.date <= date_end)
        & (eq_univ.frequency == frequency)
        & (eq_univ.currency == "USD")
    ]

    eq_df_filt = eq_df_filt.drop(columns=["name", "frequency", "currency"])

    price = get_subset_by_type(eq_df_filt, "Price Adjusted", "price")
    market_cap = get_subset_by_type(eq_df_filt, "Market Capitalization", "market_cap")
    total_return = get_subset_by_type(eq_df_filt, "Total Return", "total_return")

    ret_df = price.join(market_cap.set_index(["date", "ticker"]), on=["date", "ticker"])
    ret_df = ret_df.join(
        total_return.set_index(["date", "ticker"]), on=["date", "ticker"]
    )

    return ret_df


def get_subset_by_type(df, datatype, col_name):
    """
    Returns a subset of the dataframe for only one type, with renamed columns.
    """

    ret_df = df[df.type == datatype].reset_index(drop=True)
    ret_df.rename(columns={"value": col_name}, inplace=True)
    ret_df = ret_df.drop(columns=["type"])

    return ret_df
