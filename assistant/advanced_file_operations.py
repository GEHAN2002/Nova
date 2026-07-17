"""Advanced file operations: batch operations, compression, organization."""
import os
import shutil
import zipfile
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import sqlite3

class AdvancedFileOps:
    """Handle complex file operations and organization."""
    
    def __init__(self, history_db: str = "data/file_operations.db"):
        self.history_db = Path(history_db)
        self.history_db.parent.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize file operations history."""
        with sqlite3.connect(self.history_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS file_ops (
                    id INTEGER PRIMARY KEY,
                    operation TEXT,
                    source_path TEXT,
                    target_path TEXT,
                    timestamp TIMESTAMP,
                    status TEXT
                )
            """)
            conn.commit()
    
    def batch_copy(self, pattern: str, source_dir: str, dest_dir: str) -> Dict:
        """Copy all files matching pattern from source to destination.
        
        Args:
            pattern: File pattern (e.g., '*.pdf')
            source_dir: Source directory
            dest_dir: Destination directory
        
        Returns:
            Dict with operation status and count
        """
        source = Path(source_dir)
        dest = Path(dest_dir)
        dest.mkdir(parents=True, exist_ok=True)
        
        copied = 0
        errors = []
        
        try:
            for file in source.glob(pattern):
                try:
                    shutil.copy2(file, dest / file.name)
                    copied += 1
                except Exception as e:
                    errors.append(f"{file.name}: {str(e)}")
            
            result = {"status": "success", "copied": copied, "errors": errors}
            self._record_operation("batch_copy", str(source), str(dest), "success")
            return result
        except Exception as e:
            self._record_operation("batch_copy", str(source), str(dest), "failed")
            return {"status": "failed", "error": str(e)}
    
    def batch_move(self, pattern: str, source_dir: str, dest_dir: str) -> Dict:
        """Move all files matching pattern."""
        source = Path(source_dir)
        dest = Path(dest_dir)
        dest.mkdir(parents=True, exist_ok=True)
        
        moved = 0
        errors = []
        
        try:
            for file in source.glob(pattern):
                try:
                    shutil.move(str(file), str(dest / file.name))
                    moved += 1
                except Exception as e:
                    errors.append(f"{file.name}: {str(e)}")
            
            return {"status": "success", "moved": moved, "errors": errors}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def batch_delete(self, pattern: str, directory: str) -> Dict:
        """Delete all files matching pattern (with confirmation check)."""
        directory = Path(directory)
        deleted = 0
        errors = []
        files_to_delete = list(directory.glob(pattern))
        
        result = {
            "status": "pending_confirmation",
            "count": len(files_to_delete),
            "preview": [f.name for f in files_to_delete[:5]]
        }
        
        return result
    
    def batch_compress(self, pattern: str, source_dir: str, archive_name: str = None) -> Dict:
        """Compress all files matching pattern into a ZIP archive."""
        source = Path(source_dir)
        archive_name = archive_name or f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        archive_path = source / archive_name
        
        try:
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in source.glob(pattern):
                    if file.is_file():
                        zipf.write(file, arcname=file.name)
            
            self._record_operation("batch_compress", str(source), str(archive_path), "success")
            return {"status": "success", "archive": str(archive_path)}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def batch_extract(self, archive_path: str, extract_to: str = None) -> Dict:
        """Extract all files from archive."""
        archive = Path(archive_path)
        extract_to = extract_to or archive.parent
        
        try:
            with zipfile.ZipFile(archive, 'r') as zipf:
                zipf.extractall(extract_to)
            
            self._record_operation("batch_extract", str(archive), extract_to, "success")
            return {"status": "success", "extracted_to": extract_to}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def find_by_date(self, directory: str, days_ago: int = 1) -> List[Dict]:
        """Find files modified in the last N days."""
        from datetime import timedelta
        import time
        
        directory = Path(directory)
        cutoff_time = time.time() - (days_ago * 86400)
        files = []
        
        for file in directory.rglob('*'):
            if file.is_file() and file.stat().st_mtime > cutoff_time:
                files.append({
                    "path": str(file),
                    "size": file.stat().st_size,
                    "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                })
        
        return sorted(files, key=lambda x: x["modified"], reverse=True)
    
    def find_by_size(self, directory: str, min_size_mb: int = 10) -> List[Dict]:
        """Find files larger than specified size."""
        directory = Path(directory)
        min_bytes = min_size_mb * 1024 * 1024
        files = []
        
        for file in directory.rglob('*'):
            if file.is_file() and file.stat().st_size > min_bytes:
                files.append({
                    "path": str(file),
                    "size_mb": round(file.stat().st_size / (1024 * 1024), 2),
                    "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                })
        
        return sorted(files, key=lambda x: x["size_mb"], reverse=True)
    
    def organize_by_type(self, directory: str, create_subdirs: bool = True) -> Dict:
        """Organize files into subdirectories by type."""
        type_map = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov"],
            "Audio": [".mp3", ".wav", ".flac", ".aac"],
            "Archives": [".zip", ".rar", ".7z", ".tar"],
            "Code": [".py", ".js", ".java", ".cpp", ".c"]
        }
        
        directory = Path(directory)
        organized = {}
        
        for file in directory.glob('*'):
            if not file.is_file():
                continue
            
            file_type = "Other"
            for type_name, extensions in type_map.items():
                if file.suffix.lower() in extensions:
                    file_type = type_name
                    break
            
            if create_subdirs:
                type_dir = directory / file_type
                type_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(type_dir / file.name))
            
            if file_type not in organized:
                organized[file_type] = []
            organized[file_type].append(file.name)
        
        return {"status": "success", "organized": organized}
    
    def _record_operation(self, operation: str, source: str, target: str, status: str):
        """Record file operation in history."""
        with sqlite3.connect(self.history_db) as conn:
            conn.execute(
                """INSERT INTO file_ops (operation, source_path, target_path, timestamp, status)
                   VALUES (?, ?, ?, ?, ?)""",
                (operation, source, target, datetime.now(), status)
            )
            conn.commit()
