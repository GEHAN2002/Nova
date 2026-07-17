"""Extensible skill plugin system for custom functionality."""
import importlib.util
import json
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional
import sqlite3
from datetime import datetime

class SkillPluginSystem:
    """Manage and load skill plugins dynamically."""
    
    def __init__(self, plugins_dir: str = "skills/plugins", registry_db: str = "data/plugins_registry.db"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        self.registry_db = Path(registry_db)
        self.registry_db.parent.mkdir(exist_ok=True)
        self._init_db()
        self.loaded_skills = {}
    
    def _init_db(self):
        """Initialize plugin registry database."""
        with sqlite3.connect(self.registry_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS plugins (
                    id INTEGER PRIMARY KEY,
                    plugin_name TEXT UNIQUE,
                    file_path TEXT,
                    version TEXT,
                    description TEXT,
                    author TEXT,
                    enabled INTEGER DEFAULT 1,
                    installed_at TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS plugin_dependencies (
                    id INTEGER PRIMARY KEY,
                    plugin_name TEXT,
                    dependency TEXT,
                    required_version TEXT
                )
            """)
            conn.commit()
    
    def install_plugin(self, plugin_path: str, metadata: Dict) -> bool:
        """Install a new plugin.
        
        Args:
            plugin_path: Path to plugin file
            metadata: Plugin metadata (name, version, description, author, dependencies)
        """
        try:
            plugin_file = Path(plugin_path)
            plugin_name = metadata.get("name", plugin_file.stem)
            dest_path = self.plugins_dir / plugin_file.name
            
            # Copy plugin file
            import shutil
            shutil.copy2(plugin_path, dest_path)
            
            # Register in database
            with sqlite3.connect(self.registry_db) as conn:
                conn.execute(
                    """INSERT INTO plugins (plugin_name, file_path, version, description, author, installed_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (plugin_name, str(dest_path), metadata.get("version", "1.0"),
                     metadata.get("description", ""), metadata.get("author", ""), datetime.now())
                )
                
                # Register dependencies
                for dep in metadata.get("dependencies", []):
                    conn.execute(
                        """INSERT INTO plugin_dependencies (plugin_name, dependency, required_version)
                           VALUES (?, ?, ?)""",
                        (plugin_name, dep["name"], dep.get("version", ""))
                    )
                
                conn.commit()
            
            return True
        except Exception as e:
            print(f"Failed to install plugin: {e}")
            return False
    
    def load_plugin(self, plugin_name: str) -> Optional[Any]:
        """Load a plugin dynamically."""
        if plugin_name in self.loaded_skills:
            return self.loaded_skills[plugin_name]
        
        with sqlite3.connect(self.registry_db) as conn:
            cursor = conn.execute(
                "SELECT file_path, enabled FROM plugins WHERE plugin_name = ?",
                (plugin_name,)
            )
            row = cursor.fetchone()
            if not row or not row[1]:
                return None
        
        try:
            plugin_path = Path(row[0])
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            self.loaded_skills[plugin_name] = module
            return module
        except Exception as e:
            print(f"Failed to load plugin {plugin_name}: {e}")
            return None
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict]:
        """Get plugin metadata."""
        with sqlite3.connect(self.registry_db) as conn:
            cursor = conn.execute(
                "SELECT plugin_name, version, description, author, enabled, installed_at FROM plugins WHERE plugin_name = ?",
                (plugin_name,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "name": row[0],
                    "version": row[1],
                    "description": row[2],
                    "author": row[3],
                    "enabled": bool(row[4]),
                    "installed_at": row[5]
                }
            return None
    
    def list_plugins(self) -> List[Dict]:
        """List all installed plugins."""
        with sqlite3.connect(self.registry_db) as conn:
            cursor = conn.execute(
                "SELECT plugin_name, version, description, enabled FROM plugins ORDER BY plugin_name"
            )
            return [{
                "name": row[0],
                "version": row[1],
                "description": row[2],
                "enabled": bool(row[3])
            } for row in cursor.fetchall()]
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin."""
        with sqlite3.connect(self.registry_db) as conn:
            conn.execute(
                "UPDATE plugins SET enabled = 1 WHERE plugin_name = ?",
                (plugin_name,)
            )
            conn.commit()
        return True
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin."""
        with sqlite3.connect(self.registry_db) as conn:
            conn.execute(
                "UPDATE plugins SET enabled = 0 WHERE plugin_name = ?",
                (plugin_name,)
            )
            conn.commit()
        if plugin_name in self.loaded_skills:
            del self.loaded_skills[plugin_name]
        return True
    
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """Uninstall a plugin."""
        try:
            with sqlite3.connect(self.registry_db) as conn:
                cursor = conn.execute(
                    "SELECT file_path FROM plugins WHERE plugin_name = ?",
                    (plugin_name,)
                )
                row = cursor.fetchone()
                if row:
                    Path(row[0]).unlink(missing_ok=True)
                
                conn.execute("DELETE FROM plugins WHERE plugin_name = ?", (plugin_name,))
                conn.execute("DELETE FROM plugin_dependencies WHERE plugin_name = ?", (plugin_name,))
                conn.commit()
            
            if plugin_name in self.loaded_skills:
                del self.loaded_skills[plugin_name]
            
            return True
        except Exception as e:
            print(f"Failed to uninstall plugin: {e}")
            return False
