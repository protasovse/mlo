from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import F
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

from config.settings import AUTH_USER_MODEL


class Purse(models.Model):

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.NOT_PROVIDED,
        verbose_name=_('Пользователь'),
    )

    balance = models.IntegerField(
        default=0,
        verbose_name=_('Текущий баланс')
    )

    class Meta:
        verbose_name = _('Кошелёк')
        verbose_name_plural = _('Кошельки')

    def make_history(self, amount, comment):
        History.objects.create(user=self.user, value=amount, comment=comment)

    def debit(self, amount, comment):
        if (amount < 0) or (self.balance < amount):
            return False
        self.balance = F('balance') - amount
        self.save(update_fields=['balance'])
        self.make_history(amount, comment)
        return True

    def credit(self, amount, comment):
        if amount < 0:
            return False
        self.balance = F('balance') + amount
        self.save(update_fields=['balance'])
        self.make_history(amount, comment)
        return True

    def transfer(self, amount, to_user, comment):
        with transaction.atomic():
            purse, created = Purse.objects.get_or_create(user=to_user)
            if self.debit(amount, "Transfer to %s: «%s»" % (to_user, comment)):
                purse.credit(amount, "Transfer from %s: «%s»" % (self.user, comment))
                return True
        return False


class History(models.Model):

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.NOT_PROVIDED,
        verbose_name=_('Пользователь'),
    )

    value = models.IntegerField(
        _('Значение')
    )

    date = models.DateTimeField(
        _('Дата перевода'),
        db_index=True, default=timezone.now,
        editable=False
    )

    comment = models.CharField(
        _('Наименование платежа'),
        max_length=256,
    )

    class Meta:
        verbose_name = _('История платежей')
        verbose_name_plural = _('Истории платежей')


# Зачисление/списание средств юристу в кошелёк ±value рублей
def transfer_to_user(user, value, comment):
    purse, created = Purse.objects.get_or_create(user=user)
    purse.balance = F('balance') + value
    purse.save()
    History.objects.create(user=user, value=value, comment=comment)