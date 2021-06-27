import argparse
import csv
import datetime as dt
import sys

import pandas as pd

from data.reference_data.Constants import STRFTIME_DATE_FORMAT
from data.reference_data.TradesExecutedFile import SHEET_NAME, ASSET_TYPE, B_S, \
    OPEN_CLOSE, OPTION_EVENT_TYPE, BOOKED_AMOUNT, TRADE_EXECUTION_TIME, UNDERLYING_INSTRUMENT_SYMBOL, AMOUNT

DEFAULT_MODES = ['short_put', 'cc']


class ProfitCalculator:

    def __init__(self, filepath, lang='eng'):
        splitted = filepath.split('\\')
        filename = splitted[len(splitted) - 1]
        if filename.startswith('TradesExecuted'):
            self.sheet_name = SHEET_NAME[lang]
            self.amount = AMOUNT[lang]
            self.b_s = B_S[lang]
            self.open_close = OPEN_CLOSE[lang]
            self.option_event_type = OPTION_EVENT_TYPE[lang]
            self.asset_type = ASSET_TYPE[lang]
            self.booked_amount = BOOKED_AMOUNT[lang]
            self.trade_execution_time = TRADE_EXECUTION_TIME[lang]
            self.underlying_instrument_symbol = UNDERLYING_INSTRUMENT_SYMBOL[lang]
        else:
            sys.exit(2)
        if filename.endswith('csv'):
            self.df = pd.read_csv(filepath, encoding='latin-1')
        elif filename.endswith('xlsx'):
            self.df = pd.read_excel(io=filepath, sheet_name=self.sheet_name)

    def calculate_cc_time_series(self, df, start_date, end_date):
        if start_date is None:
            start_date = min(df[self.trade_execution_time]).strftime(STRFTIME_DATE_FORMAT)
        if end_date is None:
            end_date = dt.datetime.today().strftime(STRFTIME_DATE_FORMAT)
        cc_operations = df[((df[self.b_s] == 'Sold')
                            & (df[self.open_close] == 'Open')
                            & (df[self.option_event_type] == 'Call') |
                            (df[self.b_s] == 'Bought')
                            & (df[self.open_close] == 'Close')
                            & (df[self.option_event_type] == 'Call'))]
        # {"2021-04-05" : {("BB", 200),("PTBR", 100)}, "2021-04-06" :[ etc... ]}
        positions_by_date = self.calculate_positons_by_date(df, start_date, end_date)

        value_for_day = 0
        response = []
        for date in pd.date_range(start=start_date, end=end_date, freq='D'):
            value_for_day += cc_operations[
                df[self.trade_execution_time] == date.strftime(STRFTIME_DATE_FORMAT)][self.booked_amount].sum()

            # Compute the profit coming from the underlying
            df_stocks_sold = df[(df[self.trade_execution_time] == date.strftime(STRFTIME_DATE_FORMAT))
                                & (df[self.asset_type] == 'Stock')
                                & (df[self.amount] < 0)][self.underlying_instrument_symbol]

            tickers_with_ccs = df_stocks_sold
            for ticker in tickers_with_ccs:
                has_active_cc = len((df[self.trade_execution_time] == date.strftime(STRFTIME_DATE_FORMAT))
                                    & (df[self.asset_type] == 'StockOption')
                                    & (df[self.underlying_instrument_symbol] == ticker)) > 0
                if (has_active_cc and positions_by_date[date].get(ticker) and positions_by_date[date][ticker] > 0):
                    profit = 0
                    value_for_day += profit

            response.append((date, value_for_day))

        return response

    def calculate_short_put_time_series(self, df, start_date=None, end_date=None):
        if start_date is None:
            start_date = min(df[self.trade_execution_time]).strftime(STRFTIME_DATE_FORMAT)
        if end_date is None:
            end_date = dt.datetime.today().strftime(STRFTIME_DATE_FORMAT)
        value_for_day = 0
        response = []
        short_put_operations = df[((df[self.b_s] == 'Sold')
                                   & (df[self.open_close] == 'Open')
                                   & (df[self.option_event_type] == 'Put') |
                                   (df[self.b_s] == 'Bought')
                                   & (df[self.open_close] == 'Close')
                                   & (df[self.option_event_type] == 'Put'))]
        for date in pd.date_range(start=start_date, end=end_date, freq='D'):
            value_for_day += short_put_operations[
                df[self.trade_execution_time] == date.strftime(STRFTIME_DATE_FORMAT)][self.booked_amount].sum()
            response.append((date, value_for_day))

        return response

    def process_file(self, modes=None, start_date=None, end_date=None):
        if modes is None:
            modes = DEFAULT_MODES
        df = self.df
        response = {}
        for mode in modes:
            time_series = []
            if mode == 'short_put':
                time_series = self.calculate_short_put_time_series(df, start_date, end_date)

            if mode == 'cc':
                time_series = self.calculate_cc_time_series(df, start_date, end_date)

            with open('results_of_profit_mode_{}.csv'.format(mode), 'w') as out:
                csv_out = csv.writer(out)
                csv_out.writerow(['mode: {} - date'.format(mode), 'mode: {} - profit'.format(mode)])
                for row in time_series:
                    csv_out.writerow(row)

            if (len(time_series) > 0):
                total_profit = time_series[len(time_series) - 1][1]
                print('profit of short puts: {}'.format(total_profit))
                response[mode] = total_profit, time_series

        return response

    def calculate_positons_by_date(self, df, start_date, end_date):
        positions_by_date = {}
        for date in pd.date_range(start=start_date, end=end_date, freq='D'):
            if len(positions_by_date) == 0:
                stocks = {}
            else:
                stocks = positions_by_date[date - dt.timedelta(1)].copy()
            df_comprados = df[(df[self.trade_execution_time] == date.strftime(STRFTIME_DATE_FORMAT))
                              & (df[self.asset_type] == 'Stock')][[self.underlying_instrument_symbol, self.amount]]

            for index, symbol_ammount in df_comprados.iterrows():
                symbol = symbol_ammount[self.underlying_instrument_symbol]
                amount = symbol_ammount[self.amount]
                if stocks.get(symbol) and (amount + stocks.get(symbol) > 0):
                    stocks[symbol] += amount
                elif stocks.get(symbol) and amount + stocks.get(symbol) == 0:
                    stocks.pop(symbol)
                elif not stocks.get(symbol):
                    stocks[symbol] = amount
            positions_by_date[date] = stocks
        return positions_by_date


