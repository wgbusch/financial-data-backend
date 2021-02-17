# import os
# import sys
#
# from flask import Flask, jsonify, Response, make_response, request, url_for
# from flask_cors import CORS
# from flask_restful import Resource, Api
#
# import core
#
# app = Flask(__name__)
# cors = CORS(app, resources={r"*": {"origins": "*"}})
# api = Api(app)
#
#
# @app.route("/api/v1/columns-state/", methods=["POST"])
# def post_columns_state():
#     if request.is_json:
#         try:
#             req = request.get_json()
#         except Exception as e:
#             response = jsonify(data='Bad request')
#             return response, 500
#         mainObj.save_columns_state(req)
#         return "JSON received!", 200
#
#
# class MarketOverview(Resource):
#
#     @app.route("/", methods=["GET"])
#     def get(self):
#         try:
#             view = request.args.get('view')
#             if (not view):
#                 view = 'all'
#             start = request.args.get('start')
#             if (not start):
#                 start = 0
#             else:
#                 start = int(start)
#             end = request.args.get('end')
#             if (not end):
#                 end = None
#             else:
#                 end = int(end)
#             view_name = request.args.get('view_name')
#             if (not view_name):
#                 view_name = 'default'
#             else:
#                 view_name = str(view_name)
#             data = mainObj.get_market_overview(view, start, end, view_name)
#             resp = Response(data, status=200, mimetype='application/json',
#                             headers={"Access-Control-Allow-Headers": "X-PINGOTHER, Content-Type"})
#             return resp
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             response = jsonify(data='Error finding Market Data')
#             return response, 500
#
#     @app.errorhandler(404)
#     def not_found(error):
#         return make_response(jsonify({'error': 'Not found'}), 404)
#
#
# class Option(Resource):
#     def get(self, symbol):
#         if symbol == None or len(symbol) == 0:
#             return "Error: No id field provided. Please specify an id.", 400
#         try:
#             data = {"hola":"123"}
#             resp = Response(data, status=200, mimetype='application/json',
#                             headers={"Access-Control-Allow-Headers": "X-PINGOTHER, Content-Type"})
#             return resp
#
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             response = jsonify(data='Error finding Market Data')
#             return response, 500
#
#
# def has_no_empty_params(rule):
#     defaults = rule.defaults if rule.defaults is not None else ()
#     arguments = rule.arguments if rule.arguments is not None else ()
#     return len(defaults) >= len(arguments)
#
#
# @app.route("/site-map")
# def site_map():
#     links = []
#     for rule in app.url_map.iter_rules():
#         # Filter out rules we can't navigate to in a browser
#         # and rules that require parameters
#         if "GET" in rule.methods and has_no_empty_params(rule):
#             url = url_for(rule.endpoint, **(rule.defaults or {}))
#             links.append((url, rule.endpoint))
#     return links
#     # links is now a list of url, endpoint tuples
#
#
# api.add_resource(MarketOverview, '/api/v1/market-overview/', endpoint='market-overview')
# api.add_resource(Option, '/api/v1/options/option_dates/<string:symbol>/', endpoint='option')
#
# if __name__ == '__main__':
#     mainObj = core.mainObj()
#     app.run()
