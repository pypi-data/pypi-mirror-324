from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from .base import Lock, LockManager


class PostgresLockManager(LockManager):
    @asynccontextmanager
    def try_lock(self, lock_name: str) -> AsyncGenerator[Lock, None]:
        raise NotImplementedError()

    @asynccontextmanager
    def wait_for_lock(self, lock_name: str) -> AsyncGenerator[Lock, None]:
        raise NotImplementedError()
