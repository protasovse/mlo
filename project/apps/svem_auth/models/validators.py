from django.core.exceptions import ValidationError

from apps.sxgeo.models import Cities


class Validator:
    message = ''

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def throw_exception(self):
        raise ValidationError(self.message, code=self.code)


class PasswordValidator(Validator):
    strength_len = 6

    def __init__(self, message=None, code=None, strength_len=None):
        super().__init__(message, code)
        if strength_len is not None:
            self.strength_len = strength_len

    def __call__(self, value):
        if len(value) < self.strength_len:
            self.throw_exception()


class CityIdValidator(Validator):
    def __call__(self, value):
        if not Cities.is_city_id_exists(value):
            self.throw_exception()
