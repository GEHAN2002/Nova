"""Full-screen control for Nova with keyboard shortcuts and window management."""
from __future__ import annotations
import pyautogui
import time
from pathlib import Path


class FullscreenController:
    """Manage fullscreen mode for Nova and handle full-screen commands."""
    
    def __init__(self):
        self.is_fullscreen = False
        self.original_window = None
    
    def toggle_fullscreen(self) -> bool:
        """Toggle fullscreen mode for Nova."""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self._enter_fullscreen()
            return True
        else:
            self._exit_fullscreen()
            return False
    
    def _enter_fullscreen(self):
        """Enter fullscreen mode."""
        try:
            # Press F11 to toggle fullscreen in most Windows applications
            pyautogui.press('f11')
            time.sleep(0.5)
        except Exception as e:
            print(f"Fullscreen toggle error: {e}")
    
    def _exit_fullscreen(self):
        """Exit fullscreen mode."""
        try:
            # Press F11 again or Escape to exit fullscreen
            pyautogui.press('f11')
            time.sleep(0.5)
        except Exception as e:
            print(f"Exit fullscreen error: {e}")
    
    def maximize_window(self):
        """Maximize the current window."""
        try:
            # Windows + Up arrow maximizes window
            pyautogui.hotkey('win', 'up')
            time.sleep(0.3)
        except Exception as e:
            print(f"Window maximize error: {e}")
    
    def minimize_window(self):
        """Minimize the current window."""
        try:
            # Windows + Down arrow minimizes window
            pyautogui.hotkey('win', 'down')
            time.sleep(0.3)
        except Exception as e:
            print(f"Window minimize error: {e}")
    
    def snap_left(self):
        """Snap window to left half of screen."""
        try:
            # Windows + Left arrow
            pyautogui.hotkey('win', 'left')
            time.sleep(0.3)
        except Exception as e:
            print(f"Snap left error: {e}")
    
    def snap_right(self):
        """Snap window to right half of screen."""
        try:
            # Windows + Right arrow
            pyautogui.hotkey('win', 'right')
            time.sleep(0.3)
        except Exception as e:
            print(f"Snap right error: {e}")
    
    def fullscreen_scan(self) -> str:
        """Display fullscreen scan mode for file indexing."""
        return "Scanning full computer in fullscreen mode. Indexing all drives and folders..."
    
    def close_window(self):
        """Close current window."""
        try:
            # Alt + F4
            pyautogui.hotkey('alt', 'f4')
            time.sleep(0.3)
        except Exception as e:
            print(f"Close window error: {e}")
    
    def switch_window(self):
        """Switch between windows."""
        try:
            # Alt + Tab
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.3)
        except Exception as e:
            print(f"Switch window error: {e}")


# Global fullscreen controller instance
_fullscreen_controller = None


def get_fullscreen_controller() -> FullscreenController:
    """Get or create the fullscreen controller singleton."""
    global _fullscreen_controller
    if _fullscreen_controller is None:
        _fullscreen_controller = FullscreenController()
    return _fullscreen_controller
