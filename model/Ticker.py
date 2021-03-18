from marshmallow import Schema, fields
import datetime as dt


class TickerSchema(Schema):
    name = fields.Str()
    symbol = fields.Str()
    open = fields.Float()
    low = fields.Float()
    previous_close = fields.Float()
    volume = fields.Integer()
    high = fields.Float()
    is_etf = fields.Boolean()
    ask = fields.Float()
    bid = fields.Float()
    quote = fields.Float()
    quote_timestamp = fields.DateTime()


class Ticker():
    def __init__(self, symbol,
                 name=None,
                 open=None,
                 low=None,
                 previous_close=None,
                 volume=None,
                 high=None,
                 is_etf=None,
                 ask=None,
                 bid=None,
                 quote=None,
                 quote_timestamp=None):
        self.symbol = symbol
        self.name = name
        self.open = open
        self.low = low
        self.previous_close = previous_close
        self.volume = volume
        self.high = high
        self.is_etf = is_etf
        self.ask = ask
        self.bid = bid
        self.quote = quote
        self.quote_timestamp = quote_timestamp

    def __repr__(self):
        return '<Ticker(name={self.name!r})>'.format(self=self)
