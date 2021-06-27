import getopt
import os
import sys

import numpy as np
import pandas as pd

from apis import yfinance_api_connection
from data.reference_data.Constants import SCRIPTS_PARSING_DATE_FORMAT


def check_if_got_under_sp(strike_price, response):
    asd = response[response < strike_price]
    if len(asd) > 0:
        return 1
    return 0


def check_if_finished_under_sp(strike_price, response):
    response = response[len(response) - 1]
    if response - strike_price < 0:
        return 1
    return 0


def how_much_under_sp_they_got(strike_price, lows, finished_under):
    if (finished_under == 0):
        return 0
    lowest_point = abs(max(-lows))
    percent = lowest_point / strike_price
    return percent - 1


def calculate_profit(bid, strike_price, finishing_price):
    loss = 0
    if (finishing_price < strike_price):
        loss = (strike_price - finishing_price) * 100
    profit = bid * 100 - loss
    return profit


def process_file(filename, start_date, end_date):
    df = pd.read_csv(filename)
    df = df
    tickers = []
    for ticker in df['Include symbols']:
        tickers.append(ticker)

    response = yfinance_api_connection.get_historic_data(tickers, start_date, end_date)
    # saxo = saxo_api_connection.saxo_api_connection(
    #     'eyJhbGciOiJFUzI1NiIsIng1dCI6IjhGQzE5Qjc0MzFCNjNFNTVCNjc0M0QwQTc5MjMzNjZCREZGOEI4NTAifQ.eyJvYWEiOiI3Nzc3NSIsImlzcyI6Im9hIiwiYWlkIjoiMTA5IiwidWlkIjoiSDlmZHRyLU5hV1BjTVhOZTREcmx2QT09IiwiY2lkIjoiSDlmZHRyLU5hV1BjTVhOZTREcmx2QT09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiNzM2YzZkYzJkMGY0NDMyNDgxYTc3N2E0YWE1NDc4YmUiLCJkZ2kiOiI4NCIsImV4cCI6IjE2MjQxMjg5NDMiLCJvYWwiOiIxRiJ9.lYZBTq951Epb3Q_0m3vSMwJNrgha2uJYdYUyfVYGcCGUirKMvE5hBZjyF82KqDsHuXHQN_q3WX80te4it24Phg')
    # # l = saxo.get_trading_conditions_by_uid(8070932, 'Stock')
    # saxo_risk_ratings = saxo.get_risk_rating(tickers)

    df['Ticker got under Strike Price'] = np.nan
    df['Ticker finished under Strike Price'] = np.nan
    df['How much under Strike Price it got'] = np.nan
    df['Finish price'] = np.nan
    df['Profit'] = 0

    bid_column_empty = False
    for index, row in df.iterrows():
        ticker = df.at[index, 'Include symbols']

        strike_price = df[df['Include symbols'] == ticker]['Strike'].iloc[0]
        lows = response.Low[ticker]
        closes = response.Close[ticker]
        finished_under = check_if_finished_under_sp(strike_price, lows)
        finishing_price = closes[len(closes) - 1]

        df.at[index, 'Ticker got under Strike Price'] = check_if_got_under_sp(strike_price, lows)
        df.at[index, 'Ticker finished under Strike Price'] = finished_under
        df.at[index, 'How much under Strike Price it got'] = how_much_under_sp_they_got(strike_price, lows,
                                                                                        finished_under)
        df.at[index, 'Finish price'] = finishing_price

        try:
            if (not bid_column_empty):
                bid = df[df['Include symbols'] == ticker]['Bid'].iloc[0]
                df.at[index, 'Profit'] = calculate_profit(bid, strike_price, finishing_price)
        except Exception as e:
            print(str(e))
            bid_column_empty = True

        # risk_ratings.append(saxo_risk_ratings[ticker])

    result_csv_filename = r'csv_output_startdate_{0}_enddate_{1}.csv'.format(start_date, end_date)
    if not os.path.isfile(result_csv_filename):
        df.to_csv(result_csv_filename, index=False)
    else:
        df.to_csv(result_csv_filename, index=False, mode='w')

    data = [
        [len(list(filter(lambda t: t, df['Ticker got under Strike Price']))) / len(df['Ticker got under Strike Price']),
         len(list(filter(lambda t: t, df['Ticker finished under Strike Price']))) / len(
             df['Ticker finished under Strike Price'])]]

    df_resultados = pd.DataFrame(data,
                                 columns=['% of tickers that got under SP', '% of tickers that finished under SP'])

    resultados_filename = r'resultados_startdate_{0}_enddate_{1}.csv'.format(start_date, end_date)
    if not os.path.isfile(resultados_filename):
        df_resultados.to_csv(resultados_filename, index=False)
    else:
        df_resultados.to_csv(resultados_filename, index=False, mode='a')


def main(argv):
    path = ''
    end_date = '2021-06-12'
    start_date = '2021-06-06'
    help_message = 'test.py -f <path_to_file (startdate_{0}_enddate_{0}.csv)> -s <start date ({0})> -e <end date ({0})>'.format(
        SCRIPTS_PARSING_DATE_FORMAT)
    try:
        opts, args = getopt.getopt(argv, "hf:s:e:", ["filepath=", "startdate=", "enddate="])
    except getopt.GetoptError:
        try:
            opts, args = getopt.getopt(argv, "hf:", ["filepath="])
        except getopt.GetoptError:
            print(help_message)
            sys.exit(2)
    if (len(opts) == 3):
        for opt, arg in opts:
            if opt == '-h':
                print(help_message)
                sys.exit()
            elif opt in ("-f", "--filepath"):
                path = arg
            elif opt in ("-s", "--startdate"):
                start_date = arg
            elif opt in ("-e", "--enddate"):
                end_date = arg
    elif (len(opts) == 1):
        for opt, arg in opts:
            if opt == '-h':
                print(help_message)
                sys.exit()
            elif opt in ("-f", "--filepath"):
                path = arg
                filename = path.split('\\')[len(path.split('\\')) - 1]
                filename = filename.split('.')[0]
                splitted = filename.split('_')
                for i in range(0, len(splitted)):
                    if (splitted[i] == 'startdate'):
                        start_date = splitted[i + 1]
                    elif (splitted[i] == 'enddate'):
                        end_date = splitted[i + 1]

    process_file(path, start_date, end_date)


if __name__ == "__main__":
    main(sys.argv[1:])
