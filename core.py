# Raw Package
import datetime
import json
import multiprocessing
import os
import re
import sys
from typing import List

import numpy as np
import pandas as pd
# Data Source
import yfinance as yf
from flask import jsonify
from joblib import Parallel, delayed, parallel_backend
# Data viz
from tqdm import tqdm

from db import db

model = ["Open", "High", "Low", "Close", "Adj Close", "Volume", "Symbol", "Name", "Is_ETF"]
pd.options.mode.chained_assignment = None


class mainObj:
    SLICE = 100
    NUMBER_OF_COLUMNS = 0

    exclude = re.compile("^\$[A-Z]$")

    def __init__(self):
        self.db = db.db()
        self.list_of_tickers = self.db.get_initial_list_of_tickers()

    def main_func(self):
        pass

    # 6
    def get_ticker(self, id):
        sys.stdout = open(os.devnull, "w")
        data = yf.Ticker(id).info
        sys.stdout = sys.__stdout__
        df = pd.DataFrame.from_dict(data, orient='columns')
        return df

    # 6
    def download_ticker(self, ticker, interval='1d'):
        sys.stdout = open(os.devnull, "w")
        data = yf.download(tickers=ticker, period='5d', interval=interval)
        sys.stdout = sys.__stdout__
        return data

    # 1
    def get_market_overview(self, watchlist_name: str, start: int, end: int, view_name: str):
        try:
            watchlist = self.get_watchlist(watchlist_name)
            response = []
            if (end is None):
                end = len(watchlist)
            i = start
            while (i + self.SLICE <= end):
                response.extend(self.fetch_today_info(watchlist[i:i + self.SLICE]))
                i += self.SLICE
            if (i < end):
                response.extend(self.fetch_today_info(watchlist[i:end]))

            json_data = json.loads(pd.concat(response).to_json(orient="records"))
            columns_state = self.db.get_columns_state(view_name)
            response = {"data": json_data,
                        "columnDefs": self.add_master_grid_columns(json_data),
                        "columnsState": columns_state
                        }

            return json.dumps(response)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('-------------' + str(e) + '-------------')

    # 2
    def get_watchlist(self, watchlist: str) -> List[dict]:
        if (watchlist == 'all'):
            return self.list_of_tickers

    # 3
    def fetch_today_info(self, watchlist: List[dict]):
        if (datetime.datetime.today().weekday() in [6, 7]):
            return self.db.get_from_historical_data(list(map(lambda item: item["symbol"], watchlist)))
        missing = []
        response = []
        try:
            df = self.db.get_market_data()
            for ticker in watchlist:
                if (ticker["symbol"] not in df['Symbol'].tolist()):
                    missing.append(ticker)
            if (len(missing) > 0):
                df_missing = self.batch_download(missing)
                df.append(df_missing)
            self.db.save_market_data(df)
            # df.to_csv(market_data_filename, index=False)
        except IOError:
            missing = watchlist
            df = self.batch_download(missing)
            self.db.save_market_data(df)
            # df.to_csv(market_data_filename)
        for ticker in watchlist:
            response.append(df[df['Symbol'] == ticker["symbol"]])
        return response

    # 4
    def batch_download(self, list_of_tickers_to_download):
        currentDate = datetime.date.today()

        manager = multiprocessing.Manager()
        market_data = manager.list()

        with parallel_backend('loky', n_jobs=multiprocessing.cpu_count()):
            Parallel()(delayed(self.get_info_for_ticker)(ticker, market_data, currentDate)
                       for ticker in tqdm(list_of_tickers_to_download))
        df = pd.concat(list(market_data))
        return df

    # 5
    def get_info_for_ticker(self, ticker, market_data, interval='1d'):
        try:
            data = self.download_ticker(ticker["symbol"])
            # sometimes yf returns duplicate data, so we keep only the last row.
            if (len(data) > 1):
                data = data.iloc[[-1]]
            data["Symbol"] = np.array(ticker["symbol"])
            data["Name"] = np.array(ticker["name"])
            data["Is_ETF"] = np.array(ticker["is_etf"])
            market_data.append(data)
        except Exception as e:
            print(e)
            pass

    def add_master_grid_columns(self, data):
        columns_to_retrieve = self.db.get_grid_columns_map(data)
        return columns_to_retrieve

    def save_columns_state(self, req):
        self.db.save_columns_state(req)


if __name__ == '__main__':
    mainObj().main_func()
