import pandas as pd

import datetime
from dateutil.parser import parse
from typing import Union

from load.helpers import parse_yaml
from load.load_equities import load_equity
from load.load_factors import load_factor
from load.load_indices import load_index

config_dict = parse_yaml("config.yml")


def get(
    ticker: Union[str, list],
    universe: str,
    frequency: str = "daily",
    date_start: Union[str, datetime.date] = "1980-01-01",
    date_end: Union[str, datetime.date] = "2020-06-30",
    **kwargs,
):
    """
    The function returns the desired data for the given ticker, from a given universe.
    The ticker can be given as a string, or a list of strings. If invalid ticker
    is entered, the function will return and empty dataframe.

    Frequency of the data can be specified by the frequency parameter, by default
    daily data is returned. Other possible frequencies are weekly, monthly,
    quarterly and yearly.

    The start and end dates should be specified as datetime.date objects or in a
    string format like '2020-01-01'.

    List of available universe and returned data formats:
        * equities: pandas dataframe with the following columns:
            * date
            * ticker
            * price
            * market_cap
            * total_return
            price and market_cap are denominated in USD
        * factors: pandas dataframe with the following columns
            * date
            * ticker
            * value
        * indices: pandas dataframe with the following columns
            * date
            * ticker
            * total_return
    """

    if isinstance(ticker, str) or isinstance(ticker, list):
        try:
            universe_route = config_dict[universe]
        except KeyError:
            raise ValueError(
                f"Universe not found. Available universes: {[universe for universe in config_dict.keys()]}"
            )
    else:
        raise TypeError(
            "Invalid ticker type. Please enter the ticker(s) as a string or list of strings!"
        )

    if isinstance(date_start, str):
        date_start = parse(date_start).date()

    if isinstance(date_end, str):
        date_end = parse(date_end).date()

    if isinstance(date_start, datetime.date) and isinstance(date_end, datetime.date):
        if universe == "equities":
            ret_df = load_equity(
                ticker, universe_route, frequency, date_start, date_end
            )
        elif universe == "factors":
            ret_df = load_factor(
                ticker, universe_route, frequency, date_start, date_end
            )
        elif universe == "indices":
            ret_df = load_index(ticker, universe_route, frequency, date_start, date_end)

        return ret_df
