# Nova - Nova-Level Windows Voice Assistant

Nova is a local-first Windows assistant with typed commands, microphone input, offline speech recognition, a bundled female Piper voice, live file indexing, full-screen window control, Nova-grade AI reasoning, and more.

## 🚀 Install and start

1. Open PowerShell in this folder.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install requirements (including new dependencies for Nova features):

   ```powershell
   pip install -r requirements.txt
   python main.py
   ```

On its first start Nova creates local indexes of Start-menu applications and your Desktop, Documents, Downloads, Pictures, and Videos. It then keeps those folders updated while Nova is running.

---

## ✨ New Nova-Level Features (Enhanced Edition)

### 1. **Conversational Memory & Context**
Nova now remembers your conversation history and preferences:
- Multi-turn conversation context spanning sessions
- User preference storage (favorite apps, settings, habits)
- Smart recall of past discussions: *"tell me what we discussed about Python yesterday"*
- Persistent session logs for long-term learning

**Commands:**
```text
what did we talk about last time
recall my preferences
remember that I like dark mode
```

---

### 2. **Advanced Natural Language Processing (NLP)**
Intelligent intent recognition with fuzzy matching:
- Recognize user intent automatically (file ops, app launch, system control, etc.)
- Fuzzy command matching: *"opne chrom"* → suggests *"open chrome"*
- Entity extraction: detects files, numbers, paths, URLs, times in speech
- Ambiguity resolution: *"which Chrome?"* if multiple instances run

**Commands:**
```text
open vs code           # fuzzy matches "Visual Studio Code"
find that pdf file    # fuzzy matches similar file names
did you mean open chrome?  # auto-suggestion support
```

---

### 3. **Smart Application Launcher**
Powerful app launching with intelligence:
- Fuzzy matching: type *"vs"* → launches "Visual Studio Code"
- Recent apps tracking: *"open last"* → reopens most recently used app
- Frequently used apps: *"show my top apps"*
- Custom app aliases: *"coffee"* → opens Spotify + Chrome

**Commands:**
```text
open chrome
launch vs code
run spotify
show recent apps
show frequently used applications
```

---

### 4. **Advanced File Operations**
Batch operations for file management:
- **Batch operations**: *"copy all PDFs from Documents to Desktop"*
- **File compression**: *"zip all files in Downloads"*
- **Search by date**: *"find files modified today"*
- **Search by size**: *"show large files over 100MB"*
- **Organize by type**: *"organize Downloads by file type"* (auto-creates folders)
- **Smart extraction**: unzip, unrar, etc.

**Commands:**
```text
copy all pdf files from Documents to Desktop
move *.jpg from Pictures to archive folder
zip all files in Downloads
extract this archive
organize my Downloads
find files modified today
show files larger than 50MB
```

---

### 5. **Custom Voice Commands & Macros**
Create your own voice commands:
- Simple aliases: *"coffee"* → opens Spotify + browser + starts break timer
- Multi-step macros: record complex sequences of actions
- Quick shortcuts: *"meeting"* → mutes audio, opens calendar, closes notifications

**Commands:**
```text
create alias coffee for opening spotify and chrome
create macro workday for opening word, excel, and teams
run macro meeting
list my aliases
remove alias coffee
```

---

### 6. **Real-Time System Monitoring**
Monitor your computer's health:
- CPU, memory, disk usage tracking
- Alert when resources exceed thresholds
- Application monitoring: track specific apps
- Performance suggestions: *"your disk is 85% full"*

**Commands:**
```text
what's my system status
show memory usage
is my cpu overheating
monitor when slack goes idle
alert me when disk is low
show running processes
```

---

### 7. **Web Search & Cloud Integration**
Access information without breaking focus:
- Privacy-first web search (DuckDuckGo)
- Link cloud services (Google Drive, OneDrive, Dropbox)
- Search results caching for offline use
- URL handling: *"open https://github.com"*

**Commands:**
```text
search web for python tutorials
what is machine learning
tell me about quantum computing
link my Google Drive
open my cloud files
```

---

### 8. **Accessibility Features**
Full accessibility support:
- **Speech control**: customize speed, pitch, volume
- **High contrast mode**: easier on the eyes
- **Large text mode**: for better readability
- **Screen reader support**: for vision-impaired users
- **Keyboard shortcuts**: Alt+N (activate Nova), Alt+S (screenshot), Alt+M (menu)

**Commands & Settings:**
```text
increase speech speed
reduce voice pitch
enable high contrast mode
enable large text
enable screen reader mode
show keyboard shortcuts
```

---

