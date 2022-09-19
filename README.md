
# Data API for Financial Markets, FS 2022

## Installation

To install the package, type

```
pip install git+https://github.com/edualphacruncher/financial_markets_data_api_fs2022
```

## Basic usage in python

To use in python, import the package:

```
import nvdata as nd
```

To obtain time series information, use the `get` method:

```
amzn = nd.get("AMZN/84788", "equities", "monthly", start_date = "1999-01-01", end_date = "2018-12-31")
```

To obtain information about all the tickers in a universe:

```
ticker_list = nd.ticker_list("equities")
```

## Basic usage in R via `reticulate`

Make sure that you have the `reticulate` package installed in R.

Then:
```
library(reticulate)
nd <- reticulate::import("nvdata")
amzn <- nd.get("AMZN/84788", "equities", "monthly", start_date = "1999-01-01", end_date = "2018-12-31", reticulate =T)
```
to get the same data frame but now in an R environment. Note the final parameter `reticulate` to the `get()` call! This is required to resolve datatype casting issues that exist between `datetime.date()` and R date objects.



