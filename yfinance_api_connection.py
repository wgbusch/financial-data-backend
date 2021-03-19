import datetime as dt

import yfinance as yf

from model.Ticker import Ticker


def construct_ticker(yf_ticker):
    return Ticker(yf_ticker["symbol"],
                  name=yf_ticker["shortName"],
                  open=yf_ticker["open"],
                  low=yf_ticker["dayLow"],
                  close=yf_ticker["previousClose"],
                  volume=yf_ticker["volume"],
                  high=yf_ticker["dayHigh"],
                  is_etf=yf_ticker["quoteType"] == "ETF",
                  ask=yf_ticker["ask"],
                  bid=yf_ticker["bid"],
                  change=None,
                  changePercent=None,
                  ytdChange=None,
                  quote=(yf_ticker["ask"] + yf_ticker["bid"]) / 2,
                  quote_timestamp=dt.datetime.now())


def get_realtime_data(tickers):
    response_from_api = yf.Tickers(tickers).tickers
    r = []
    for t in response_from_api:
        r.append(construct_ticker(t.info))
    return r
