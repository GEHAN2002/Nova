"""Central, local-first settings for Nova."""
from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

ASSISTANT_NAME = "Nova"
WAKE_PHRASES = ("nova",)  # Single wake word: just "nova"
VOICE_MODEL = ROOT / "assets" / "voices" / "en_US-lessac-medium.onnx"
PIPER_PATH = ROOT / "tools" / "piper" / "piper_windows_amd64" / "piper" / "piper.exe"
DATA_DIR = ROOT / "data"
MOBILE_TOKEN = os.getenv("NOVA_MOBILE_TOKEN", "")
MOBILE_PORT = int(os.getenv("NOVA_MOBILE_PORT", "8765"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

USER_FOLDERS = tuple(
    Path.home() / name for name in ("Desktop", "Documents", "Downloads", "Pictures", "Videos")
)

# Auto-scan settings
AUTO_SCAN_ON_STARTUP = True  # Enable automatic full computer scan on startup
FULLSCREEN_MODE = True  # Enable fullscreen control
