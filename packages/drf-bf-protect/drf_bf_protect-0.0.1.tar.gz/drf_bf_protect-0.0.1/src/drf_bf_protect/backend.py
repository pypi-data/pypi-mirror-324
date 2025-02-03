import uuid
from abc import ABC, abstractmethod
from datetime import timedelta as TimeDelta

from django.db import transaction
from django.utils import timezone

from . import config
from .models import DeviceToken, FailureCount, Lock, LockLog

class AbstractBackendBase(ABC):

    def __init__(self, name, token):
        self.name = name
        self.token = token
        if not self.has_valid_token():
            self.token = None

    @abstractmethod
    def has_valid_token(self, name, token):
        pass

    @abstractmethod
    def is_locked(self, token):
        pass

    @abstractmethod
    def lock(self, token):
        pass

    @abstractmethod
    def get_token(self):
        pass

    @abstractmethod
    def note_failure(self):
        pass

    @abstractmethod
    def reset_failurecount(self):
        pass


class DatabaseBackend(AbstractBackendBase):

    def __init__(self, name, token):
        self._has_valid_token = None
        self._failure_count = None
        self._token_id = None
        super().__init__(name, token)

    def is_locked(self):
        locked = False
        if Lock.objects.filter(
            name=self.name,
            timestamp__gt=timezone.now() - TimeDelta(minutes=config.LOCK_TIME)
        ).exists():
            if not self.has_valid_token():
                locked = True
        return locked

    def get_token(self):
        if not self.token:
            self.token = uuid.uuid4()
            DeviceToken.objects.update_or_create(
                name=self.name, token=self.token
            )
        return self.token

    def has_valid_token(self):
        if not self.token:
            return False
        if self._has_valid_token is None:
            token = DeviceToken.objects.filter(name=self.name, token=self.token).first()
            if token:
                self._has_valid_token = True
                self._token_id = token.id
        return self._has_valid_token

    def lock(self):
        Lock.objects.update_or_create(name=self.name, defaults={"timestamp": timezone.now()})
        FailureCount.objects.filter(name=self.name, token_id=self._token_id).delete()
        logtext = self.token if self.token else None
        LockLog.objects.create(name=self.name, text=logtext)
        if self.token:
            DeviceToken.objects.filter(token=self.token).delete()

    @transaction.atomic
    def note_failure(self):
        token = self.token if self.token and self.has_valid_token() else None
        failure_count, _ = (
            FailureCount.objects
            .select_for_update()
            .get_or_create(name=self.name, token_id=self._token_id)
        )
        
        if failure_count.updated > timezone.now() - TimeDelta(seconds=config.RESET_FAILURE_COUNT_SECONDS):
            if failure_count.failures < config.FAILURES_BEFORE_LOCK:
                failure_count.failures = failure_count.failures + 1
                failure_count.save()
                self._failure_count = failure_count
            else:
                self.lock()
        else:
            failure_count.failures = 1
            failure_count.save()
            self._failure_count = failure_count

    def reset_failurecount(self):
        FailureCount.objects.filter(name=self.name).delete()
