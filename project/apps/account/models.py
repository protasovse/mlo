from django.db import models, connection
from django.db.models.signals import post_save, post_delete, pre_save
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import EnumField
from image_cropping import ImageCropField, ImageRatioField

from apps.entry.models import Answer
from apps.sxgeo.models import Cities
from config.settings import AUTH_USER_MODEL

SEX_MALE = 'М'
SEX_FEMALE = 'Ж'
SEX = (
    (SEX_MALE, _('Мужской')),
    (SEX_FEMALE, _('Женский')),
)


class AccountBase(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        verbose_name=_('Пользователь')
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления данных')
    )

    class Meta:
        abstract = True


class RatingTypes(models.Model):
    """
    Типы баллов рейтинга.
    """
    key = models.CharField(
        _('Ключ'),
        max_length=128,
    )

    description = models.TextField(
        _('Описание'),
    )

    value = models.IntegerField(
        _('Балл'),
    )

    class Meta:
        verbose_name = _('Рейтинг: тип баллов')
        verbose_name_plural = _('Рейтинг: типы баллов')

    def __str__(self):
        return '%s (%d)' % (self.description, self.value)


class Rating(models.Model):
    """
    Баллы рейтинга пользователей
    """
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь')
    )

    date = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name=_('Дата'),
    )

    value = models.IntegerField(
        _('Балл'),
        editable=False,
    )

    comment = models.CharField(
        blank=True,
        max_length=128,
    )

    type = models.ForeignKey(RatingTypes, on_delete=models.NOT_PROVIDED)

    class Meta:
        verbose_name = _('Рейтинг: балл')
        verbose_name_plural = _('Рейтинг: баллы')

    def save(self, *args, **kwargs):
        self.value = self.type.value
        return super(Rating, self).save(*args, **kwargs)

    def __str__(self):
        return '%s: %d — %s (%s) — %s' % (self.user, self.value, self.type.key, self.date, self.comment)


class RatingResult(models.Model):
    """
    Рейтинг — суммы баллов
    """
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        primary_key=True
    )

    value = models.IntegerField(
        _('Балл'),
        db_index=True,
    )

    class Meta:
        verbose_name = _('Рейтинг: сумма балов')
        verbose_name_plural = _('Рейтинг: сумма балов')

    def __str__(self):
        return 'Рейтинг %s — %d' % (self.user, self.value)


class Info(models.Model):
    """
    Общая информация
    """
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        verbose_name=_('Пользователь')
    )

    birth_date = models.DateField(blank=True, null=True,
                                  verbose_name=_('Дата рождения'))

    sex = models.CharField(choices=SEX, max_length=1, null=True, blank=True, verbose_name=_('Пол'))

    orig = ImageCropField(blank=True, verbose_name=_('Оригинал'),
                          upload_to='account/photo/%Y/%m/')
    photo = ImageRatioField('orig', '600x720', verbose_name=_('Фото профиля'))

    pic = ImageRatioField('orig', '300x300', verbose_name=_('Миниатюра'))

    status = models.CharField(max_length=140, null=True, blank=True, verbose_name=_('Статус'))

    about = models.TextField(null=True, blank=True, verbose_name=_('О себе'))

    signature = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Подпись под ответами'))

    class Meta:
        verbose_name = _('Профиль юриста')
        verbose_name_plural = _('Профили юристов')

    def __str__(self):
        return self.user.get_full_name


class Contact(AccountBase):
    C_EMAIL = 'Электронный ящик'
    C_PHONE = 'Телефон'
    C_ADDRESS = 'Адрес'
    C_SITE = 'Сайт'
    C_SKYPE = 'Skype'
    C_WHATSAPP = 'WhatsApp'
    C_TELEGRAM = 'Telegram'

    CONTACT_TYPES = [C_EMAIL, C_PHONE, C_ADDRESS, C_SITE, C_SKYPE, C_WHATSAPP, C_TELEGRAM]

    type = EnumField(
        _('Тип'), db_index=True, choices=CONTACT_TYPES)

    value = models.CharField(
        _('Значение'), max_length=128)

    class Meta:
        verbose_name = _('Контакт')
        verbose_name_plural = _('Контакты')

    def __str__(self):
        return self.value


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
        return 'Кейс: «%s»' % (self.title,)


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

    position = models.CharField(_('Должность'), blank=True, null=True, max_length=128)

    description = models.TextField(_('Описание организации'), max_length=1024, blank=True)

    site = models.URLField(_('Сайт'), blank=True)

    start = models.DateField(_('Начало работы'))

    finish = models.DateField(_('Окончание работы'), blank=True, null=True,
                              help_text=_('Если не введено, то по настоящее время'))

    doc = models.ImageField(_('Документ подтверждающий трудовую деятельность'),
                            upload_to='account/experience/%Y/%m/', blank=True)

    checked = models.BooleanField(_('Подтверждено'), default=False)

    class Meta:
        verbose_name = _('Опыт работы')
        verbose_name_plural = _('Опыт работы')

    def __str__(self):
        return self.name


# Добавление или удаление баллов рейтинга. Считаем суммы баллов и кешируем в account_ratingresult
def post_save_rating_receiver(sender, instance, *args, **kwargs):
    cursor = connection.cursor()
    cursor.execute("""
      REPLACE account_ratingresult
        (user_id, value)
        VALUES (%d, IFNULL((SELECT SUM(value) FROM account_rating WHERE user_id = %d), 0))
    """ % (instance.user_id, instance.user_id, ))


post_save.connect(post_save_rating_receiver, sender=Rating)
post_delete.connect(post_save_rating_receiver, sender=Rating)


# Юрист отвечает на вопрос — добавляем балл рейтинга
def expert_add_answer(sender, instance, *args, **kwargs):

    if 'created' in kwargs and kwargs['created']:
        # Если первый ответ
        if instance.is_parent:
            Rating.objects.create(
                type=RatingTypes.objects.get(key='answer'),
                user=instance.author,
                comment='За ответ %d' % (instance.pk,)
            )
        # если дополнительный ответ
        else:
            Rating.objects.create(
                type=RatingTypes.objects.get(key='add_answer'),
                user=instance.author,
                comment='За дополнительный ответ %d' % (instance.pk,)
            )


post_save.connect(expert_add_answer, sender=Answer, dispatch_uid='signal_expert_add_answer')