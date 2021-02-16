# Raw Package

import json

import numpy as np
import pandas as pd
# Data Source
import yfinance as yf


def get_options_expiry_dates(symbol):
    data = yf.Ticker(symbol)
    try:
        expiry_dates = data.options
    except Exception as e:
        return json.dumps({"data": [],
                           "columnDefs": add_detail_grid_columns(),
                           "expiryDates": []})

    option_chain = []
    for date in expiry_dates:
        df_option_chain = data.option_chain(date)
        df_option_chain.calls["expiryDate"] = np.array(date)
        df_option_chain.puts["expiryDate"] = np.array(date)
        df_option_chain.calls["callOrPut"] = np.array("call")
        df_option_chain.puts["callOrPut"] = np.array("put")
        df_option_all = df_option_chain.calls.append(df_option_chain.puts)
        option_chain.append(df_option_all)

    return json.dumps({"data": json.loads(pd.concat(option_chain).to_json(orient="records")),
                       "columnDefs": add_detail_grid_columns(),
                       "expiryDates": expiry_dates})


def add_detail_grid_columns():
    columns_to_retrieve = []
    with open('data/columns_state/OPTIONS_COLUMNS_MAP.txt') as f:
        columns_map = json.load(f)
    for column in columns_map.keys():
        columns_to_retrieve.append(columns_map[column])
    return columns_to_retrieve
