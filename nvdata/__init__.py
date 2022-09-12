import pandas as pd

import datetime
from dateutil.parser import parse
from typing import Union, List

from .load.helpers import parse_yaml
from .load.load_equities import load_equity
from .load.load_factors import load_factor
from .load.load_indices import load_index

from .info import get_ticker_info, get_universe_info, get_all_ticker_info

import os.path

try:
    CONFIG_DICT = parse_yaml("/files/data/config.yml")
except FileNotFoundError:
    print(
        f"The package couldn't locate a config.yml in its standard location. Please use the set_config_path() call to set a config.yml file location"
    )


def get(
    ticker: Union[str, List[str]],
    universe: str,
    frequency: str = "monthly",
    start_date: Union[str, datetime.date] = "1980-01-01",
    end_date: Union[str, datetime.date] = "2022-07-31",
    **kwargs,
):
    """
    The function returns data for a given ticker or multiple tickers, from a given universe.

    Arguments:

    ticker: string or list of strings
    universe: string, possible values: "equities", "factors", "indices"
    frequency: string, possible values: "daily", "weekly", "monthly", "quarterly", "yearly".
    start_date: string or datetime.date
    end_date: string or datetime.date

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
            universe_route = CONFIG_DICT[universe]["series"]
        except KeyError:
            raise ValueError(
                f"Universe not found. Available universes: {[universe for universe in CONFIG_DICT.keys()]}"
            )
    else:
        raise TypeError(
            "Invalid ticker type. Please enter the ticker(s) as a string or list of strings!"
        )

    if isinstance(start_date, str):
        start_date = parse(start_date).date()

    if isinstance(end_date, str):
        end_date = parse(end_date).date()

    if isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date):
        if universe == "equities":
            ret_df = load_equity(
                ticker, universe_route, frequency, start_date, end_date
            )
        elif universe == "factors":
            ret_df = load_factor(
                ticker, universe_route, frequency, start_date, end_date
            )
        elif universe == "indices":
            ret_df = load_index(ticker, universe_route, frequency, start_date, end_date)

        return ret_df


def set_config_path(path: str):
    global CONFIG_DICT
    try:
        CONFIG_DICT = parse_yaml(path)
    except:
        print(
            "Could not read your configuration file. Please check your file and the yml layout."
        )
    return


def ticker_info(
    ticker: Union[str, List[str]],
    universe: str,
    **kwargs,
):

    """
    The function returns basic information for a given ticker or multiple tickers, from a given universe.

    Arguments:

    ticker: string or list of strings
    universe: string, possible values: "equities", "factors", "indices"

    Behaviour:
    Prints information about the queried tickers.

    Information returned:

    name: the name corresponding to the product (if possible)
    start_date: the first available data date for the given ticker
    last_date: the last available data date for the given ticker
    types: the available data types for the given ticker
    frequency: the available frequency types for the given ticker
    """

    if isinstance(ticker, str) or isinstance(ticker, list):
        try:
            universe_route = CONFIG_DICT[universe]["metadata"]
        except KeyError:
            raise ValueError(
                f"Universe not found. Available universes: {[universe for universe in CONFIG_DICT.keys()]}"
            )
    else:
        raise TypeError(
            "Invalid ticker type. Please enter the ticker(s) as a string or list of strings!"
        )

    ret_dict = get_ticker_info(ticker, universe_route)

    return ret_dict


def universe_info(
    universe: str,
    **kwargs,
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
    tickers_no: the number of different tickers in the universe

    """

    try:
        universe_route = CONFIG_DICT[universe]["metadata"]
    except KeyError:
        raise ValueError(
            f"Universe not found. Available universes: {[universe for universe in CONFIG_DICT.keys()]}"
        )

    ret_dict = get_universe_info(universe_route)

    return ret_dict


def ticker_list(
    universe: str,
    **kwargs,
):

    """
    The function returns description of all tickers in a given universe.

    Arguments:

    universe: string, possible values: "equities", "factors", "indices"

    Behaviour:
    returns a pandas.DataFrame object

    Information returned:

    ticker: ticker of the product
    name: name of the product
    start_date: the first available data point for the ticker
    last_date: the last available data point for the ticker
    nobs: number of data observations

    """
    
    try:
        universe_route = CONFIG_DICT[universe]["metadata"]
    except KeyError:
        raise ValueError(
            f"Universe not found. Available universes: {[universe for universe in CONFIG_DICT.keys()]}"
        )

    ret_df = get_all_ticker_info(universe_route)
    return ret_df
