import pandas as pd
import datetime
from typing import Union


def load_index(
    ticker: list,
    universe_path: str,
    frequency: str,
    date_start: Union[str, datetime.date],
    date_end: Union[str, datetime.date],
):
    """
    Index loading function that reads the data from files and returns them in
    a standard format. Ticker can be a string or a list of strings. Only the
    total return datatype is returned.
    """

    ind_univ = pd.read_feather(universe_path)

    if isinstance(ticker, str):
        ticker = [ticker]

    ind_df_filt = ind_univ[
        (ind_univ.ticker.isin(ticker))
        & (ind_univ.date >= date_start)
        & (ind_univ.date <= date_end)
        & (ind_univ.frequency == frequency)
        & (ind_univ.currency == "USD")
        & (ind_univ.type == "Total Return")
    ]

    ind_df_filt = ind_df_filt[["date", "ticker", "value"]]
    ind_df_filt = ind_df_filt.rename(columns={"value": "total_return"})
    ind_df_filt = ind_df_filt.reset_index(drop=True)

    return ind_df_filt
