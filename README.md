# Data query API for Financial Markets course at MIT Sloan

This package provides tools for straightforward data loading from specified universes.
With the get function the user can specify the tickers, universe, frequency and date range and will get a pandas dataframe as a result.
The package currently have three modules to load three different universe:
* equities
* factors
* indices.

## Modules
### Equities universe
In this universe the user can filter the database for tickers and will receive a pandas dataframe with the following structure:
|date|ticker|price|market_cap|total_return|
|:--:|:----:|:---:|:--------:|:----------:|

Note, that the price corresponds to the adjusted price and is denominated in USD.

### Factors universe
In this universe the user can filter the database for factors. The factor's type can be either total return or excess return. Total return only corresponds to the risk-free rate (ticker:rf), for evert factor the type is excess return. The returned dataframe has the following structure:
|date|ticker|value|
|:--:|:----:|:---:|

### Indices universe
In this universe the user can obtain data regarding different indices that are in the database based on tickers. The returned dataframe has the following structure:
|date|ticker|total_return|
|:--:|:----:|:----------:|

## Usage
### Get function
The get function has 5 parameters:
* ticker
* universe
* frequency
* date_start
* date_end.

The ticker can be a string or a list of strings that exist in the given universe. In case the ticker does not exist, the function will return an empty dataframe.

The universe should be selected from the above presented list and entered as a string.

The frequency can vary from daily to yearly in different sequences based on the universe. For more details see the error message if wrong frequency is entered. By default the frequency is set daily.

Date_start and date_end corresponds to the range in between the data is required. It can be a datetime.date or string format. If the database contains no avaialable data for the given period, an empty dataframe is returned.

The config file contains the source of the data files that contains all info about a universe. By default that folder is in the same hieararcy level as the working folder and called *data*. In case the user wants to specify otherwise, changes in the config file are required.

Example code:
```
data = nvdata.get(ticker='GOOGL', universe='equities', frequency='monthly', date_start='2010-01-01', date_end='2020-12-31')
```