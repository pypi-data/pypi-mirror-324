from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class DjBfProtectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drf_bf_protect'
    verbose_name = gettext_lazy("Bruteforce Protection")
