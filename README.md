# Data query API for Financial Markets course at MIT Sloan

The package provides a high-level API for interacting with various Financial data made available on Nuvolos for the Financial Markets course of Andrea Vedolin at MIT Sloan (Fall Semester, 2022).

The main functionality of the package is to load data from various data sources ("universes"):

```
my_data = get(ticker, universe, frequency, date_start, date_end)
```

After the call `my_data` will contain a `pandas.DataFrame` object - if the query cannot find corresponding records, the DataFrame will be empty.

## Coverage

The package currently loads the following universes:

* equities,
* factors,
* indices.

## Modules

### Equities universe

In this universe the user can filter the database for tickers and will receive a pandas dataframe with the following structure:
|date|ticker|price|market_cap|total_return|
|:--:|:----:|:---:|:--------:|:----------:|

Note, that the price corresponds to the adjusted price and is denominated in USD.

### Factors universe

In this universe the user can filter the database for factors. 
* The factor's type can be either total return or excess return. 
   * The `type` "Total return" only corresponds to the risk-free rate (ticker:rf).
   * Every other factor the `type` is excess return. 

The returned dataframe has the following structure:
|date|ticker|value|
|:--:|:----:|:---:|

### Indices universe

In this universe the user can obtain data regarding different indices that are in the database based on tickers. The returned dataframe has the following structure:
|date|ticker|total_return|
|:--:|:----:|:----------:|

## UsageA

### `get`

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

Example code:
```
data = nvdata.get(ticker='GOOGL', universe='equities', frequency='monthly', date_start='2010-01-01', date_end='2020-12-31')
```
