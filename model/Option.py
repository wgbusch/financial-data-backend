import math

from marshmallow import Schema, fields


class OptionSchema(Schema):
    contract_symbol = fields.Str(required=True, allow_none=True)
    last_trade_date = fields.Str(required=False, allow_none=True)
    strike = fields.Number(required=True, allow_none=True)
    last_price = fields.Number(required=False, allow_none=True)
    bid = fields.Number(required=False, allow_none=True)
    ask = fields.Number(required=False, allow_none=True)
    change = fields.Number(required=False, allow_none=True)
    percent_change = fields.Number(required=False, allow_none=True)
    volume = fields.Integer(required=False, allow_none=True)
    open_interest = fields.Integer(required=False, allow_none=True)
    implied_volatility = fields.Tuple(tuple_fields=[fields.Number(required=False, allow_none=True)])
    in_the_money = fields.Tuple(tuple_fields=[fields.Number(required=False, allow_none=True)])
    contract_size = fields.Tuple(tuple_fields=[fields.Str(required=False, allow_none=True)])
    currency = fields.Str(required=False, allow_none=True)

    @staticmethod
    def columns():
        return ["contract_symbol", "last_trade_date", "strike", "last_price",
                "bid", "ask", "change", "percent_change", "volume",
                "open_interest", "implied_volatility",
                "in_the_money", "contract_size", "currency"]


class Option:
    def __init__(self,
                 contract_symbol=None,
                 last_trade_date=None,
                 strike=None,
                 last_price=None,
                 bid=None,
                 ask=None,
                 change=None,
                 percent_change=None,
                 volume=None,
                 open_interest=None,
                 implied_volatility=None,
                 in_the_money=None,
                 contract_size=None,
                 currency=None):
        strike = strike if not math.isnan(strike) else None
        bid = bid if not math.isnan(bid) else None
        ask = ask if not math.isnan(ask) else None
        change = change if not math.isnan(change) else None
        percent_change = percent_change if not math.isnan(percent_change) else None
        volume = volume if not math.isnan(volume) else None
        open_interest = open_interest if not math.isnan(open_interest) else None
        implied_volatility = implied_volatility if not math.isnan(implied_volatility) else None

        self.contract_symbol = contract_symbol
        self.last_trade_date = last_trade_date
        self.strike = strike
        self.last_price = last_price
        self.bid = bid
        self.ask = ask
        self.change = change
        self.percent_change = percent_change
        self.volume = volume
        self.open_interest = open_interest
        self.implied_volatility = implied_volatility,
        self.in_the_money = in_the_money,
        self.contract_size = contract_size,
        self.currency = currency

    def __repr__(self):
        return '<Option(contract_symbol={self.contract_symbol!r})>'.format(self=self)
