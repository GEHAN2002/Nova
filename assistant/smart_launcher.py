"""Smart application launcher with fuzzy matching and recent apps."""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from difflib import SequenceMatcher
import subprocess
import sqlite3

class SmartLauncher:
    """Launch applications with fuzzy matching and usage tracking."""
    
    def __init__(self, apps_db: str = "data/app_history.db"):
        self.apps_db = Path(apps_db)
        self.apps_db.parent.mkdir(exist_ok=True)
        self._init_db()
        self.known_apps = self._load_apps()
    
    def _init_db(self):
        """Initialize app history database."""
        with sqlite3.connect(self.apps_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS app_history (
                    id INTEGER PRIMARY KEY,
                    app_name TEXT,
                    app_path TEXT,
                    launched_at TIMESTAMP,
                    launch_count INTEGER DEFAULT 1
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS app_aliases (
                    app_name TEXT PRIMARY KEY,
                    aliases TEXT
                )
            """)
            conn.commit()
    
    def _load_apps(self) -> List[Dict]:
        """Load known applications from system and cache."""
        apps = []
        # Common Windows apps
        common_apps = {
            "Chrome": "chrome",
            "Firefox": "firefox",
            "Edge": "msedge",
            "VS Code": "code",
            "Notepad": "notepad",
            "Calculator": "calc",
            "Word": "winword",
            "Excel": "excel",
            "PowerPoint": "powerpnt",
            "Slack": "slack",
            "Teams": "teams",
            "Discord": "discord",
            "Spotify": "spotify",
            "VLC": "vlc",
            "Git Bash": "bash"
        }
        
        for name, executable in common_apps.items():
            apps.append({"name": name, "executable": executable, "builtin": True})
        
        return apps
    
    def fuzzy_match(self, query: str, threshold: float = 0.6) -> Optional[Dict]:
        """Find app with fuzzy matching.
        
        Args:
            query: App name or partial name
            threshold: Minimum similarity ratio (0-1)
        
        Returns:
            Best matching app or None
        """
        query = query.lower().strip()
        best_match = None
        best_ratio = 0
        
        for app in self.known_apps:
            # Check exact match first
            if app["name"].lower() == query:
                return app
            
            # Fuzzy match
            ratio = SequenceMatcher(None, query, app["name"].lower()).ratio()
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                best_match = app
        
        return best_match
    
    def launch(self, app_name: str) -> bool:
        """Launch application and track usage."""
        app = self.fuzzy_match(app_name)
        if not app:
            return False
        
        try:
            subprocess.Popen([app["executable"]])
            self._record_launch(app["name"], app["executable"])
            return True
        except Exception as e:
            print(f"Failed to launch {app['name']}: {e}")
            return False
    
    def _record_launch(self, app_name: str, app_path: str):
        """Record app launch in history."""
        with sqlite3.connect(self.apps_db) as conn:
            conn.execute(
                """INSERT OR IGNORE INTO app_history (app_name, app_path, launched_at, launch_count)
                   VALUES (?, ?, ?, 1)""",
                (app_name, app_path, datetime.now())
            )
            conn.execute(
                """UPDATE app_history SET launched_at = ?, launch_count = launch_count + 1
                   WHERE app_name = ?""",
                (datetime.now(), app_name)
            )
            conn.commit()
    
    def get_recent_apps(self, limit: int = 5) -> List[Dict]:
        """Get most recently launched apps."""
        with sqlite3.connect(self.apps_db) as conn:
            cursor = conn.execute(
                """SELECT app_name, app_path, launched_at, launch_count
                   FROM app_history ORDER BY launched_at DESC LIMIT ?""",
                (limit,)
            )
            return [{"name": row[0], "path": row[1], "last_used": row[2], "count": row[3]}
                    for row in cursor.fetchall()]
    
    def get_frequently_used(self, limit: int = 5) -> List[Dict]:
        """Get most frequently launched apps."""
        with sqlite3.connect(self.apps_db) as conn:
            cursor = conn.execute(
                """SELECT app_name, app_path, launch_count
                   FROM app_history ORDER BY launch_count DESC LIMIT ?""",
                (limit,)
            )
            return [{"name": row[0], "path": row[1], "count": row[2]}
                    for row in cursor.fetchall()]
    
    def add_alias(self, app_name: str, aliases: List[str]):
        """Add custom aliases for app names."""
        with sqlite3.connect(self.apps_db) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO app_aliases (app_name, aliases) VALUES (?, ?)",
                (app_name, json.dumps(aliases))
            )
            conn.commit()