class CommandLine:
    filepath = ''
    modes = []
    lang = 'eng'

    def __init__(self):
        parser = argparse.ArgumentParser(description="Import historically closed positions file from Saxo bank to "
                                                     "calculate profits")
        parser.add_argument("-H", "--Help", help="Example: help argument", required=False, default="")
        parser.add_argument("-f", "--filepath", help="Example: <path_to_file>", required=True, default="")
        parser.add_argument("-m", "--mode", help="Example: <mode [long_put|short_put|long_call|cc|pmcc]>",
                            required=False, default="")
        parser.add_argument("-l", "--language", help="Example: <language [eng|spa]>]", required=False, default="")

        argument = parser.parse_args()
        status = False

        if argument.Help:
            print("You have used '-h' or '--help' with argument: {0}".format(argument.Help))
            status = True
        if argument.filepath:
            print("You have used '-f' or '--filepath' with argument: {0}".format(argument.filepath))
            self.filepath = argument.filepath
            status = True
        if argument.mode:
            print("You have used '-m' or '--mode' with argument: {0}".format(argument.mode))
            self.modes = argument.mode.split(',')
            status = True
        if argument.language:
            print("You have used '-l' or '--language' with argument: {0}".format(argument.language))
            self.lang = argument.language
            status = True
        if not status:
            print("Maybe you want to use -h or -f or -m or -l as arguments ?")


if __name__ == "__main__":
    app = CommandLine()
    calculator = ProfitCalculator(app.filepath, app.lang)
    calculator.process_file(None)
