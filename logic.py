from flask import jsonify

import api_connection
from model.Ticker import Ticker, TickerSchema
import yfinance as yf


def get_tickers(tickers):
    columns = ["name", "symbol", "open", "low",
               "previous_close", "volume", "high",
               "is_etf", "ask", "bid", "quote", "quote_timestamp"]

    results = api_connection.get_realtime_data(tickers)

    ticker_schema = TickerSchema()
    return jsonify({"data": ticker_schema.dump(results, many=True),
                    "columns": columns})
