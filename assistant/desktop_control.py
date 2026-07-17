"""Explicit, local desktop automation for Nova."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from config import DATA_DIR


class DesktopControlError(RuntimeError):
    """Raised when desktop automation cannot be completed."""


def _automation():
    try:
        import pyautogui
    except ImportError as error:
        raise DesktopControlError("Desktop control needs PyAutoGUI. Run: python -m pip install pyautogui") from error
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.15
    return pyautogui


def _run(operation: str, callback):
    try:
        return callback()
    except Exception as error:
        raise DesktopControlError(
            f"{operation} failed: {error}. Move the mouse away from a screen corner and try again."
        ) from error


def take_screenshot() -> Path:
    """Capture the current desktop locally and return its saved path."""
    folder = DATA_DIR / "screenshots"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"screenshot-{datetime.now():%Y%m%d-%H%M%S}.png"
    _run("Screenshot", lambda: _automation().screenshot(str(path)))
    return path


def open_notifications() -> None:
    """Open the Windows notification center."""
    _run("Opening notifications", lambda: _automation().hotkey("win", "a"))


def move_mouse(x: int, y: int) -> None:
    gui = _automation()
    width, height = _run("Checking screen size", gui.size)
    if not (0 <= x < width and 0 <= y < height):
        raise DesktopControlError(f"That position is outside your {width} by {height} screen.")
    _run("Moving the mouse", lambda: gui.moveTo(x, y, duration=0.2))


def click(button: str = "left", clicks: int = 1) -> None:
    _run("Clicking", lambda: _automation().click(button=button, clicks=clicks, interval=0.15))


def scroll(amount: int) -> None:
    _run("Scrolling", lambda: _automation().scroll(amount))


def press(keys: str) -> None:
    gui = _automation()
    parts = [key.strip().lower() for key in keys.split("+") if key.strip()]
    if not parts or any(key not in gui.KEYBOARD_KEYS for key in parts):
        raise DesktopControlError("I don't recognize that keyboard key.")
    if len(parts) == 1:
        _run("Pressing a key", lambda: gui.press(parts[0]))
    else:
        _run("Pressing a key combination", lambda: gui.hotkey(*parts))


def write_text(text: str) -> None:
    _run("Typing", lambda: _automation().write(text, interval=0.02))