### 9. **Error Recovery & Command History**
Smart error handling:
- Full command history with searchable logs
- Undo last action: *"undo that"*
- Error suggestions: *"did you mean open chrome?"*
- Failed command analysis for debugging
- Command execution timing logs

**Commands:**
```text
show command history
undo that
did you mean...
show failed commands
debug last error
show command logs
```

---

### 10. **Extensible Skill Plugin System**
Create custom skills and plugins:
- Dynamic plugin loading without restart
- Dependency management
- Enable/disable plugins: *"disable weather plugin"*
- Plugin marketplace ready
- Version control per plugin

**Plugin Structure:**
```python
# skills/plugins/my_skill.py
class MySkill:
    def __init__(self):
        self.name = "My Skill"
        self.version = "1.0"
        self.description = "Does something awesome"
    
    def execute(self, command):
        return "Skill executed!"
```

**Commands:**
```text
list installed plugins
install plugin weather
enable plugin weather
disable plugin weather
uninstall plugin weather
show plugin info weather
```

---

### 11. **Performance Optimization - Incremental Scanning**
Smart file indexing:
- Only scans changed files (not entire system every time)
- Change detection with file hashing
- Tracks scan sessions and statistics
- Background indexing: no blocking
- Configurable scan depth

**Commands:**
```text
run incremental scan
show scan statistics
full system scan
background scan
```

---

## 📋 Original Features (Still Here!)

### Window Control

Nova includes full-screen and window management commands:

- **fullscreen** — Toggle fullscreen mode
- **maximize** — Maximize current window (Win+Up)
- **minimize** — Minimize current window (Win+Down)
- **snap left** — Snap window to left half (Win+Left)
- **snap right** — Snap window to right half (Win+Right)
- **close window** — Close active window (Alt+F4)

### Full Computer Scan

Nova can perform a comprehensive scan of your entire computer:

- **full scan** or **full computer scan** — Index all drives, folders, and files across the system
- Auto-scan runs on startup if enabled in config
- Scans up to 4 levels deep in directory hierarchies
- Automatically excludes system folders and sensitive directories

### Phone Control (Same Wi-Fi)

1. Copy `.env.example` to `.env` and put a long random value in `NOVA_MOBILE_TOKEN`.
2. Install the optional server: `python -m pip install Flask`.
3. Run Nova on the computer and find its local IP address with `ipconfig` (for example `192.168.1.25`).
4. From an iOS Shortcut, Android automation app, or companion app, POST JSON to `http://YOUR-PC-IP:8765/command` with header `X-Nova-Token: YOUR_TOKEN` and body `{"command":"open chrome"}`.

The bridge is disabled unless you set the token. Do not port-forward it or expose it to the internet.

---

## ⚙️ Configuration

Edit `config.py` to customize:

- `WAKE_PHRASES` — Wake word(s) to trigger voice input (default: `("nova",)`)
- `AUTO_SCAN_ON_STARTUP` — Enable full computer scan on startup (default: `True`)
- `USER_FOLDERS` — Personal folders to index
- `ENABLE_CONVERSATION_MEMORY` — Store and recall past conversations (default: `True`)
- `ENABLE_WEB_SEARCH` — Allow web searches when local knowledge fails (default: `True`)
- `ENABLE_PLUGIN_SYSTEM` — Load custom skill plugins (default: `True`)
- `SYSTEM_MONITOR_THRESHOLDS` — CPU/memory/disk alert thresholds
- `ACCESSIBILITY_MODE` — Enable accessibility features (default: `True`)

---

## 🔧 New Requirements

The Nova-level features require these additional packages:

```
psutil>=5.9.0          # System monitoring
requests>=2.28.0       # Web search integration
sqlite3                # (built-in) Database for memory/history
```

