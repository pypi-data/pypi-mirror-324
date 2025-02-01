from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta

from ....types import EventSubscriber, EventSubscriberKey


@dataclass(frozen=True)
class EventSubscriberState:
    group: str
    id: str
    last_seen: datetime

    @property
    def key(self) -> EventSubscriberKey:
        return EventSubscriberKey(self.group, self.id)


class EventSubscriberStateStore(ABC):
    @abstractmethod
    async def add(self, subscriber: EventSubscriber) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def remove(self, subscriber: EventSubscriber) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def list(
        self,
        subscriber_group: str | None = None,
        max_time_since_last_seen: timedelta | None = None,
    ) -> Sequence[EventSubscriberState]:
        raise NotImplementedError()

    @abstractmethod
    async def heartbeat(self, subscriber: EventSubscriber) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def purge(
        self, max_time_since_last_seen: timedelta = timedelta(seconds=360)
    ) -> None:
        raise NotImplementedError()
