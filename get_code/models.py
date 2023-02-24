from django.db import models


class PurchaseType(models.Model):
    amount = models.FloatField(
        verbose_name="Сумма",
        unique=True
    )
    codes_list = models.CharField(
        verbose_name="Список кодов",
        max_length=150
    )

    def __str__(self):
        return f'#{self.amount}'

    class Meta:
        verbose_name = 'Тип Покупки'
        verbose_name_plural = 'Типы Покупок'


class Key(models.Model):
    key = models.TextField(
        verbose_name='Ключ покупки',
        unique=True
    )
    amount = models.FloatField(default=0)

    def __str__(self):
        return f'Ключ - {self.key}'

    class Meta:
        verbose_name = "Ключ"
        verbose_name_plural = 'Ключи'


class SteamCode(models.Model):
    code = models.TextField(
        verbose_name="Код",
        unique=True
    )
    value = models.PositiveIntegerField(
        verbose_name="Сумма",
    )
    status = models.BooleanField(
        verbose_name='Статус',
        default=True,
    )
    key = models.ForeignKey(Key, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'#{self.code}'

    class Meta:
        verbose_name = 'Код пополнения'
        verbose_name_plural = 'Коды пополнения'



class Shop(models.Model):
    name = models.TextField(
        verbose_name='Название магазина',
    )
    guid = models.TextField(
        verbose_name='API Guid',
    )
    seller_id = models.TextField(
        verbose_name='Seller ID'
    )

    def __str__(self):
        return f'Магазин - {self.name}'

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = 'Магазины'
