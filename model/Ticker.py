from marshmallow import Schema, fields


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
    change = fields.Tuple(tuple_fields=[fields.Float()])
    change_percent = fields.Tuple(tuple_fields=[fields.Float()])
    ytd_change = fields.Tuple(tuple_fields=[fields.Float()])
    quote = fields.Float()
    quote_timestamp = fields.Str()

    @staticmethod
    def columns():
        return ["name", "symbol", "open", "low", "close", "volume", "high",
                "is_etf", "ask", "bid", "quote", "quote_timestamp", "change", "change_percent"]


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
                 change_percent=None,
                 ytd_change=None,
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
        self.change = change,
        self.change_percent = change_percent,
        self.ytd_change = ytd_change,
        self.quote = quote
        self.quote_timestamp = quote_timestamp

    def __repr__(self):
        return '<Ticker(name={self.name!r})>'.format(self=self)
