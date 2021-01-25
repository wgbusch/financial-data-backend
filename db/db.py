import csv
import datetime
import json
import os
import re
import sys

import pandas as pd
from tqdm import tqdm
import numpy as np

# Data Source
import yfinance as yf
from datetime import datetime as dt

from TickersController import get_initial_list_of_tickers

MARKET_DATA_DIRECTORY = "data/market_data/"
HISTORICAL_DATA_DIRECTORY = "data/historical_data/"
OPTIONS_DATA_DIRECTORY = "data/options/"
COLUMNS_STATE_DIRECTORY = "data/columns_state/"
COLUMNS_STATE = COLUMNS_STATE_DIRECTORY + 'columns_state.txt'


class db:
    list_of_tickers = []

    def __init__(self):

        if not os.path.exists(MARKET_DATA_DIRECTORY):
            os.mkdir(MARKET_DATA_DIRECTORY)
        if not os.path.exists(HISTORICAL_DATA_DIRECTORY):
            os.mkdir(HISTORICAL_DATA_DIRECTORY)
        if not os.path.exists(OPTIONS_DATA_DIRECTORY):
            os.mkdir(OPTIONS_DATA_DIRECTORY)
        if not os.path.exists(COLUMNS_STATE_DIRECTORY):
            os.mkdir(COLUMNS_STATE_DIRECTORY)

        with open('data\initial_tickers_list.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    # global exportList
                    self.list_of_tickers.append({"symbol": row[0], "name": row[1], "is_etf": row[4]})
                    line_count += 1
            print(f'Processed {line_count} lines.')

    def get_from_historical_data(self, symbols, tick='1d', interval=1):
        response = []
        for symbol in tqdm(symbols):
            file_name = HISTORICAL_DATA_DIRECTORY + symbol + "_" + tick + ".csv"
            try:
                df = pd.read_csv(file_name)
            except IOError:
                sys.stdout = open(os.devnull, "w")

                currentDate = datetime.date.today()

                df = yf.download(tickers=symbol, end=currentDate, interval=tick)
                ticker_complete_info = list(filter(lambda ticker: ticker["symbol"] == symbol, self.list_of_tickers))[0]

                df["Symbol"] = np.array(ticker_complete_info["symbol"])
                df["Name"] = np.array(ticker_complete_info["name"])
                df["Is_ETF"] = np.array(ticker_complete_info["is_etf"])
                sys.stdout = sys.__stdout__
                df.to_csv(file_name)

            # get only latest market day
            if (len(df) > 0):
                response.append(df.iloc[[-interval]])
        return pd.concat(response)

    def save_to_historical_data(self, dataframes_for_symbols, tick='1d'):
        errors = []
        for df_symbol in dataframes_for_symbols:
            file_name = HISTORICAL_DATA_DIRECTORY + df_symbol["Symbol"] + "_" + tick + ".csv"
            try:
                df = pd.read_csv(file_name)
                df.append(df_symbol)
                df.to_csv(file_name)
            except Exception:
                errors.append(df_symbol["Symbol"])
        return errors

    def get_options_expiry_dates(self, symbol):
        options_filename = OPTIONS_DATA_DIRECTORY + symbol + ".csv"
        try:
            df = pd.read_csv(options_filename)
        except Exception as e:
            print("Missing options file..." + str(e))
            data = yf.Ticker(symbol)
            df = data.options
            df.to_csv(options_filename)

        return None

    ##columns state view
    def save_columns_state(self, req):
        json_wrapper_for_view = {"isLatest": 1,
                                 "updateDate": str(dt.now().utcnow()),
                                 "data": req}
        try:
            f = open(COLUMNS_STATE, "r+")
            views = json.load(f)
            f.seek(0)
            for view in views:
                view["isLatest"] = 0
            views.append(json_wrapper_for_view)
            json.dump(views, f)
            f.close()
        except Exception as e:
            list_of_views = [json_wrapper_for_view]
            with open(COLUMNS_STATE, 'w') as json_file:
                json.dump(list_of_views, json_file)
        return None

    def get_columns_state(self, view_name):
        f = open(COLUMNS_STATE, "r+")
        views = json.load(f)
        views = list(filter(lambda view_item: view_item["isLatest"] == 1, views))
        if (len(views) > 1):
            return {}
        return json.dumps(views[0]["data"])

    def get_market_data(self):
        market_data_filename = MARKET_DATA_DIRECTORY + str(datetime.date.today()) + ".csv"
        df = pd.read_csv(market_data_filename)
        return df

    def save_market_data(self, df):
        market_data_filename = MARKET_DATA_DIRECTORY + str(datetime.date.today()) + ".csv"
        df.to_csv(market_data_filename, index=False)

    def get_initial_list_of_tickers(self):
        return list(filter(lambda ticker: not bool(re.search('\$[A-Z]|File Creation Time|\.[A-Z]', ticker["symbol"])),
                           self.list_of_tickers))
