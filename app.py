from flask import Flask, jsonify, Response, request
from flask_caching import Cache
from flask_cors import CORS
import re

import logic

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

incomes = [
    {'description': 'salary', 'amount': 5000}
]


@app.route(PREFIX + '/')
# @cache.memoize(timeout=120)
def get_tickers():
    tickers = request.args.get('tickers')
    if tickers:
        if re.search("^([a-zA-Z0-9.^=]+,)*[a-zA-Z0-9.^=]+$", tickers):
            tickers_list = tickers.split(',')
            if len(tickers_list) > 50:
                return "Too many symbols", 400
        else:
            return "Invalid request", 400
    else:
        tickers_list = []
    result = logic.get_tickers(tickers_list)
    return result


@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return Response('', status=204, headers={"Access-Control-Allow-Headers": "X-PINGOTHER, Content-Type"})


if __name__ == '__main__':
    app.run(threaded=True)
