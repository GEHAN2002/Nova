# Nova

Nova is a local-first Windows assistant with typed commands, microphone input, offline speech recognition, a bundled female Piper voice, live file indexing, full-screen window control, and an optional phone command bridge.

## Install and start

1. Open PowerShell in this folder.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the requirements and start Nova:

   ```powershell
   pip install -r requirements.txt
   python main.py
   ```

On its first start Nova creates local indexes of Start-menu applications and your Desktop, Documents, Downloads, Pictures, and Videos. It then keeps those folders updated while Nova is running. With auto-scan enabled, Nova also performs a full computer scan on startup to index all drives and system folders.

## Use it

Type a command at the prompt, or press Enter and say **Nova**; Nova then wakes up and asks for your command. Commands include:

```text
nova
open chrome
open Downloads
find resume
list files in Documents
delete file draft.txt
shutdown computer
fullscreen
maximize
minimize
snap left
snap right
full scan
```

Delete and shutdown actions require a separate `confirm`; say `cancel` to stop them. Nova only searches the indexed personal folders for file operations.

## Window Control

Nova includes full-screen and window management commands:

- **fullscreen** — Toggle fullscreen mode
- **maximize** — Maximize current window (Win+Up)
- **minimize** — Minimize current window (Win+Down)
- **snap left** — Snap window to left half (Win+Left)
- **snap right** — Snap window to right half (Win+Right)
- **close window** — Close active window (Alt+F4)

## Full Computer Scan

Nova can perform a comprehensive scan of your entire computer:

- **full scan** or **full computer scan** — Index all drives, folders, and files across the system
- Auto-scan runs on startup if enabled in config
- Scans up to 4 levels deep in directory hierarchies
- Automatically excludes system folders and sensitive directories

## Phone control (same Wi-Fi)

1. Copy `.env.example` to `.env` and put a long random value in `NOVA_MOBILE_TOKEN`.
2. Install the optional server: `python -m pip install Flask`.
3. Run Nova on the computer and find its local IP address with `ipconfig` (for example `192.168.1.25`).
4. From an iOS Shortcut, Android automation app, or companion app, POST JSON to `http://YOUR-PC-IP:8765/command` with header `X-Nova-Token: YOUR_TOKEN` and body `{"command":"open chrome"}`.

The bridge is disabled unless you set the token. Do not port-forward it or expose it to the internet.

## Configuration

Edit `config.py` to customize:

- `WAKE_PHRASES` — Wake word(s) to trigger voice input (default: `("nova",)`)
- `AUTO_SCAN_ON_STARTUP` — Enable full computer scan on startup (default: `True`)
- `USER_FOLDERS` — Personal folders to index
