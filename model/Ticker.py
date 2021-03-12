from marshmallow import Schema, fields

class TickerSchema(Schema):
    name=fields.Str()
    symbol=fields.Str()
    quote=fields.Float()
    date=fields.Date()
