import pandas as pd


def get_ticker_info(ticker: list, universe_path: str):

    """
    Info function that returns the basic information on the given ticker.
    Tha same function is used for all the universes as they have similar format.
    """

    univ = pd.read_feather(universe_path)
    univ = univ[(univ.currency == "USD") & (univ.type == "Total Return")]

    if isinstance(ticker, str):
        ticker = [ticker]

    ret_dict = {}
    for tick in ticker:
        df_filt = univ[(univ.ticker == tick)]
        ticker_meta = {
            "name": df_filt.name.iloc[0],
            "start_date": df_filt.date.min(),
            "end_date": df_filt.date.max(),
            "types": df_filt.type.unique().tolist(),
            "frequency": df_filt.frequency.unique().tolist(),
        }

        ret_dict[tick] = ticker_meta

    return ret_dict


def get_universe_info(universe_path: str):
    """
    Info function to return universe info.
    """

    univ = pd.read_feather(universe_path)

    ret_dict = {
        "start_date": univ.date.min(),
        "end_date": univ.date.max(),
        "tickers_no": len(univ.ticker.unique()),
    }

    return ret_dict


def get_all_ticker_info(universe_path: str):
    """
    Info function to return infos on all tickers from one universe in a
    pd.DataFrame format.
    TODO write faster function with groupby
    """

    univ = pd.read_feather(universe_path)

    ret_dict = {}
    for tick in univ.ticker.unique():
        df_filt = univ[(univ.ticker == tick)]
        ticker_meta = {
            "name": df_filt.name.iloc[0],
            "start_date": df_filt.date.min(),
            "end_date": df_filt.date.max(),
            "nobs": df_filt.shape[0],
        }

        ret_dict[tick] = ticker_meta

    ret_df = pd.DataFrame.from_dict(ret_dict, orient="index")
    ret_df = ret_df.reset_index().rename(columns={"index": "ticker"})

    return ret_df
