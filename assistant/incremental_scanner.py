"""Incremental file scanning for better performance."""
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
import json
import hashlib

class IncrementalScanner:
    """Scan only changed files instead of full system scan."""
    
    def __init__(self, index_db: str = "data/file_index.db"):
        self.index_db = Path(index_db)
        self.index_db.parent.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize file index database."""
        with sqlite3.connect(self.index_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS file_index (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT UNIQUE,
                    file_hash TEXT,
                    file_size INTEGER,
                    modified_time REAL,
                    indexed_at TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scan_sessions (
                    id INTEGER PRIMARY KEY,
                    scan_type TEXT,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    files_scanned INTEGER,
                    files_added INTEGER,
                    files_modified INTEGER,
                    files_deleted INTEGER
                )
            """)
            conn.commit()
    
    def _get_file_hash(self, file_path: str) -> str:
        """Calculate file hash for change detection."""
        hash_obj = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    def incremental_scan(self, directory: str, max_depth: int = 3) -> Dict:
        """Scan only files that changed since last scan."""
        directory = Path(directory)
        scan_id = None
        
        with sqlite3.connect(self.index_db) as conn:
            cursor = conn.execute(
                "INSERT INTO scan_sessions (scan_type, started_at) VALUES (?, ?)",
                ("incremental", datetime.now())
            )
            scan_id = cursor.lastrowid
        
        files_added = 0
        files_modified = 0
        files_deleted = 0
        files_scanned = 0
        
        # Get all indexed files
        with sqlite3.connect(self.index_db) as conn:
            cursor = conn.execute("SELECT file_path FROM file_index")
            indexed_paths = {row[0] for row in cursor.fetchall()}
        
        # Scan directory
        current_paths = set()
        for file_path in self._walk_directory(directory, max_depth):
            current_paths.add(str(file_path))
            files_scanned += 1
            
            if str(file_path) not in indexed_paths:
                # New file
                self._index_file(file_path)
                files_added += 1
            else:
                # Check if modified
                if self._file_modified(file_path):
                    self._index_file(file_path)
                    files_modified += 1
        
        # Find deleted files
        deleted = indexed_paths - current_paths
        for deleted_path in deleted:
            with sqlite3.connect(self.index_db) as conn:
                conn.execute("DELETE FROM file_index WHERE file_path = ?", (deleted_path,))
                conn.commit()
            files_deleted += 1
        
        # Update scan session
        with sqlite3.connect(self.index_db) as conn:
            conn.execute(
                """UPDATE scan_sessions SET completed_at = ?, files_scanned = ?, 
                   files_added = ?, files_modified = ?, files_deleted = ?
                   WHERE id = ?""",
                (datetime.now(), files_scanned, files_added, files_modified, files_deleted, scan_id)
            )
            conn.commit()
        
        return {
            "status": "complete",
            "scanned": files_scanned,
            "added": files_added,
            "modified": files_modified,
            "deleted": files_deleted
        }
    
    def _walk_directory(self, directory: Path, max_depth: int, current_depth: int = 0) -> List[Path]:
        """Walk directory with depth limit."""
        files = []
        if current_depth >= max_depth:
            return files
        
        for item in directory.iterdir():
            if item.is_file():
                files.append(item)
            elif item.is_dir() and not item.name.startswith('.'):
                files.extend(self._walk_directory(item, max_depth, current_depth + 1))
        
        return files
    
    def _index_file(self, file_path: Path):
        """Index a file."""
        try:
            stat = file_path.stat()
            file_hash = self._get_file_hash(str(file_path))
            
            with sqlite3.connect(self.index_db) as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO file_index 
                       (file_path, file_hash, file_size, modified_time, indexed_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (str(file_path), file_hash, stat.st_size, stat.st_mtime, datetime.now())
                )
                conn.commit()
        except Exception as e:
            print(f"Failed to index {file_path}: {e}")
    
    def _file_modified(self, file_path: Path) -> bool:
        """Check if file was modified since last index."""
        try:
            current_hash = self._get_file_hash(str(file_path))
            
            with sqlite3.connect(self.index_db) as conn:
                cursor = conn.execute(
                    "SELECT file_hash FROM file_index WHERE file_path = ?",
                    (str(file_path),)
                )
                row = cursor.fetchone()
                return not row or row[0] != current_hash
        except Exception:
            return True
