import os

import pyEX as p
import requests
from model.Ticker import Ticker

c = p.Client()
iex_endpoint = 'https://cloud.iexapis.com/v1'
all_exchanges = '/ref-data/market/us/exchanges'
all_symbols = '/ref-data/symbols'


def construct_ticker(iex_ticker):
    iex_quote = iex_ticker["quote"]

    symbol = iex_quote["symbol"]
    name = iex_quote["companyName"]
    open = iex_quote["open"] if iex_quote["open"] else iex_quote["iexOpen"]
    low = iex_quote["low"]
    close = iex_quote["close"] if iex_quote["close"] else iex_quote["iexClose"]
    volume = iex_quote["volume"] if iex_quote["volume"] else iex_quote["iexVolume"]
    high = iex_quote["high"]
    if " ETF" in name:
        is_etf = True
        name = name.split('-')[-1]
    else:
        is_etf = False
    ask = iex_quote["iexAskPrice"]
    bid = iex_quote["iexBidPrice"]
    change = iex_quote["change"]
    change_percent = iex_quote["changePercent"]
    ytd_change = iex_quote["ytdChange"]
    quote = iex_quote["latestPrice"]
    quote_timestamp = iex_quote["latestTime"]
    return Ticker(symbol, name=name, open=open, low=low,
                  close=close, volume=volume, high=high,
                  is_etf=is_etf, ask=ask, bid=bid,
                  change=change, change_percent=change_percent,
                  ytd_change=ytd_change, quote=quote, quote_timestamp=quote_timestamp)


def get_realtime_data(tickers):
    if not tickers:
        return []
    r = []
    er2 = c.bulkBatch(tickers, fields=['quote'])

    if len(tickers) == 1:
        r.append(construct_ticker(er2))
    else:
        for ticker in er2:
            try:
                r.append(construct_ticker(er2[ticker]))
            except Exception as e:
                print("could not find symbol")
    return r


def get_all_symbols():
    r = requests.get(url='https://cloud.iexapis.com/v1' + all_symbols,
                     params={'token': os.environ["IEX_TOKEN"]})
    return r


def get_all_exchanges():
    r = requests.get(url='https://cloud.iexapis.com/v1' + all_exchanges,
                     params={'token': os.environ["IEX_TOKEN"]})
    return r


def get_options(ticker):
    expirations = c.optionExpirations(ticker)
    options = []
    for opt in expirations:
        options.append(c.options(opt, ticker))
    return {"expirations": expirations, "options": options}
