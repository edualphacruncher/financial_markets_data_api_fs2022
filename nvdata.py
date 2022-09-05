import pandas as pd
from load.helpers import parse_yaml
from load.load_equities import load_equity
import datetime as dt

config_dict = parse_yaml('config.yml')

def get(ticker:str or list, universe:str, date_start:str or datetime.date, date_end:str or datetime.date, **kwargs):
    """
    The function returns the desired data for the given ticker, from a given universe.
    The ticker can be given as a string, or a list of strings. If invalid ticker
    is entered, the function will return and empty dataframe. The start and end
    dates should be specified as datetime.date objects or in a string format
    like '2020-01-01'.
    
    List of available universe and returned data formats:
        * equities: pandas dataframe with the following columns:
            * date
            * ticker
            * price
            * market_cap
            * total_return
            price and market_cap are denominated in USD
    """

    if isinstance(ticker, str) or isinstance(ticker, list):
        try:
            universe_route = config_dict[universe]
        except KeyError:
            print('Please use existing universe!')
            return None
    else:
        print('Please enter the ticker(s) as a string or list of strings!')
        return None

    if isinstance(date_start, str):
        try:
            date_start = dt.datetime.strptime(date_start,'%Y-%m-%d').date()
        except ValueError:
            print('Please use datetime.date or the YYYY-MM-DD format for dates')
            return None

    if isinstance(date_end, str):
        try:
            date_end = dt.datetime.strptime(date_end,'%Y-%m-%d').date()
        except ValueError:
            print('Please use datetime.date or the YYYY-MM-DD format for dates')
            return None

    if isinstance(date_start, dt.date) and isinstance(date_end, dt.date):
            ret_df = load_equity(ticker, universe_route, date_start, date_end)
            return ret_df
