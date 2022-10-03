import pandas as pd
import datetime
from typing import Union

from ..info import INVERSE_TYPE_CODES, INVERSE_FREQUENCY_CODES

def load_treasury_yc(
    ticker: list,
    universe_path: str,
    frequency: str,
    start_date: Union[str, datetime.date],
    end_date: Union[str, datetime.date],
):
    """
    Treasury yield curve loading function that reads the data from files and returns them in
    a standard format. Ticker can be a string or a list of strings. Only the
    total return datatype is returned.
    """

    tr_univ = pd.read_feather(universe_path)

    if isinstance(ticker, str):
        ticker = [ticker]

    tr_df_filt = tr_univ[
        (tr_univ.ticker.isin(ticker))
        & (tr_univ.date >= start_date)
        & (tr_univ.date <= end_date)
        & (tr_univ.frequency == INVERSE_FREQUENCY_CODES[frequency])
        & (tr_univ.currency == "USD")
        & (tr_univ.type == INVERSE_TYPE_CODES["Yield-to-Maturity"])
    ]

    tr_df_filt = ind_df_filt[["date", "ticker", "type", "value"]]
    tr_df_filt = ind_df_filt.reset_index(drop=True)

    return tr_df_filt
