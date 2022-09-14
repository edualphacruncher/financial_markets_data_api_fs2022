import pandas as pd
from typing import List

TYPE_CODES = {
            "pu": "Price Unadjusted",
            "tr": "Total Return",
            "rwd": "Return without Dividends",
            "mc": "Market Capitalization",
            "tv": "Trading Volume",
            "so": "Shares Outstanding",
            "pa": "Price Adjusted",
            "er": "Excess Return",
            "trh": "Total Return Hedged"
}

INVERSE_TYPE_CODES = {
    "Price Unadjusted": "pu",
    "Total Return": "tr",
    "Excess Return": "er",
    "Return without Dividends": "rwd",
    "Market Capitalization": "mc",
    "Trading Volume": "tv",
    "Shares Outstanding": "so",
    "Price Adjusted": "pa",
    "Total Return Hedged": "trh"
}

FREQUENCY_CODES = {
            "m": "monthly",
            "d": "daily",
            "w": "weekly",
            "q": "quarterly",
            "y": "yearly"
}

INVERSE_FREQUENCY_CODES = {
            "monthly": "m",
            "daily": "d",
            "weekly": "w",
            "quarterly": "q",
            "yearly": "y"
}



def convert_type_code(type_list: List[str]):
    return [TYPE_CODES[t] for t in type_list]


def convert_frequency_code(frequency_list: List[str]):
    return [FREQUENCY_CODES[f] for f in frequency_list]


def get_ticker_info(ticker: list, universe_metadata_path: str):

    """
    Info function that returns the basic information on the given ticker.
    Tha same function is used for all the universes as they have similar format.
    """

    univ = pd.read_feather(universe_metadata_path)

    if isinstance(ticker, str):
        ticker = [ticker]

    ret_dict = {}
    for tick in ticker:
        df_filt = univ[(univ.ticker == tick)]
        ticker_meta = {
            "name": df_filt.name.iloc[0,0],
            "start_date": df_filt.min_date.min(),
            "last_date": df_filt.max_date.max(),
            "types": convert_type_code(df_filt.type.unique().tolist()),
            "frequency": convert_frequency_code(df_filt.frequency.unique().tolist()),
        }

        ret_dict[tick] = ticker_meta

    return ret_dict


def get_universe_info(universe_metadata_path: str):
    """
    Info function to return universe info.
    """

    univ = pd.read_feather(universe_metadata_path)

    ret_dict = {
        "start_date": univ.min_date.min(),
        "last_date": univ.max_date.max(),
        "tickers_no": len(univ.ticker.unique()),
    }

    return ret_dict


def get_all_ticker_info(universe_metadata_path: str):
    """
    Info function to return infos on all tickers from one universe in a
    pd.DataFrame format.
    """

    univ = pd.read_feather(universe_metadata_path)

    return univ
