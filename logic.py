from fast_autocomplete import AutoComplete

import connections.db_connection as db
import iexcloud_api_connection as api_connection
from model.Ticker import TickerSchema


def get_tickers(tickers):
    results = api_connection.get_realtime_data(tickers)
    return TickerSchema().dump(results, many=True)


def search_for_ticker(search_query):
    symbols = db.get_symbols_data()
    autocomplete = AutoComplete(words=symbols)
    result = autocomplete.search(word=search_query, max_cost=0, size=7)
    return result


def save_symbols():
    symbols = api_connection.get_all_symbols()
    dict = {}
    for sym in symbols.json():
        dict[sym["symbol"]] = sym
    return db.save_symbols(dict)


def save_exchanges():
    exchanges = api_connection.get_all_exchanges()
    return db.save_exchanges(exchanges)
