from django.contrib import admin

from .models import DeviceToken, Lock, LockLog


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ["token", "name", "created"]


@admin.register(Lock)
class LockAdmin(admin.ModelAdmin):
    list_display = ["name", "timestamp"]
    search_fields = ["name"]


@admin.register(LockLog)
class LockAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]
    search_fields = ["name"]
