import string

from fast_autocomplete import AutoComplete

import connections.db_connection as db
from apis import iexcloud_api_connection as iex_api_connection, yfinance_api_connection as yf_api_connection
from model.Ticker import TickerSchema


def get_tickers(tickers):
    results = iex_api_connection.get_realtime_data(tickers)
    return TickerSchema().dump(results, many=True)


def search_for_ticker(search_query):
    symbols = db.get_symbols_data()
    valid_chars = "-."
    valid_chars += string.ascii_lowercase
    valid_chars += string.ascii_uppercase
    autocomplete = AutoComplete(words=symbols, valid_chars_for_string=valid_chars)
    result = autocomplete.search(word=search_query, max_cost=0, size=7)
    return result


def save_symbols():
    symbols = iex_api_connection.get_all_symbols()
    dictionary_of_symbols = {}
    for sym in symbols.json():
        dictionary_of_symbols[sym["symbol"]] = sym
    return db.save_symbols(dictionary_of_symbols)


def save_exchanges():
    exchanges = iex_api_connection.get_all_exchanges()
    return db.save_exchanges(exchanges)


def get_options(ticker):
    options_result = yf_api_connection.get_options(ticker)
    return options_result
