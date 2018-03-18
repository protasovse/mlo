from django.db import models, connection
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    RUSSIAN_ID = 185
    UKRAINE_ID = 222

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
    is_main_city = models.BooleanField(default=False)

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

    @classmethod
    def _get_cityes_not_uniq_like_as(cls, city, county_ids):
        cursor = connection.cursor()
        sql = """
            select ct.name_ru from sxgeo_cities ct 
            join sxgeo_regions rg on ct.`region_id` = rg.id
            join `sxgeo_country` cntr on cntr.iso = rg.`country` and cntr.id in ({1})
            where ct.name_ru like "{0}%" group by ct.name_ru having count(*)>1 
        """.format(city, ','.join(map(str, county_ids)))
        cursor.execute(sql)
        return [x[0] for x in cursor.fetchall()]

    @classmethod
    def city_like_as(cls, city, county_ids):
        names_not_unic = cls._get_cityes_not_uniq_like_as(city, county_ids)
        cursor = connection.cursor()
        sql = """
            select ct.name_ru, ct.id, rg.name_ru region_name , cntr.`name_ru` country_name 
            from sxgeo_cities ct
            join sxgeo_regions rg on ct.`region_id` = rg.id
            join `sxgeo_country` cntr on cntr.iso = rg.`country` and cntr.id in ({1})
            where ct.name_ru like "{0}%" 
        """.format(city, ','.join(map(str, county_ids)))
        cursor.execute(sql)
        result_raw = cursor.fetchall()
        return [
            {
                'name':
                    obj[0] if obj[0] not in names_not_unic
                    else '{0} ({2}, {1})'.format(obj[0], obj[2], obj[3]),
                'id': obj[1]
            } for obj in result_raw]

    @classmethod
    def get_default(cls, county_ids):
        cursor = connection.cursor()
        sql = """
            select ct.name_ru, ct.id from sxgeo_cities ct 
            join sxgeo_regions rg on ct.`region_id` = rg.id
            join `sxgeo_country` cntr on cntr.iso = rg.`country` and cntr.id in ({})
            where ct.is_main_city = 1 
        """.format(','.join(map(str, county_ids)))
        cursor.execute(sql)
        result_raw = cursor.fetchall()
        return [{'name': obj[0], 'id': obj[1]} for obj in result_raw]

    @classmethod
    def is_city_id_exists(self, id):
        cursor = connection.cursor()
        sql = 'select count(*) cnt from sxgeo_cities where id ={}'.format(id)
        cursor.execute(sql)
        return bool(cursor.fetchall()[0][0])

    def __str__(self):
        return self.full_name_ru

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
