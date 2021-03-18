from model.Ticker import Ticker, TickerSchema
import yfinance as yf
import datetime as dt


def construct_ticker(yf_ticker):
    return Ticker(yf_ticker["symbol"],
                  yf_ticker["shortName"],
                  yf_ticker["open"],
                  yf_ticker["dayLow"],
                  yf_ticker["previousClose"],
                  yf_ticker["volume"],
                  yf_ticker["dayHigh"],
                  yf_ticker["quoteType"] == "ETF",
                  yf_ticker["ask"],
                  yf_ticker["bid"],
                  (yf_ticker["ask"] + yf_ticker["bid"]) / 2,
                  dt.datetime.now())


def get_realtime_data(tickers):
    response_from_api = yf.Tickers(tickers).tickers
    r = []
    for t in response_from_api:
        r.append(construct_ticker(t.info))
    return r
