"""Accessibility features and customization."""
import json
from pathlib import Path
from typing import Dict, Optional

class AccessibilityManager:
    """Manage accessibility settings and features."""
    
    def __init__(self, settings_file: str = "data/accessibility_settings.json"):
        self.settings_file = Path(settings_file)
        self.settings_file.parent.mkdir(exist_ok=True)
        self._init_settings()
    
    def _init_settings(self):
        """Initialize accessibility settings with defaults."""
        if not self.settings_file.exists():
            defaults = {
                "speech": {
                    "speed": 1.0,  # 0.5 to 2.0
                    "pitch": 1.0,  # 0.5 to 2.0
                    "volume": 1.0,  # 0.0 to 1.0
                    "voice_index": 0  # Available voice model index
                },
                "ui": {
                    "high_contrast": False,
                    "large_text": False,
                    "screen_reader_mode": False
                },
                "input": {
                    "voice_enabled": True,
                    "text_enabled": True,
                    "keyboard_shortcuts_enabled": True,
                    "speech_recognition_timeout": 10  # seconds
                },
                "notifications": {
                    "sound_enabled": True,
                    "visual_alerts": True,
                    "haptic_feedback": False
                }
            }
            self.settings_file.write_text(json.dumps(defaults, indent=2))
    
    def get_settings(self) -> Dict:
        """Get all accessibility settings."""
        return json.loads(self.settings_file.read_text())
    
    def update_speech_settings(self, speed: float = None, pitch: float = None, 
                              volume: float = None, voice_index: int = None):
        """Update speech synthesis settings."""
        settings = self.get_settings()
        if speed is not None:
            settings["speech"]["speed"] = max(0.5, min(2.0, speed))
        if pitch is not None:
            settings["speech"]["pitch"] = max(0.5, min(2.0, pitch))
        if volume is not None:
            settings["speech"]["volume"] = max(0.0, min(1.0, volume))
        if voice_index is not None:
            settings["speech"]["voice_index"] = voice_index
        
        self.settings_file.write_text(json.dumps(settings, indent=2))
    
    def toggle_high_contrast(self):
        """Toggle high contrast mode."""
        settings = self.get_settings()
        settings["ui"]["high_contrast"] = not settings["ui"]["high_contrast"]
        self.settings_file.write_text(json.dumps(settings, indent=2))
    
    def toggle_large_text(self):
        """Toggle large text mode."""
        settings = self.get_settings()
        settings["ui"]["large_text"] = not settings["ui"]["large_text"]
        self.settings_file.write_text(json.dumps(settings, indent=2))
    
    def toggle_screen_reader(self):
        """Toggle screen reader mode."""
        settings = self.get_settings()
        settings["ui"]["screen_reader_mode"] = not settings["ui"]["screen_reader_mode"]
        self.settings_file.write_text(json.dumps(settings, indent=2))
    
    def enable_keyboard_shortcuts(self) -> Dict[str, str]:
        """Get keyboard shortcuts configuration."""
        return {
            "alt+n": "activate nova",
            "alt+s": "take screenshot",
            "alt+m": "show menu",
            "alt+c": "open command palette",
            "alt+h": "show help"
        }
