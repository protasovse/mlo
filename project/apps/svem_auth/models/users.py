import binascii
import os
from django.db import models
from django.conf import settings
from datetime import date
from django.core.exceptions import ValidationError




class PasswordValidator:
    message = ''
    strength_len = 6

    def __init__(self, message=None, code=None, strength_len=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if strength_len is not None:
            self.strength_len = strength_len

    def __call__(self, value):
        if len(value) < self.strength_len:
            raise ValidationError(self.message, code=self.code)


class UserHash(models.Model):
    key = models.CharField("Key", max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField("created", auto_now_add=True)
    live_until = models.DateTimeField("created", auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(UserHash, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    @staticmethod
    def get_or_create(user):
        try:
            user_hash = UserHash.objects.get(user=user, live_until__gte=date.today().isoformat())
        except UserHash.DoesNotExist:
            user_hash = UserHash(user=user)
            user_hash.save()
        return user_hash

    def __str__(self):
        return self.key


