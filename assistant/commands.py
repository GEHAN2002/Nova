"""Predictable local commands. Destructive system changes always need confirmation."""
from __future__ import annotations
import os
import re
import shutil
import subprocess
from pathlib import Path
from system.launcher import open_anything

HELP = "Try: open Chrome, open Downloads, find report, list files in Documents, or stop Nova."


class CommandHandler:
    def __init__(self): self.pending: tuple[str, str] | None = None

    def handle(self, raw: str) -> str | None:
        text = raw.lower().strip()
        if text in {"help", "what can you do"}: return HELP
        if text in {"cancel", "never mind"}: self.pending = None; return "Cancelled."
        if text in {"yes", "confirm"} and self.pending:
            action, target = self.pending; self.pending = None
            if action == "delete":
                try: Path(target).unlink(); return f"Deleted {Path(target).name}."
                except OSError as error: return f"I could not delete it: {error}"
            if action == "shutdown": subprocess.run(["shutdown", "/s", "/t", "0"]); return "Shutting down."
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
