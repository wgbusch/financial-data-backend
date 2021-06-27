import datetime as dt

import yfinance as yf

from data.reference_data.Constants import STRFTIME_DATE_FORMAT
from model.Option import OptionSchema, Option
from model.Ticker import Ticker


def construct_option(yf_option):
    return Option(contract_symbol=yf_option["contractSymbol"],
                  last_trade_date=yf_option["lastTradeDate"],
                  strike=yf_option["strike"],
                  last_price=yf_option["lastPrice"],
                  bid=yf_option["bid"],
                  ask=yf_option["ask"],
                  change=yf_option["change"],
                  percent_change=yf_option["percentChange"],
                  volume=yf_option["volume"],
                  open_interest=yf_option["openInterest"],
                  implied_volatility=yf_option["impliedVolatility"],
                  in_the_money=yf_option["inTheMoney"],
                  contract_size=yf_option["contractSize"],
                  currency=yf_option["currency"])


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
                  change_percent=None,
                  ytd_change=None,
                  quote=(yf_ticker["ask"] + yf_ticker["bid"]) / 2,
                  quote_timestamp=dt.datetime.now())


def get_realtime_data(tickers):
    response_from_api = yf.Tickers(tickers).tickers
    yf.download(tickers, )
    r = []
    for t in response_from_api:
        r.append(construct_ticker(t.info))
    return r


# created_date
def get_historic_data(tickers, start_date=None, end_date=None):
    if (end_date is None):
        end_date = dt.datetime.today().strftime(STRFTIME_DATE_FORMAT)
    else:
        try:
            end_date = dt.datetime.strptime(end_date, STRFTIME_DATE_FORMAT)
        except Exception as e:
            print("Incorrect formatting for end_date, required YYY-mm-dd")
            return None
    if (start_date is None):
        lookback_days = 7
        start_date = end_date - dt.timedelta(lookback_days)
    resppp = yf.download(tickers, start_date, end_date)
    return resppp


def get_options(ticker):
    val = yf.Tickers(ticker).tickers
    expiration_dates = val[0].options
    option_chain = val[0].option_chain(expiration_dates[0])

    calls = []
    for index, option in (option_chain.calls).iterrows():
        calls.append(construct_option(option))
    puts = []
    for index, option in (option_chain.puts).iterrows():
        puts.append(construct_option(option))

    return {"expiration_dates": expiration_dates,
            "calls": OptionSchema().dump(calls, many=True),
            "puts": OptionSchema().dump(puts, many=True)}
