from django.db import models
from image_cropping import ImageCropField, ImageRatioField

from apps.sxgeo.models import Cities


class CityMeta(models.Model):

    city = models.ForeignKey(Cities, on_delete=models.NOT_PROVIDED)

    lawyers_page_description = models.TextField(
        "Описание для списка юристов из города",
        null=True,
        default=None,
    )

    lawyers_page_cover_orig = ImageCropField(blank=True, upload_to='front/city_meta/%Y/%m/')
    lawyers_page_cover = ImageRatioField('lawyers_page_cover_orig', '1920x500', verbose_name="Обложка")
