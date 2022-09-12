import pandas as pd
import datetime
from typing import Union

from ..info import INVERSE_TYPE_CODES, INVERSE_FREQUENCY_CODES

def load_factor(
    ticker: list,
    universe_path: str,
    frequency: str,
    start_date: Union[str, datetime.date],
    end_date: Union[str, datetime.date],
):
    """
    factor loading function that reads the data from files and returns them in
    a standard format. Ticker can be a string or a list of strings.
    """

    fact_univ = pd.read_feather(universe_path)

    if isinstance(ticker, str):
        ticker = [ticker]

    fact_df_filt = fact_univ[
        (fact_univ.ticker.isin(ticker))
        & (fact_univ.date >= start_date)
        & (fact_univ.date <= end_date)
        & (fact_univ.frequency == INVERSE_FREQUENCY_CODES[frequency])
    ]

    fact_df_filt = fact_df_filt[["date", "ticker", "value"]]
    fact_df_filt = fact_df_filt.reset_index(drop=True)

    return fact_df_filt
