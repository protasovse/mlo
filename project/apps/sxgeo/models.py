from django.db import models, connection
from django.utils.translation import ugettext_lazy as _


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

    @property
    def name(self):
        return self.name_ru

    @property
    def full_name_ru(self):
        cursor = connection.cursor()
        sql = """
                SELECT c.name_ru, r.name_ru, co.name_ru FROM sxgeo_cities c
                LEFT JOIN sxgeo_regions r ON c.region_id = r.id
                LEFT JOIN sxgeo_country co ON r.country = co.iso
                WHERE c.id = %d
               """ % (self.id,)
        cursor.execute(sql)
        c = cursor.fetchone()
        return "%s (%s, %s)" % (c[0], c[2], c[1])

    def __str__(self):
        return self.full_name_ru

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')