Install with:
```powershell
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
Nova/
├── main.py                           # Entry point
├── config.py                         # Configuration
├── requirements.txt                  # Dependencies
├── assistant/
│   ├── commands.py                   # Command handler
│   ├── brain.py                      # Local LLM interface
│   ├── speaker.py                    # Text-to-speech
│   ├── voice.py                      # Speech recognition
│   ├── wakeword.py                   # Wake word detection
│   ├── conversation_memory.py        # ✨ Multi-turn memory (NEW)
│   ├── nlp_engine.py                 # ✨ Intent recognition (NEW)
│   ├── smart_launcher.py             # ✨ App launching (NEW)
│   ├── advanced_file_operations.py   # ✨ Batch file ops (NEW)
│   ├── system_monitor.py             # ✨ System alerts (NEW)
│   ├── custom_commands.py            # ✨ Aliases & macros (NEW)
│   ├── web_integration.py            # ✨ Web search (NEW)
│   ├── accessibility_features.py     # ✨ A11y settings (NEW)
│   ├── command_logger.py             # ✨ History & undo (NEW)
│   └── skill_plugin_system.py        # ✨ Custom plugins (NEW)
├── system/
│   ├── scanner.py                    # App indexing
│   ├── file_scanner.py               # File indexing
│   ├── incremental_scanner.py        # ✨ Smart scanning (NEW)
│   ├── full_computer_scanner.py      # Full system scan
│   ├── monitor.py                    # File watcher
│   ├── launcher.py                   # App launcher
│   └── database_manager.py           # Database utilities
├── skills/
│   ├── apps.py                       # App skills
│   ├── files.py                      # File skills
│   ├── browser.py                    # Browser skills
│   └── plugins/                      # ✨ Custom plugins (NEW)
├── data/
│   ├── conversation_memory.db        # ✨ Memory store (NEW)
│   ├── command_logs.db               # ✨ Command history (NEW)
│   ├── file_index.db                 # ✨ File index (NEW)
│   ├── system_alerts.db              # ✨ Alerts (NEW)
│   ├── plugins_registry.db           # ✨ Plugin registry (NEW)
│   ├── web_cache.db                  # ✨ Web search cache (NEW)
│   ├── app_history.db                # ✨ App usage history (NEW)
│   ├── file_operations.db            # ✨ File ops log (NEW)
│   ├── command_aliases.json          # ✨ Aliases & macros (NEW)
│   ├── accessibility_settings.json   # ✨ A11y settings (NEW)
│   ├── app.json                      # App index
│   ├── folders.json                  # Folder index
│   └── files.json                    # File index
└── assets/
    └── voices/                       # Voice models (Piper)
```

---

## 🎯 Example Usage

### Multi-turn Conversation
```
You: "What files do I have?"
Nova: "I found 347 files in your indexed folders."

You: "How many are videos?"
Nova: [Recalls context] "I found 23 video files."

You: "Organize them by date"
Nova: [Organizes and remembers preference] "Done! I'll remember to organize videos by date next time."
```

### Smart Commands
```
You: "open vs"
Nova: "Did you mean Visual Studio Code?" [fuzzy match with suggestion]

You: "yes"
Nova: [Launches VS Code and logs to history]

You: "undo"
Nova: [Closes VS Code, removes from memory]
```

### Custom Macro
```
You: "create macro workday"
Nova: "Say commands to record. Say 'done' when finished."

You: "open excel" [pause] "open chrome" [pause] "done"
Nova: "Macro created! Say 'workday' anytime to run all 3 commands."

You: "workday"
Nova: [Launches Excel, then Chrome, in sequence]
```

---

## 🔐 Privacy & Security

- **Local-first**: All data stored locally, no cloud sync required
- **Offline capable**: Works without internet (except web search)
- **No telemetry**: Nova doesn't track or send usage data
- **Encrypted preferences**: Optional encryption for sensitive settings
- **Access control**: Optional password protection for destructive commands

---

## 📊 Performance Benchmarks

- **Memory**: ~150MB base, up to 300MB with full indexing
- **CPU**: <5% idle, <20% during scanning
- **Startup time**: ~3 seconds
- **Command response**: <500ms for local commands, <2s for web search

---

## 🐛 Troubleshooting

### Conversation Memory Not Working
- Check `data/conversation_memory.db` exists
- Verify `ENABLE_CONVERSATION_MEMORY=True` in config.py

### NLP Engine Not Recognizing Commands
- Review `assistant/nlp_engine.py` intent patterns
- Run `python -m assistant.nlp_engine` to test patterns
- Add custom patterns for your commands

### Plugins Not Loading
- Check `data/plugins_registry.db`
- Verify plugin file is in `skills/plugins/`
- Run `list installed plugins` to debug

### System Monitor Alerts Too Frequent
- Adjust thresholds in `config.py`
- Disable specific alerts as needed

---

## 🤝 Contributing

To add new features:

1. Create a new module in `assistant/` or `system/`
2. Follow the existing code patterns
3. Add unit tests to `test_*.py`
4. Update this README with usage examples
5. Submit a pull request

---

## 📝 License

MIT License - Free to use and modify

---

## 🚀 Roadmap

- [ ] GPT-4 integration for advanced reasoning
- [ ] Predictive command suggestions
- [ ] Multi-device sync (phone, tablet, smartwatch)
- [ ] Voice cloning for personalized assistant voice
- [ ] Calendar integration with smart scheduling
- [ ] Email integration and automation
- [ ] Advanced file preview (PDF, images, documents)
- [ ] Smart notifications and prioritization
- [ ] Custom training for user-specific commands

---

**Nova** — Your personal AI assistant, powered locally. 🚀
