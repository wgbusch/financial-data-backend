import json

__exchange_data_path__ = 'data/reference_data/exchanges_data.json'
__symbols_data_path__ = 'data/reference_data/symbols_data.json'


def __save_all__(data, file_name):
    try:
        with open(file_name, 'w') as outfile:
            import json
            json.dump(data, outfile, separators=(',', ':'))
        return True
    except Exception as e:
        return False


def __get_all__(type):
    with open(type, 'r') as file:
        r = json.load(file)
    return r


def get_exchanges_data():
    return __get_all__(__exchange_data_path__)


# @cache.memoize()
def get_symbols_data():
    return __get_all__(__symbols_data_path__)


def save_symbols(symbols):
    return __save_all__(symbols, __symbols_data_path__)


def save_exchanges(exchanges):
    return __save_all__(exchanges, __exchange_data_path__)
