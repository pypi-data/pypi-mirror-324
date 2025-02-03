from django.db import models
from django.utils.translation import gettext_lazy


class DeviceToken(models.Model):
    name = models.CharField(
        verbose_name=gettext_lazy("Name"),
    )
    token = models.UUIDField(
        verbose_name=gettext_lazy("Token"),
    )
    created = models.DateTimeField(
        verbose_name=gettext_lazy("Created"),
        auto_now_add=True
    )

    class Meta:
        unique_together = ("name", "token")
        verbose_name = gettext_lazy("Device Token")
        verbose_name_plural = gettext_lazy("Device Tokens")


class FailureCount(models.Model):
    name = models.CharField()
    token = models.ForeignKey(DeviceToken, null=True, on_delete=models.CASCADE)
    failures = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "token")


class Lock(models.Model):
    name = models.CharField(primary_key=True)
    timestamp = models.DateTimeField(
        verbose_name=gettext_lazy("Timestamp"),
    )

    class Meta:
        verbose_name = gettext_lazy("Lock")
        verbose_name_plural = gettext_lazy("Locks")


class LockLog(models.Model):
    name = models.CharField(
        verbose_name=gettext_lazy("Name"),
    )
    text = models.CharField()
    created = models.DateTimeField(
        verbose_name=gettext_lazy("Created"),
        auto_now_add=True
    )
