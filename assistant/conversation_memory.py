"""Multi-turn conversation memory with context persistence."""
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import sqlite3

class ConversationMemory:
    """Persistent multi-turn conversation context."""
    
    def __init__(self, db_path: str = "data/conversation_memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
        self.current_session_id = self._create_session()
    
    def _init_db(self):
        """Initialize SQLite database for conversations."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY,
                    session_id TEXT UNIQUE,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY,
                    session_id TEXT,
                    user_input TEXT,
                    assistant_response TEXT,
                    timestamp TIMESTAMP,
                    context_tags TEXT,
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP
                )
            """)
            conn.commit()
    
    def _create_session(self) -> str:
        """Create a new conversation session."""
        session_id = f"session_{datetime.now().isoformat()}"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO sessions (session_id, created_at, updated_at) VALUES (?, ?, ?)",
                (session_id, datetime.now(), datetime.now())
            )
            conn.commit()
        return session_id
    
    def add_exchange(self, user_input: str, assistant_response: str, context_tags: List[str] = None):
        """Store a user-assistant exchange with context tags."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO conversations 
                   (session_id, user_input, assistant_response, timestamp, context_tags)
                   VALUES (?, ?, ?, ?, ?)""",
                (self.current_session_id, user_input, assistant_response, 
                 datetime.now(), json.dumps(context_tags or []))
            )
            conn.commit()
    
    def get_context(self, limit: int = 10) -> List[Dict]:
        """Retrieve conversation context for current session."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT user_input, assistant_response, timestamp, context_tags
                   FROM conversations WHERE session_id = ?
                   ORDER BY timestamp DESC LIMIT ?""",
                (self.current_session_id, limit)
            )
            return [{
                "user": row[0],
                "assistant": row[1],
                "timestamp": row[2],
                "tags": json.loads(row[3] or "[]")
            } for row in cursor.fetchall()]
    
    def get_past_sessions(self, days: int = 7) -> List[Dict]:
        """Get conversation history from past N days."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT DISTINCT session_id, created_at FROM sessions
                   WHERE created_at > datetime('now', ?)
                   ORDER BY created_at DESC""",
                (f"-{days} days",)
            )
            return [{"session_id": row[0], "created_at": row[1]} for row in cursor.fetchall()]
    
    def set_preference(self, key: str, value: str):
        """Store user preference for recall."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
                   VALUES (?, ?, ?)""",
                (key, value, datetime.now())
            )
            conn.commit()
    
    def get_preference(self, key: str) -> Optional[str]:
        """Retrieve stored user preference."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT value FROM user_preferences WHERE key = ?",
                (key,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
    
    def recall_about(self, topic: str) -> List[Dict]:
        """Search conversation history for topic mentions."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT user_input, assistant_response, timestamp FROM conversations
                   WHERE user_input LIKE ? OR assistant_response LIKE ?
                   ORDER BY timestamp DESC LIMIT 5""",
                (f"%{topic}%", f"%{topic}%")
            )
            return [{"user": row[0], "assistant": row[1], "timestamp": row[2]} 
                    for row in cursor.fetchall()]
