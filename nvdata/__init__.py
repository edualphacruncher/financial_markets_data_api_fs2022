import pandas as pd

import datetime
from dateutil.parser import parse
from typing import Union

from load.helpers import parse_yaml
from load.load_equities import load_equity
from load.load_factors import load_factor
from load.load_indices import load_index

CONFIG_DICT = parse_yaml("config.yml")


def get(
    ticker: Union[str, list],
    universe: str,
    frequency: str = "daily",
    date_start: Union[str, datetime.date] = "1980-01-01",
    date_end: Union[str, datetime.date] = "2020-06-30",
    **kwargs,
):
    """
    The function returns data for a given ticker or multiple tickers, from a given universe.

    Arguments:

    ticker: string or list of strings
    universe: string, possible values: "equities", "factors", "indices"
    frequency: string, possible values: "daily", "weekly", "monthly", "quarterly", "yearly".
    date_start: string or datetime.date
    date_end: string or datetime.date

    Behaviour:
    Returns a pandas.DataFrame object.
    If no tickers are valid, then the returned object is empty.

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
            universe_route = CONFIG_DICT[universe]
        except KeyError:
            raise ValueError(
                f"Universe not found. Available universes: {[universe for universe in CONFIG_DICT.keys()]}"
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

def set_config_path(path: str):
    global CONFIG_DICT
    try:
        CONFIG_DICT = parse_yaml(path)
    except:
        print("Could not read your configuration file. Please check your file and the yml layout.")
    return

def ticker_info(
    ticker: Union[str, list],
    universe: str,
    frequency: str = "daily",
    **kwargs,
):
    
    """
    The function returns basic information for a given ticker or multiple tickers, from a given universe.

    Arguments:

    ticker: string or list of strings
    universe: string, possible values: "equities", "factors", "indices"
    frequency: string, possible values: "daily", "weekly", "monthly", "quarterly", "yearly".
    
    Behaviour:
    Prints information about the queried tickers.
    
    Information returned:
    
    name: the name corresponding to the product (if possible)
    start_date: the first available data date for the given ticker
    last_date: the last available data date for the given ticker
    types: the available data types for the given ticker
    
    """
    
    return

def universe_info(
    universe: str,
):
    
    """
    The function returns basic information for a given universe.

    Arguments:

    universe: string, possible values: "equities", "factors", "indices"
    
    Behaviour:
    Prints information about the queried universe.
    
    Information returned:
    
    start_date: the first available data date for the given universe
    last_date: the last available data date for the given universe
    tickers: the number of different tickers in the universe
        
    """
    
    return

def ticker_list(
    universe: str,
):
    
    """
    The function returns description of all tickers in a given universe.

    Arguments:

    universe: string, possible values: "equities", "factors", "indices"
    
    Behaviour:
    returns a pandas.DataFrame object
    
    Information returned:
    
    name: name of the product
    ticker: ticker of the product
    start_date: the first available data point for the ticker
    last_date: the last available data point for the ticker
    nobs: number of data observations
        
    """
    return