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
