from datetime import date

from marshmallow.fields import Date as BaseDate


class Date(BaseDate):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, date):
            return str(value)
        return super()._deserialize(value, attr, data)
