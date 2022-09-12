import pandas as pd
import datetime
from typing import Union

from ..info import INVERSE_TYPE_CODES, INVERSE_FREQUENCY_CODES

def load_index(
    ticker: list,
    universe_path: str,
    frequency: str,
    start_date: Union[str, datetime.date],
    end_date: Union[str, datetime.date],
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
        & (ind_univ.date >= start_date)
        & (ind_univ.date <= end_date)
        & (ind_univ.frequency == INVERSE_FREQUENCY_CODES[frequency])
        & (ind_univ.currency == "USD")
        & (ind_univ.type == "Total Return")
    ]

    ind_df_filt = ind_df_filt[["date", "ticker", "value"]]
    ind_df_filt = ind_df_filt.rename(columns={"value": "total_return"})
    ind_df_filt = ind_df_filt.reset_index(drop=True)

    return ind_df_filt
