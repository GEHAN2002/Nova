# Nova

Nova is a local-first Windows assistant with typed commands, microphone input, offline speech recognition, a bundled female Piper voice, live file indexing, and an optional phone command bridge.

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

On its first start Nova creates local indexes of Start-menu applications and your Desktop, Documents, Downloads, Pictures, and Videos. It then keeps those folders updated while Nova is running.

## Use it

Type a command at the prompt, or press Enter and say **Hi Nova** or **Hey Nova**; Nova then asks for your command. Commands include:

```text
open chrome
open Downloads
find resume
list files in Documents
delete file draft.txt
shutdown computer
```

Delete and shutdown actions require a separate `confirm`; say `cancel` to stop them. Nova only searches the five indexed personal folders for file operations.

## Phone control (same Wi-Fi)

1. Copy `.env.example` to `.env` and put a long random value in `NOVA_MOBILE_TOKEN`.
2. Install the optional server: `python -m pip install Flask`.
3. Run Nova on the computer and find its local IP address with `ipconfig` (for example `192.168.1.25`).
4. From an iOS Shortcut, Android automation app, or companion app, POST JSON to `http://YOUR-PC-IP:8765/command` with header `X-Nova-Token: YOUR_TOKEN` and body `{"command":"open chrome"}`.

The bridge is disabled unless you set the token. Do not port-forward it or expose it to the internet.
