## Description

Fullstack Python application which pulls from the Federal Economic Reserves' (FRED) API to obtain free marco-economic and financial time series data to perform an analysis. The backend relies on a PostgreSQL database to store data and forecasted series. Analysis results are then displayed on the frontend using Solara.

The analysis attempts to forecast two times series:
1) Industrial Production: Semiconductor and Other Electronic Component (NAICS = 3344) - IPG3344S
2) Coinbase Bitcoin (USD) - CBBTCUSD

Vector-Error Correction Models are used since the time series are co-integrated with a significant lag-order. The forecasts are not accurate at all and the models need much refining to make accurate predictions, although it is beyond the scope of this exercise. The aim of the project is to use advanced Python features and pull data from a free API. The project instructions are described below.

**Semiconductor model:**
1) *Industrial Production: Semiconductor and Other Electronic Component (NAICS = 3344) - IPG3344S*
2) Manufacturers' New Orders: Information Technology Industries - AITINO
3) Nominal Advanced Foreign Economies U.S. Dollar Index - DTWEXAFEGS
4) 3-Month Treasury Bill Secondary Market Rate, Discount Basis (Percent) - DTB3
5) M2 money supply - WM2NS
6) Unemployment Rate - UNRATE
7) 5-Year Breakeven Inflation Rate - T5YIE
8) CBOE Volatility Index: VIX - VIXCLS
9) CBOE Crude Oil ETF Volatility Index - OVXCLS
10) Equity Market Volatility: Infectious Disease Tracker - INFECTDISEMVTRACKD

**Cryptocurrency model:**
1) *Coinbase Bitcoin (USD) - CBBTCUSD*
2) Manufacturers' New Orders: Information Technology Industries - AITINO
3) Nominal Advanced Foreign Economies U.S. Dollar Index - DTWEXAFEGS
4) 3-Month Treasury Bill Secondary Market Rate, Discount Basis (Percent) - DTB3
5) M2 money supply - WM2NS
6) Unemployment Rate - UNRATE
7) 5-Year Breakeven Inflation Rate - T5YIE
8) CBOE Volatility Index: VIX - VIXCLS
9) CBOE Crude Oil ETF Volatility Index - OVXCLS
10) Equity Market Volatility: Infectious Disease Tracker - INFECTDISEMVTRACKD

![Frontend Demo](./frontend/assets/frontend.gif)

## Usage

1) Set up a PostgreSQL server on your local machine.

2) Rename `example.env` to `.env` and add your database URL to the `DATABASE_URL` environment variable.

3) Set up a [FRED](https://fred.stlouisfed.org/) account and add API key to `FRED_API_KEY` environment variable.

4) Install poetry and run `poetry install` to install project dependencies in `poetry.lock` file.

    * Note that if you want your virtual environment created in the project root run this command:
    ```zsh
    poetry config virtualenvs.in-projct true
    ```

5) To fetch the time series data from the FRED's API, store it in the PostgreSQL database, and perform the analysis to forecast the two series of interest, run the following command with your virtual environment activated:

```zsh
python3 backend/main.py
```

6) Finally, to display the results on the frontend run:

```zsh
uvicorn backend.app:app --reload
```

And open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view results in your browser.

## TODO

* Refine models to obtain actually accurate and realistic predictions.
* Fill Nans with a more advanced method such as multiple imputation, K-Nearest Neighbours, or Bayesian Principal Component Analysis.
* Improve frontend aesthetics.
* Add testing.

### Project Instructions

* **Instructions quoted from [https://www.arjancodes.com/](https://www.arjancodes.com/).**

Write a tool in Python that communicates with a free API, retrieves some data and performs an analysis of that data. For example, you can use the World POP API to retrieve and analyze world population data.

Here are some ideas of how to use the topics covered in the class in this assignment:

1. Communicate with the API using concurrent programming. The challenge is to make sure that API requests stay within the rate limit of the API you're using, but that at the same time retrieving a lot of data doesn't block the application.

2. Graphical user interfaces are not covered in this course, so you could perform an analysis and store the result in a CSV file. Another possibility is to use a framework for dashboards such as Plotly Dash or Streamlit.

3. Add type annotations to the classes and functions you write so they're easy to read and test.

4. Use iterators and generators to write a data processing pipeline that fits in nicely with the existing Python tooling such as itertools but that is also memory-efficient due to using generators.

5. If you want to store the data you retrieve locally in a database, you can use a context manager to manage opening and closing the database connection like I show in the class.

6. Use lamdba functions to define and apply simple filters on your data.

You can take this assignment as far as you like, but I suggest to start simple and as a first step, write a script that retrieves some data from the API using concurrency. After that, expand the program step by step to include processing, filters, and optionally, a basic GUI interface.