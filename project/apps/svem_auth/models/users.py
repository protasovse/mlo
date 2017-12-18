import binascii
import os
from django.db import models
from django.conf import settings
from datetime import date


class UserHash(models.Model):
    key = models.CharField("Key", max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
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


