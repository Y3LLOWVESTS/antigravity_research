"""
Graceful AGMINER stop-state support.

The first signal requests a graceful stop through persistent SQLite state.
Previously committed candidate results therefore remain available.
"""

from __future__ import annotations

import signal
from collections.abc import Callable

from .storage import Storage


class StopController:
    def __init__(self, storage: Storage):
        self.storage = storage
        self._installed = False

    def request_stop(self) -> None:
        self.storage.request_stop()

    def clear(self) -> None:
        self.storage.clear_stop()

    def requested(self) -> bool:
        return self.storage.stop_requested()

    def install_signal_handlers(
        self,
        callback: Callable[[], None] | None = None,
    ) -> None:
        if self._installed:
            return

        def handler(signum: int, frame: object) -> None:
            del signum, frame
            self.storage.request_stop()

            if callback is not None:
                callback()

        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

        self._installed = True
