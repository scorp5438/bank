from django.core.validators import MinValueValidator
from django.db import models


class Wallet(models.Model):
    balance = models.DecimalField(default=0.00, max_digits=100000000000, decimal_places=2, null=False, blank=False,
                                  verbose_name='баланс', validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошелек'

    def __str__(self):
        return f'Балан кошелька с id {self.pk}: {self.balance}'
