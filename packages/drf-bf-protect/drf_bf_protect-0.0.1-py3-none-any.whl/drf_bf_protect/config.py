from django.conf import settings

try:
    COOKIENAME = settings.BF_PROTECT_SETTINGS["cookie_name"]
except (AttributeError, KeyError):
    COOKIENAME = 'did'

try:
    FAILURES_BEFORE_LOCK = int(settings.BF_PROTECT_SETTINGS["failures_before_lock"])
except (AttributeError, KeyError):
    FAILURES_BEFORE_LOCK = 5

try:
    LOCK_TIME = int(settings.BF_PROTECT_SETTINGS["lock_time_minutes"])
except (AttributeError, KeyError):
    LOCK_TIME = 10

try:
    BACKEND = settings.BF_PROTECT_SETTINGS["backend"]
except (AttributeError, KeyError):
    BACKEND = "drf_bf_protect.backend.DatabaseBackend"

try:
    RESET_FAILURE_COUNT_SECONDS = int(settings.BF_PROTECT_SETTINGS["reset_failure_count_seconds"])
except (AttributeError, KeyError):
    RESET_FAILURE_COUNT_SECONDS = 300
