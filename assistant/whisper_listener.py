"""Microphone recording and local speech-to-text."""
from __future__ import annotations
import tempfile
from pathlib import Path

_model = None


def _get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        print("Loading local speech recognizer (first use can take a moment)...")
        _model = WhisperModel("base.en", device="cpu", compute_type="int8")
    return _model


def listen(seconds: int = 5) -> str:
    try:
        import sounddevice as sd
        import soundfile as sf
        sample_rate = 16000
        print("Listening...")
        audio = sd.rec(seconds * sample_rate, samplerate=sample_rate, channels=1, dtype="float32")
        sd.wait()
        audio_file = Path(tempfile.gettempdir()) / "nova_command.wav"
        sf.write(audio_file, audio, sample_rate)
        segments, _ = _get_model().transcribe(str(audio_file), language="en", beam_size=5)
        return " ".join(segment.text for segment in segments).strip().lower()
    except Exception as error:
        print(f"Microphone unavailable: {error}")
        return ""
