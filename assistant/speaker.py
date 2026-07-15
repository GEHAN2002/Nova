"""Offline female voice output using the bundled Piper voice."""
from __future__ import annotations
import subprocess
import tempfile
from pathlib import Path
from config import PIPER_PATH, VOICE_MODEL


def speak(text: str) -> None:
    """Say and print a response. Falls back to text if Piper is unavailable."""
    text = str(text).strip()
    if not text:
        return
    print(f"Nova: {text}")
    if not PIPER_PATH.exists() or not VOICE_MODEL.exists():
        return
    output = Path(tempfile.gettempdir()) / "nova_speech.wav"
    try:
        subprocess.run(
            [str(PIPER_PATH), "--model", str(VOICE_MODEL), "--output_file", str(output)],
            input=text, text=True, check=True, capture_output=True,
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"(New-Object Media.SoundPlayer '{output}').PlaySync()"],
            check=False, capture_output=True,
        )
    except (OSError, subprocess.SubprocessError) as error:
        print(f"Voice output unavailable: {error}")
