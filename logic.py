import iexcloud_api_connection as api_connection
from model.Ticker import TickerSchema


def get_tickers(tickers):
    results = api_connection.get_realtime_data(tickers)

    return TickerSchema().dump(results, many=True)
