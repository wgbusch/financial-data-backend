from pprint import pprint

import requests

from connections.db_connection import get_risk_ratings, save_saxo_instruments


def condition_to_find_ticker(instrument, ticker):
    exchange_id = instrument['ExchangeId']
    symbol = instrument['Symbol']
    return symbol.lower() == "{}:xnys".format(ticker).lower() or \
           (symbol.lower() == "{}:xnas".format(ticker).lower())


class saxo_api_connection:
    import json
    import saxo_openapi as __saxo__
    import saxo_openapi.endpoints.rootservices as __rs__
    import saxo_openapi.endpoints.referencedata as __rd__

    def __init__(self, token, account_key="H9fdtr-NaWPcMXNe4DrlvA=="):
        self.__token__ = token
        self.__client__ = self.__saxo__.API(access_token=token)
        self.__accountkey__ = account_key
        r = self.__rs__.diagnostics.Get()
        rv = self.__client__.request(r)
        assert rv is None and r.status_code == 200
        r = self.__rs__.features.Availability()
        rv = self.__client__.request(r)
        print('diagnostics passed')

    def get_instrument_details(self, tickers):
        if (len(tickers) == 1):
            ticker = tickers[0]
        r = self.__rd__.instruments.InstrumentDetails(Uic=99, AssetType='Stock')
        self.__client__.request(r)
        print(self.json.dumps(r.response, indent=4))

    def get_trading_conditions(self, ticker):
        uid, asset_type = self.__find_uid_asset_type__(ticker)
        json_response = self.get_trading_conditions_by_uid(uid, asset_type)
        print(json_response)
        return json_response

    def get_trading_conditions_by_uid(self, uid=4727, asset_type='Stock'):
        r = requests.get(
            r'https://gateway.saxobank.com/sim/openapi/cs/v1/tradingconditions/instrument/{0}/{1}/{2}/'.format(
                self.__accountkey__, uid, asset_type),
            headers={'Authorization': r'Bearer {0}'.format(self.__token__)})

        json_response = self.json.loads(r.text)
        return json_response

    def get_trading_conditions_options(self, option):
        option_root_id = 100
        r = requests.get(
            r'https://gateway.saxobank.com/sim/openapi/cs/v1/tradingconditions/ContractOptionSpaces/{0}/{1}/'.format(
                self.__accountkey__, option_root_id), headers={'Authorization': r'Bearer {0}'.format(self.__token__)})

        json_response = self.json.loads(r.text, indent=4)
        print(json_response)
        return json_response

    def __find_uid_asset_type__(self, ticker):
        return 659, 'Stock'

    def get_risk_rating(self, tickers):
        response = []
        found_tickers, missing_tickers = get_risk_ratings(tickers)

        saxo_instruments_to_save_to_db = []
        for ticker in missing_tickers:
            r = self.__rd__.instruments.Instruments(params={"AssetTypes": "Stock", "Keywords": ticker})
            self.__client__.request(r)
            results = list(
                filter(lambda instrument: condition_to_find_ticker(instrument, ticker), (r.response)['Data']))
            saxo_instruments_to_save_to_db.append(results[0])
            response.append(results[0])
        save_saxo_instruments(saxo_instruments_to_save_to_db)

        uids = {response['Symbol']: response['Identifier'] for i in range(0, len(response), 1)}

        return uids
