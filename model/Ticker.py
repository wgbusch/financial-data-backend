from marshmallow import Schema, fields
import datetime as dt


class TickerSchema(Schema):
    name = fields.Str()
    symbol = fields.Str()
    quote = fields.Float()
    date = fields.Date()


class Ticker():
    def __init__(self, name, symbol, quote):
        self.name = name
        self.symbol = symbol
        self.date = dt.datetime.now()
        self.quote = quote

    def __repr__(self):
        return '<Ticker(name={self.name!r})>'.format(self=self)
