import os
import re

from flask import Flask, jsonify, Response
from flask_caching import Cache
from flask_cors import CORS

import logic
from model.Ticker import TickerSchema

print('-----main running----')
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)

PREFIX = '/api/v1'


@app.route(PREFIX + '/tickers/', defaults={'tickers': ''})
@app.route(PREFIX + '/tickers/<tickers>', methods=['GET'])
def get_tickers(tickers):
    if tickers:
        if re.search("^([a-zA-Z0-9.^=]+,)*[a-zA-Z0-9.^=]+$", tickers):
            tickers_list = tickers.split(',')
            if len(tickers_list) > 50:
                return "Too many symbols", 400
        else:
            return "Invalid request", 400
    else:
        tickers_list = []

    tickers_cached = []
    missing_tickers = []
    for ticker_name in tickers_list:
        ticker = cache.get(ticker_name)
        if ticker:
            tickers_cached.append(ticker)
        else:
            missing_tickers.append(ticker_name)

    result = logic.get_tickers(missing_tickers)

    for ticker in result:
        cache.set(ticker["symbol"], ticker, timeout=60)
        tickers_cached.append(ticker)

    return jsonify({"data": tickers_cached,
                    "columns": TickerSchema.columns()})


@app.route(PREFIX + '/incomes', methods=['POST'])
def add_income():
    return Response('', status=204, headers={"Access-Control-Allow-Headers": "X-PINGOTHER, Content-Type"})


@app.route(PREFIX + '/searchTicker/<search_query>', methods=['GET'])
def search(search_query):
    results = logic.search_for_ticker(search_query)
    return jsonify(results)


@app.route(PREFIX + '/save_symbols/', methods=['GET'])
def save_symbols():
    try:
        is_local = os.environ["LOCAL"]
    except:
        return '', 404
    if is_local:
        results = logic.save_symbols()
        return jsonify(results)
    return '', 404



@app.route(PREFIX + '/save_exchanges/', methods=['GET'])
def save_exchanges():
    try:
        is_local = os.environ["LOCAL"]
    except:
        return '', 404
    if is_local:
        results = logic.save_exchanges()
        return jsonify(results)
    return '', 404


if __name__ == '__main__':
    app.run(threaded=True)
