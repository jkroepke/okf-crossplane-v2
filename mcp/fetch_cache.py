from __future__ import annotations

import copy
import time
from collections import OrderedDict
from collections.abc import Callable, Hashable
from threading import RLock
from typing import TypeVar, cast

T = TypeVar("T")
IMMUTABLE_SOURCE_TTL_SECONDS = 30 * 24 * 60 * 60


class FetchCache:
    """A bounded, thread-safe TTL cache for successful remote fetches."""

    def __init__(self, ttl_seconds: float = 300.0, max_entries: int = 512) -> None:
        if ttl_seconds < 0:
            raise ValueError("ttl_seconds must be greater than or equal to zero")
        if max_entries < 1:
            raise ValueError("max_entries must be at least one")
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self._entries: OrderedDict[Hashable, tuple[float, object]] = OrderedDict()
        self._lock = RLock()

    def get_or_load(
        self,
        key: Hashable,
        load: Callable[[], T],
        ttl_seconds: float | None = None,
    ) -> T:
        """Return a copy of a cached value or load and cache a fresh value."""
        ttl = self.ttl_seconds if ttl_seconds is None else ttl_seconds
        if ttl < 0:
            raise ValueError("ttl_seconds must be greater than or equal to zero")
        if ttl == 0:
            return load()
        now = time.monotonic()
        with self._lock:
            entry = self._entries.get(key)
            if entry and entry[0] > now:
                self._entries.move_to_end(key)
                return cast(T, copy.deepcopy(entry[1]))
            if entry:
                del self._entries[key]

        value = load()
        with self._lock:
            self._entries[key] = (
                time.monotonic() + ttl,
                copy.deepcopy(value),
            )
            self._entries.move_to_end(key)
            while len(self._entries) > self.max_entries:
                self._entries.popitem(last=False)
        return value
