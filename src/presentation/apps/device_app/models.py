from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class DeviceModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название модели")
    description = models.TextField(verbose_name="Описание модели")

    class Meta:
        verbose_name = "Модель устройства"
        verbose_name_plural = "Модели устройств"

    def __str__(self):
        return self.name


class Device(models.Model):
    address = models.CharField(
        max_length=500,
        verbose_name="Адрес",
        help_text="Введите адрес. Автодополнение с использованием сервиса dadata.ru."
    )
    name = models.CharField(max_length=255, verbose_name="Название устройства")
    ip_address = models.GenericIPAddressField(verbose_name="IP-адрес устройства")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="devices",
        verbose_name="Автор"
    )
    device_model = models.ForeignKey(
        DeviceModel,
        on_delete=models.CASCADE,
        related_name="devices",
        verbose_name="Модель устройства"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"

    def __str__(self):
        return f"{self.name} ({self.ip_address})"
