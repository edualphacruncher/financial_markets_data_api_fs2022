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
            "last_date": df_filt.date.max(),
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
        "last_date": univ.date.max(),
        "tickers_no": len(univ.ticker.unique()),
    }

    return ret_dict


def get_all_ticker_info(universe_path: str):
    """
    Info function to return infos on all tickers from one universe in a
    pd.DataFrame format.
    """

    univ = pd.read_feather(universe_path)

    grouped_df = univ.groupby(["ticker", "name"])

    date_start = grouped_df[["date"]].min()
    date_end = grouped_df[["date"]].max()
    nobs = grouped_df[["date"]].count()

    joined_df = date_start.join(
        date_end, on=["ticker", "name"], lsuffix="_start", rsuffix="_end"
    ).join(nobs, on=["ticker", "name"])

    joined_df = joined_df.reset_index().rename(
        columns={"date": "nobs", "date_start": "start_date", "date_end": "last_date"}
    )

    return joined_df
