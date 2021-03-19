import pyEX as p

from app import app
from model.Ticker import Ticker

c = p.Client()


def construct_ticker(iex_ticker):
    return Ticker(iex_ticker["quote"]["symbol"],
                  name=iex_ticker["quote"]["companyName"],
                  open=iex_ticker["quote"]["open"],
                  low=iex_ticker["quote"]["low"],
                  close=iex_ticker["quote"]["close"],
                  volume=iex_ticker["quote"]["volume"],
                  high=iex_ticker["quote"]["high"],
                  is_etf=(iex_ticker["stats"]["peRatio"] ** 2 + iex_ticker["stats"]["float"] ** 2 + iex_ticker["stats"][
                      "employees"] ** 2) == 0,
                  ask=iex_ticker["quote"]["iexAskPrice"],
                  bid=iex_ticker["quote"]["iexBidPrice"],
                  change=iex_ticker["quote"]["change"],
                  changePercent=iex_ticker["quote"]["changePercent"],
                  ytdChange=iex_ticker["quote"]["ytdChange"],
                  quote=iex_ticker["quote"]["latestPrice"],
                  quote_timestamp=iex_ticker["quote"]["latestTime"])


def get_realtime_data(tickers):
    app.logger.info('Message entered for ')
    er2 = c.bulkBatch(tickers, fields=['stats', 'quote'])
    app.logger.info('Message exited for ')
    r = []
    if len(tickers) == 1:
        r.append(construct_ticker(er2))
    else:
        for ticker in er2:
            r.append(construct_ticker(er2[ticker]))
    return r
