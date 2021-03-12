import os
import sys

from flask import Flask, jsonify, Response, make_response, request, url_for
from flask_cors import CORS
from flask_restful import Resource, Api

import core
import options_logic

print('-----main running----')
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

incomes = [
    {'description': 'salary', 'amount': 5000}
]


@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)

@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return Response('', status=204, headers={"Access-Control-Allow-Headers": "X-PINGOTHER, Content-Type"})


if __name__ == '__main__':
    app.run(threaded=True)
