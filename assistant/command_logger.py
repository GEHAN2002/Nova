"""Command history logging and error recovery."""
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json

class CommandLogger:
    """Log all commands and enable undo/error recovery."""
    
    def __init__(self, logs_db: str = "data/command_logs.db"):
        self.logs_db = Path(logs_db)
        self.logs_db.parent.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize command logs database."""
        with sqlite3.connect(self.logs_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY,
                    command TEXT,
                    input_text TEXT,
                    response TEXT,
                    status TEXT,
                    error_message TEXT,
                    execution_time_ms REAL,
                    timestamp TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS undoable_commands (
                    id INTEGER PRIMARY KEY,
                    command_id INTEGER,
                    undo_action TEXT,
                    undo_params TEXT,
                    FOREIGN KEY(command_id) REFERENCES command_history(id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS error_suggestions (
                    id INTEGER PRIMARY KEY,
                    command TEXT,
                    error_type TEXT,
                    suggestion TEXT,
                    frequency INTEGER DEFAULT 1
                )
            """)
            conn.commit()
    
    def log_command(self, command: str, input_text: str, response: str, 
                   status: str, error_message: str = None, execution_time_ms: float = 0):
        """Log a command execution."""
        with sqlite3.connect(self.logs_db) as conn:
            cursor = conn.execute(
                """INSERT INTO command_history 
                   (command, input_text, response, status, error_message, execution_time_ms, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (command, input_text, response, status, error_message, execution_time_ms, datetime.now())
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """Get command history."""
        with sqlite3.connect(self.logs_db) as conn:
            cursor = conn.execute(
                """SELECT id, command, input_text, response, status, timestamp
                   FROM command_history ORDER BY timestamp DESC LIMIT ?""",
                (limit,)
            )
            return [{
                "id": row[0],
                "command": row[1],
                "input": row[2],
                "response": row[3],
                "status": row[4],
                "timestamp": row[5]
            } for row in cursor.fetchall()]
    
    def get_failed_commands(self, limit: int = 20) -> List[Dict]:
        """Get failed commands for debugging."""
        with sqlite3.connect(self.logs_db) as conn:
            cursor = conn.execute(
                """SELECT command, input_text, error_message, timestamp
                   FROM command_history WHERE status = 'failed'
                   ORDER BY timestamp DESC LIMIT ?""",
                (limit,)
            )
            return [{
                "command": row[0],
                "input": row[1],
                "error": row[2],
                "timestamp": row[3]
            } for row in cursor.fetchall()]
    
    def register_undoable(self, command_id: int, undo_action: str, undo_params: Dict):
        """Register an undoable command."""
        with sqlite3.connect(self.logs_db) as conn:
            conn.execute(
                """INSERT INTO undoable_commands (command_id, undo_action, undo_params)
                   VALUES (?, ?, ?)""",
                (command_id, undo_action, json.dumps(undo_params))
            )
            conn.commit()
    
    def undo_last_command(self) -> Optional[Dict]:
        """Get last undoable command."""
        with sqlite3.connect(self.logs_db) as conn:
            cursor = conn.execute(
                """SELECT command_id, undo_action, undo_params FROM undoable_commands
                   ORDER BY id DESC LIMIT 1"""
            )
            row = cursor.fetchone()
            if row:
                return {
                    "command_id": row[0],
                    "action": row[1],
                    "params": json.loads(row[2])
                }
            return None
    
    def suggest_correction(self, failed_command: str, error_type: str) -> Optional[str]:
        """Suggest correction for failed command."""
        with sqlite3.connect(self.logs_db) as conn:
            cursor = conn.execute(
                """SELECT suggestion FROM error_suggestions 
                   WHERE command = ? AND error_type = ?
                   ORDER BY frequency DESC LIMIT 1""",
                (failed_command, error_type)
            )
            row = cursor.fetchone()
            return row[0] if row else None
