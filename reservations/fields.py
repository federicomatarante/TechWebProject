from django.db import models


class IntegerListField(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'varchar(128)'

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return None
        return [int(number) for number in value.split(',')]

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return ','.join([str(number) for number in value])

    def get_default(self):
        return []