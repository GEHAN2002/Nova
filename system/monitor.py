"""Dependency-free live index updates for Nova's personal folders.

Polling every two seconds is deliberate: it works reliably on local, cloud-synced,
and removable Windows folders without a native watcher package.
"""
from __future__ import annotations
from pathlib import Path
from threading import Event, Thread
import time
from config import USER_FOLDERS
from system.database_manager import add_file, add_folder, remove_file, remove_folder


class FolderMonitor:
    def __init__(self, interval: float = 2.0):
        self.interval, self._stop = interval, Event()
        self._known: dict[str, bool] = {}
        self._thread = Thread(target=self._run, name="nova-file-monitor", daemon=True)

    def start(self):
        self._known = self._snapshot()
        self._thread.start()
        print("Live file monitor started.")
        return self

    def stop(self): self._stop.set()
    def join(self): self._thread.join(timeout=self.interval + 1)

    def _snapshot(self) -> dict[str, bool]:
        current = {}
        for root in USER_FOLDERS:
            if root.exists():
                for item in root.rglob("*"):
                    current[str(item)] = item.is_dir()
        return current

    def _run(self):
        while not self._stop.wait(self.interval):
            now = self._snapshot()
            for path, is_directory in now.items():
                if path not in self._known: self._add(path, is_directory)
            for path, is_directory in self._known.items():
                if path not in now: self._remove(path, is_directory)
            self._known = now

    @staticmethod
    def _add(path: str, is_directory: bool):
        item = Path(path); name = item.name.lower() if is_directory else item.stem.lower()
        (add_folder if is_directory else add_file)(name, path)

    @staticmethod
    def _remove(path: str, is_directory: bool):
        item = Path(path); name = item.name.lower() if is_directory else item.stem.lower()
        (remove_folder if is_directory else remove_file)(name)


def start_monitor() -> FolderMonitor:
    return FolderMonitor().start()
