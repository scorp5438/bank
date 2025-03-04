from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Wallet(models.Model):
    """
    Модель для представления кошелька.

    Атрибуты:
    - balance: Текущий баланс кошелька.
      Тип: DecimalField (максимум 30 цифр, 2 знака после запятой).
      Ограничения:
        - Не может быть пустым (null=False, blank=False).
        - Не может быть отрицательным (MinValueValidator(Decimal('0'))).
      По умолчанию: 0.00.

    Методы:
    - __str__: Возвращает строковое представление кошелька в формате:
      "Баланс кошелька с id <id>: <balance>".
    """
    balance = models.DecimalField(
        default=0.00,
        max_digits=30,
        decimal_places=2,
        null=False,
        blank=False,
        verbose_name='баланс',
        validators=[MinValueValidator(Decimal('0'))]
    )

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошелек'

    def __str__(self):
        return f'Балан кошелька с id {self.pk}: {self.balance}'
