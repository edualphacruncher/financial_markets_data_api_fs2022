import pandas as pd
from loading_functions.helpers import parse_yaml
from loading_functions.load_equities import load_equity
import datetime

config_dict = parse_yaml('config.yml')

def get(ticker:str or list, universe:str, date_start:datetime.date, date_end:datetime.date, **kwargs):
    """
    The function returns the desired data for the given ticker, from a given universe.
    The ticker can be given as a string, or a list of strings. If invalid ticker
    is entered, the function will return and empty dataframe. The start and end
    dates should be specified as datetime.date objects.
    
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
        except Exception:
            print('Please use existing universe!')

        if isinstance(date_start, datetime.date) and isinstance(date_end, datetime.date):
            ret_df = load_equity(ticker, universe_route, date_start, date_end)
            return ret_df
        else:
            print('Please use datetime.date format!')
    else:
        print('Please enter the ticker(s) as a string or list of strings!')