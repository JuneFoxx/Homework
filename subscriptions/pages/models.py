from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Subscription(models.Model):
    """Модель подписки пользователя"""

    CURRENCY_CHOICES = [
        ('RUB', '₽ Рубли'),
        ('USD', '$ Доллары США'),
        ('EUR', '€ Евро'),
        ('UAH', '₴ Гривны'),
    ]

    PERIOD_CHOICES = [
        ('monthly',     'Ежемесячно'),
        ('quarterly',   'Раз в 3 месяца'),
        ('semi_annual', 'Раз в полгода'),
        ('annual',      'Ежегодно'),
        ('one_time',    'Разовый платёж'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название подписки',
        help_text='Например: Spotify Premium, Netflix, Яндекс Плюс и т.д.'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Стоимость',
        help_text='Сумма регулярного платежа'
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='RUB',
        verbose_name='Валюта'
    )

    period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        default='monthly',
        verbose_name='Периодичность'
    )

    next_payment_date = models.DateField(
        verbose_name='Дата следующего платежа',
        help_text='Когда ожидается следующее списание'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Отключена подписка или нет'
    )

    service_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Ссылка на сервис',
        help_text='Опционально: сайт или личный кабинет подписки'
    )

    note = models.TextField(
        blank=True,
        verbose_name='Заметка / комментарий',
        help_text='Например: семейный тариф, используется на 2 устройствах и т.д.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['next_payment_date', 'name']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['next_payment_date']),
        ]

    def get_price_display(self):
        symbols = {
            'RUB': '₽',
            'USD': '$',
            'EUR': '€',
            'UAH': '₴',
        }
        return f"{self.price:g} {symbols[self.currency]}"
    
    @property
    def days_until_next_payment(self):
        """Сколько дней осталось до следующего платежа"""
        if not self.next_payment_date:
            return None
        delta = self.next_payment_date - timezone.now().date()
        return delta.days

    def is_soon(self):
        """Скоро ли следующий платёж (например, менее 7 дней)"""
        days = self.days_until_next_payment()
        return days is not None and 0 <= days <= 7
    
class MonthlyExpenseSummary(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(choices=[(i,i) for i in range(1,13)])
    currency = models.CharField(max_length=3, default='RUB')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['year', 'month', 'currency']
        ordering = ['-year', '-month']    