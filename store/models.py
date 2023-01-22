from django.db import models


class Posy(models.Model):
    title = models.CharField(
        verbose_name='название букета',
        max_length=50,
        blank=True
    )
    cause = models.CharField(
        verbose_name='повод',
        max_length=100,
        blank=True
    )
    price = models.IntegerField(
        'цена'
    )
    description = models.TextField(
        verbose_name='описание букета',
        blank=True,
    )
    picture = models.CharField(
        verbose_name='изображение букета',
        max_length=30,
        blank=True,
        null=True,
    )
    composition = models.CharField(
        verbose_name='состав',
        max_length=200,
    )

    def __str__(self):
        return self.title


class Florist(models.Model):
    full_name = models.CharField(
        verbose_name="Имя",
        max_length=50
    )
    client_key = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.full_name


class Courier(models.Model):
    full_name = models.CharField(
        verbose_name="Имя",
        max_length=50
    )
    client_key = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.full_name


class Client(models.Model):
    client_id = models.IntegerField(
        verbose_name="Telegram ID",
        null=True
    )
    full_name = models.CharField(
        verbose_name="Имя",
        max_length=50,
        null=True
    )
    phone_number = models.CharField(
        verbose_name="Номер телефон",
        max_length=12,
        null=True
    )
    address = models.TextField(
        verbose_name="Адрес",
        help_text='ул. Пушкина, д.103, кв.56',
        null=True
    )
    delivery_datetime = models.DateTimeField(
        verbose_name="Дата и время доставки",
        null=True
    )
    florist_key = models.ForeignKey(
        "Florist",
        on_delete=models.CASCADE,
        null=True
    )
    courier_key = models.ForeignKey(
        "Courier",
        on_delete=models.CASCADE,
        null=True
    )
    posy = models.ForeignKey(
        to="Posy",
        verbose_name="Букет",
        on_delete=models.PROTECT,
        null=True
    )
