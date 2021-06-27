import json

__exchange_data_path__ = 'data/reference_data/exchanges_data.json'
__symbols_data_path__ = 'data/reference_data/symbols_data.json'
__saxo_instruments_data_path__ = 'data/reference_data/saxo_instruments.json'

from json import JSONDecodeError


def find_new_data(data_to_save, current_values, file_name):
    if file_name == __saxo_instruments_data_path__:
        response = current_values
        for new_json in data_to_save:
            if len(list(filter(lambda t: t['Identifier'] == new_json['Identifier'], current_values))) == 0:
                response.append(new_json)
        return response
    else:
        return data_to_save


def __save_all__(data_to_save, file_name):
    try:
        with open(file_name, 'r') as outfile:
            import json
            try:
                existing_data = json.load(outfile)
            except JSONDecodeError as e:
                existing_data = []

        with open(file_name, 'w') as outfile:
            new_data = find_new_data(data_to_save, existing_data, file_name)
            json.dump(new_data, outfile, separators=(',', ':'))
        return True
    except Exception as e:
        return False


def __get_all__(type):
    with open(type, 'r') as file:
        r = json.load(file)
    return r


def get_exchanges_data():
    return __get_all__(__exchange_data_path__)


def get_symbols_data():
    return __get_all__(__symbols_data_path__)


def save_symbols(symbols):
    return __save_all__(symbols, __symbols_data_path__)


def save_exchanges(exchanges):
    return __save_all__(exchanges, __exchange_data_path__)


def save_saxo_instruments(instruments):
    return __save_all__(instruments, __saxo_instruments_data_path__)


def get_risk_ratings(tickers):
    return [], tickers
