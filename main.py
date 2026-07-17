"""Nova: local Windows voice and text assistant."""
from __future__ import annotations
from assistant.commands import CommandHandler, HELP
from assistant.speaker import speak
from assistant.voice import listen
from assistant.wakeword import wait_for_wake_word
from assistant.mobile_bridge import start_mobile_bridge
from assistant.fullscreen_control import get_fullscreen_controller
from system.monitor import start_monitor
from config import AUTO_SCAN_ON_STARTUP


def bootstrap_indexes() -> None:
    """Create the first local indexes only when they do not exist yet."""
    from config import DATA_DIR
    if not (DATA_DIR / "app.json").exists():
        try:
            from system.scanner import scan_start_menu
            scan_start_menu()
        except Exception as error:
            print(f"App index skipped: {error}")
    if not (DATA_DIR / "folders.json").exists():
        from system.folder_scanner import scan_folders
        scan_folders()
    if not (DATA_DIR / "files.json").exists():
        from system.file_scanner import scan_files
        scan_files()


def perform_full_scan() -> None:
    """Perform full computer scan on startup if enabled."""
    if AUTO_SCAN_ON_STARTUP:
        speak("Performing full system scan on startup.")
        try:
            from system.full_computer_scanner import run_full_computer_scan
            result = run_full_computer_scan()
            if result.get("status") == "complete":
                speak(f"System scan complete. Indexed {result.get('files_indexed', 0)} files.")
        except Exception as error:
            print(f"Full scan error: {error}")
            speak("System scan encountered an error.")


def main() -> None:
    handler = CommandHandler()
    bootstrap_indexes()
    perform_full_scan()
    monitor = start_monitor()
    fullscreen = get_fullscreen_controller()
    start_mobile_bridge(handler.handle)
    speak("Nova is ready. Say Nova, or type a command.")
    try:
        while True:
            text = input("Nova command (Enter to wait for 'Nova'): ").strip()
            if not text:
                wait_for_wake_word()
                speak("Yes?")
                text = listen()
            if not text: continue
            
            # Handle fullscreen commands
            if text.lower() in {"fullscreen", "full screen"}:
                fullscreen.toggle_fullscreen()
                speak("Fullscreen toggled.")
                continue
            elif text.lower() in {"maximize", "max"}:
                fullscreen.maximize_window()
                speak("Window maximized.")
                continue
            elif text.lower() in {"minimize", "min"}:
                fullscreen.minimize_window()
                speak("Window minimized.")
                continue
            elif text.lower() in {"snap left"}:
                fullscreen.snap_left()
                speak("Window snapped to left.")
                continue
            elif text.lower() in {"snap right"}:
                fullscreen.snap_right()
                speak("Window snapped to right.")
                continue
            elif text.lower() in {"scan full", "full scan", "full computer scan"}:
                speak("Starting full computer scan.")
                from system.full_computer_scanner import run_full_computer_scan
                result = run_full_computer_scan()
                speak(f"Scan complete. Indexed {result.get('files_indexed', 0)} files.")
                continue
            elif text.lower() in {"close window", "close"}:
                fullscreen.close_window()
                speak("Closing window.")
                continue
            
            if text.lower() in {"stop nova", "exit", "quit"}: 
                speak("Goodbye.")
                break
            
            reply = handler.handle(text)
            if reply is None:
                from assistant.brain import ask_nova
                reply = ask_nova(text) or HELP
            speak(reply)
    except KeyboardInterrupt:
        speak("Goodbye.")
    finally:
        monitor.stop(); monitor.join()


if __name__ == "__main__":
    main()
