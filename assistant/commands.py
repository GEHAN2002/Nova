"""Predictable local commands. Destructive system changes always need confirmation."""
from __future__ import annotations
import os
import re
import shutil
import subprocess
from pathlib import Path
from assistant import desktop_control
from system.launcher import open_anything

HELP = (
    "Try: open Chrome, list files in Documents, take a screenshot, show notifications, "
    "move mouse to 500 300, scroll down, click, press control plus l, or type hello."
)


class CommandHandler:
    def __init__(self): self.pending: tuple[str, str] | None = None

    def handle(self, raw: str) -> str | None:
        raw = raw.strip()
        text = raw.lower().strip()
        if text in {"help", "what can you do"}: return HELP
        if text in {"cancel", "never mind"}: self.pending = None; return "Cancelled."
        if text in {"yes", "confirm"} and self.pending:
            action, target = self.pending; self.pending = None
            if action == "delete":
                try: Path(target).unlink(); return f"Deleted {Path(target).name}."
                except OSError as error: return f"I could not delete it: {error}"
            if action == "shutdown": subprocess.run(["shutdown", "/s", "/t", "0"]); return "Shutting down."
            try:
                if action == "click":
                    button, clicks = target.split(":")
                    desktop_control.click(button, int(clicks))
                    return "Clicked."
                if action == "press":
                    desktop_control.press(target)
                    return "Key pressed."
                if action == "type":
                    desktop_control.write_text(target)
                    return "Typed."
            except desktop_control.DesktopControlError as error:
                return f"Desktop control unavailable: {error}"
        if text in {"take screenshot", "take a screenshot", "capture screen", "capture my screen"}:
            try:
                path = desktop_control.take_screenshot()
                return f"Screenshot saved to {path}."
            except desktop_control.DesktopControlError as error:
                return f"Desktop control unavailable: {error}"
        if text in {"show notifications", "open notifications", "read notifications", "read my notifications"}:
            try:
                desktop_control.open_notifications()
                return "I opened the Windows notification center. I cannot read notification text aloud yet."
            except desktop_control.DesktopControlError as error:
                return f"Desktop control unavailable: {error}"
        move = re.fullmatch(r"move (?:the )?mouse to (\d+)\s*(?:,| )\s*(\d+)", text)
        if move:
            try:
                desktop_control.move_mouse(int(move.group(1)), int(move.group(2)))
                return f"Moved the mouse to {move.group(1)}, {move.group(2)}."
            except desktop_control.DesktopControlError as error:
                return f"Desktop control unavailable: {error}"
        scroll = re.fullmatch(r"scroll (up|down)(?: (\d+))?", text)
        if scroll:
            amount = int(scroll.group(2) or "3")
            try:
                desktop_control.scroll(amount if scroll.group(1) == "up" else -amount)
                return f"Scrolled {scroll.group(1)}."
            except desktop_control.DesktopControlError as error:
                return f"Desktop control unavailable: {error}"
        if text in {"click", "left click", "double click", "right click"}:
            button, clicks = ("right", 1) if text == "right click" else ("left", 2 if text == "double click" else 1)
            self.pending = ("click", f"{button}:{clicks}")
            return "Say confirm to click at the current mouse position, or cancel."
        key_press = re.fullmatch(r"press (.+)", text)
        if key_press:
            keys = key_press.group(1).replace(" plus ", "+")
            self.pending = ("press", keys)
            return f"Say confirm to press {keys}, or cancel."
        typing = re.fullmatch(r"(?:type|write) (.+)", raw, flags=re.IGNORECASE)
        if typing:
            self.pending = ("type", typing.group(1))
            return "Say confirm to type that text at the current cursor, or cancel."
        if text in {"shutdown computer", "turn off computer"}:
            self.pending = ("shutdown", ""); return "Say confirm to shut down the computer, or cancel."
        delete = re.fullmatch(r"delete (?:file )?(.+)", text)
        if delete:
            target = self._find_path(delete.group(1))
            if not target: return "I could not find that file in the indexed folders."
            self.pending = ("delete", str(target)); return f"Say confirm to delete {target.name}, or cancel."
        listing = re.fullmatch(r"(?:list|show) files in (.+)", text)
        if listing:
            folder = self._find_path(listing.group(1), folders_only=True)
            if not folder: return "I could not find that folder."
            names = [item.name for item in folder.iterdir()][:10]
            return "I found: " + (", ".join(names) if names else "no items")
        target = re.sub(r"^(?:open|launch|start|find|show)\s+", "", text)
        if target != text:
            return f"Opening {target}." if open_anything(target) else f"I could not find {target}. Run the scanner once if it is new."
        return None

    @staticmethod
    def _find_path(query: str, folders_only: bool = False) -> Path | None:
        roots = [Path.home() / name for name in ("Desktop", "Documents", "Downloads", "Pictures", "Videos")]
        needle = query.lower().strip()
        for root in roots:
            if not root.exists(): continue
            for path in root.rglob("*"):
                if path.name.lower() == needle or path.stem.lower() == needle:
                    if not folders_only or path.is_dir(): return path
        return None
