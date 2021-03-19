from marshmallow import Schema, fields
import datetime as dt


class TickerSchema(Schema):
    symbol = fields.Str()
    name = fields.Str()
    open = fields.Float()
    low = fields.Float()
    close = fields.Float()
    volume = fields.Integer()
    high = fields.Float()
    is_etf = fields.Boolean()
    ask = fields.Float()
    bid = fields.Float()
    change = fields.Float()
    changePercent = fields.Float()
    ytdChange = fields.Float()
    quote = fields.Float()
    quote_timestamp = fields.Str()


class Ticker:
    def __init__(self, symbol,
                 name=None,
                 open=None,
                 low=None,
                 close=None,
                 volume=None,
                 high=None,
                 is_etf=None,
                 ask=None,
                 bid=None,
                 change=None,
                 changePercent=None,
                 ytdChange=None,
                 quote=None,
                 quote_timestamp=None):
        self.symbol = symbol
        self.name = name
        self.open = open
        self.low = low
        self.close = close
        self.volume = volume
        self.high = high
        self.is_etf = is_etf
        self.ask = ask
        self.bid = bid
        self.quote = quote
        self.quote_timestamp = quote_timestamp

    def __repr__(self):
        return '<Ticker(name={self.name!r})>'.format(self=self)
