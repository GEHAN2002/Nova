"""Nova: local Windows voice and text assistant."""
from __future__ import annotations
from assistant.commands import CommandHandler, HELP
from assistant.speaker import speak
from assistant.voice import listen
from assistant.wakeword import wait_for_wake_word
from assistant.mobile_bridge import start_mobile_bridge
from system.monitor import start_monitor


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


def main() -> None:
    handler = CommandHandler()
    bootstrap_indexes()
    monitor = start_monitor()
    start_mobile_bridge(handler.handle)
    speak("Nova is ready. Say Hi Nova, or type a command.")
    try:
        while True:
            text = input("Nova command (Enter to wait for 'Hi Nova'): ").strip()
            if not text:
                wait_for_wake_word()
                speak("Yes?")
                text = listen()
            if not text: continue
            if text.lower() in {"stop nova", "exit", "quit"}: speak("Goodbye."); break
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
