from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from image_cropping import ImageCropField, ImageRatioField

from config.settings import AUTH_USER_MODEL

SEX_MALE = 'М'
SEX_FEMALE = 'Ж'
SEX = (
    (SEX_MALE, _('Мужской')),
    (SEX_FEMALE, _('Женский')),
)


class Info(models.Model):
    """
    Общая информация
    """

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('Пользователь')
    )

    birth_date = models.DateField(blank=True, null=True,
                                  verbose_name=_('Дата рождения'))

    sex = models.CharField(choices=SEX, max_length=1, null=True, blank=True, verbose_name=_('Пол'))

    orig = ImageCropField(blank=True, verbose_name=_('Оригинал'),
                          upload_to='account/photo/%Y/%m/')
    photo = ImageRatioField('orig', '600x720', verbose_name=_('Фото профиля'))
    pic = ImageRatioField('orig', '300x300', verbose_name=_('Миниатюра'))

    class Meta:
        verbose_name = _('Информация')
        verbose_name_plural = _('Информация')

    def __str__(self):
        return self.user.get_full_name


class AccountBase(models.Model):

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь')
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        abstract = True


class Case(AccountBase):
    """
    Кейсы юриста (успешные дела)
    """
    date = models.DateField(_('Дата'))

    title = models.CharField(_('Заголовок'),
                             blank=True, max_length=255)

    problem = models.TextField(_('Проблема'),
                               help_text=_('Проблема, с которой столкнулся клиент'))

    solution = models.TextField(_('Решение'),
                                help_text=_('Какие действия были предприняты, чтобы решить проблему'))

    result = models.TextField(_('Результат'),
                              help_text=_('Какого результат достигли'))

    profit = models.IntegerField(_('Выгода'), blank=True, null=True,
                                 help_text=_('Материальная выгода клиента'))

    file = models.FileField(_('Файл'), blank=True,
                            upload_to='account/case/%Y/%m/%d')

    class Meta:
        verbose_name = _('Кейс')
        verbose_name_plural = _('Кейсы')

    def __str__(self):
        return 'Кейс: «%s»' % (self.title, )


class Education(AccountBase):
    """
    Образование
    """
    name = models.CharField(_('Название учебного заведения'),
                            max_length=128)

    faculty = models.CharField(_('Факультет'),
                               max_length=64)

    specialty = models.CharField(_('Специальность'),
                                 max_length=64)

    finish = models.PositiveSmallIntegerField(_('Год выпуска'),
                                              blank=True)

    diplom = models.ImageField(_('Копия диплома'),
                               upload_to='account/education/%Y/%m/', blank=True)

    checked = models.BooleanField(_('Подтверждено'), default=False)

    class Meta:
        verbose_name = _('Образование')
        verbose_name_plural = _('Образование')

    def __str__(self):
        return self.name


class Experience(AccountBase):
    """
    Опыт работы
    """
    name = models.CharField(_('Место работы'),
                            max_length=255)

    position = models.CharField(_('Должность'),
                                max_length=128)

    description = models.TextField(_('Описание организации'),
                                   max_length=1024, blank=True)

    site = models.URLField(_('Сайт'),
                           blank=True)

    start = models.PositiveSmallIntegerField(_('Год начала работы'))

    finish = models.PositiveSmallIntegerField(_('Год окончания работы'),
                                              blank=True, null=True)

    doc = models.ImageField(_('Документ подтверждающий трудовую деятельность'),
                            upload_to='account/experience/%Y/%m/', blank=True)

    checked = models.BooleanField(_('Подтверждено'), default=False)

    class Meta:
        verbose_name = _('Опыт работы')
        verbose_name_plural = _('Опыт работы')

    def __str__(self):
        return self.name
