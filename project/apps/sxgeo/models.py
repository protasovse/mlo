from django.db import models


class Country(models.Model):
    iso = models.CharField(max_length=2, db_index=True)
    continent = models.CharField(max_length=2)
    name_ru = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    lat = models.DecimalField(max_digits=6, decimal_places=2)
    lon = models.DecimalField(max_digits=6, decimal_places=2)
    timezone = models.CharField(max_length=30)


class Regions(models.Model):
    iso = models.CharField(max_length=7)
    country = models.CharField(max_length=2, db_index=True)
    name_ru = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    timezone = models.CharField(max_length=30)
    okato = models.CharField(max_length=4)


class Cities(models.Model):
    region_id = models.IntegerField(db_index=True)
    name_ru = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    lat = models.DecimalField(max_digits=10, decimal_places=5)
    lon = models.DecimalField(max_digits=10, decimal_places=5)
    okato = models.CharField(max_length=20)

    def __str__(self):
        return self.name_ru


