"""Wake Nova with local speech recognition; avoids a hard-coded Python path/model."""
from assistant.whisper_listener import listen
from config import WAKE_PHRASES


def wait_for_wake_word() -> bool:
    print("Waiting for 'Nova' (or press Enter to type a command)...")
    while True:
        heard = listen(seconds=3)
        if any(phrase in heard for phrase in WAKE_PHRASES):
            return True
