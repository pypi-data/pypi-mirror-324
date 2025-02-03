import uuid
from datetime import timedelta as TimeDelta
from django.http import JsonResponse
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy
from rest_framework.exceptions import AuthenticationFailed

from . import config


BACKEND = import_string(config.BACKEND)


def _get_token_from_request(request):
    try:
        token = uuid.UUID(
            request.COOKIES.get(config.COOKIENAME, ""),
            version=4
        )
    except ValueError:
        token = None
    return token


def _get_name_value(request, fieldname, case_sensitiv):
    try:
        name = request.data[fieldname]
    except AttributeError:
        name = request.POST[fieldname]
    if not case_sensitiv:
        name = name.lower()
    return name.strip()


def bf_protect(fieldname='username', case_sensitiv=True):
    """Use this decorator on the view that should be protected"""
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            name = _get_name_value(request, fieldname, case_sensitiv)
            token = _get_token_from_request(request)
            backend = BACKEND(name, token)
            if backend.is_locked():
                return JsonResponse(
                    {"detail": gettext_lazy("Too many attempts.")},
                    status=423
                )
            try:
                response = function(request, *args, **kwargs)
            except AuthenticationFailed:
                backend.note_failure()
                raise
            if 200 <= response.status_code < 300:
                backend.reset_failurecount()
                response.set_cookie(
                    config.COOKIENAME,
                    backend.get_token(),
                    max_age=TimeDelta(days=28),
                    secure=True,
                    httponly=True,
                    samesite='Strict'
                )
            elif response.status_code in (401, 403):
                backend.note_failure()
            return response
        return wrapper
    return decorator
