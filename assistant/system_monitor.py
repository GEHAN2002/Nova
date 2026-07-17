"""System monitoring and alerts."""
import psutil
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import threading
import time

class SystemMonitor:
    """Monitor system resources and application states."""
    
    def __init__(self, alerts_db: str = "data/system_alerts.db"):
        self.alerts_db = Path(alerts_db)
        self.alerts_db.parent.mkdir(exist_ok=True)
        self._init_db()
        self.thresholds = {
            "cpu_percent": 80,
            "memory_percent": 85,
            "disk_percent": 90
        }
        self.monitoring = False
    
    def _init_db(self):
        """Initialize alerts database."""
        with sqlite3.connect(self.alerts_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY,
                    alert_type TEXT,
                    severity TEXT,
                    message TEXT,
                    timestamp TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS monitored_apps (
                    id INTEGER PRIMARY KEY,
                    app_name TEXT,
                    alert_condition TEXT,
                    is_active INTEGER DEFAULT 1
                )
            """)
            conn.commit()
    
    def get_system_status(self) -> Dict:
        """Get current system resource status."""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(),
            "memory": {
                "percent": psutil.virtual_memory().percent,
                "used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
                "available_gb": round(psutil.virtual_memory().available / (1024**3), 2)
            },
            "disk": {
                "percent": psutil.disk_usage('/').percent,
                "used_gb": round(psutil.disk_usage('/').used / (1024**3), 2),
                "free_gb": round(psutil.disk_usage('/').free / (1024**3), 2)
            },
            "processes": psutil.pids()
        }
    
    def check_thresholds(self) -> List[Dict]:
        """Check if system metrics exceed thresholds."""
        status = self.get_system_status()
        alerts = []
        
        if status["cpu_percent"] > self.thresholds["cpu_percent"]:
            alerts.append({
                "type": "cpu",
                "severity": "warning",
                "message": f"CPU usage high: {status['cpu_percent']}%"
            })
        
        if status["memory"]["percent"] > self.thresholds["memory_percent"]:
            alerts.append({
                "type": "memory",
                "severity": "warning",
                "message": f"Memory usage high: {status['memory']['percent']}%"
            })
        
        if status["disk"]["percent"] > self.thresholds["disk_percent"]:
            alerts.append({
                "type": "disk",
                "severity": "critical",
                "message": f"Disk space low: {status['disk']['percent']}%"
            })
        
        for alert in alerts:
            self._record_alert(alert["type"], alert["severity"], alert["message"])
        
        return alerts
    
    def monitor_app(self, app_name: str, condition: str):
        """Monitor an application for specific conditions.
        
        Args:
            app_name: Name of application to monitor
            condition: Condition to check (e.g., 'idle_30min', 'high_memory')
        """
        with sqlite3.connect(self.alerts_db) as conn:
            conn.execute(
                """INSERT INTO monitored_apps (app_name, alert_condition, is_active)
                   VALUES (?, ?, 1)""",
                (app_name, condition)
            )
            conn.commit()
    
    def get_running_processes(self) -> List[Dict]:
        """Get list of running processes."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu_percent": proc.info['cpu_percent'],
                    "memory_percent": proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return sorted(processes, key=lambda x: x["cpu_percent"], reverse=True)
    
    def _record_alert(self, alert_type: str, severity: str, message: str):
        """Record alert in database."""
        with sqlite3.connect(self.alerts_db) as conn:
            conn.execute(
                """INSERT INTO alerts (alert_type, severity, message, timestamp)
                   VALUES (?, ?, ?, ?)""",
                (alert_type, severity, message, datetime.now())
            )
            conn.commit()
    
    def get_alert_history(self, limit: int = 20) -> List[Dict]:
        """Get recent alerts."""
        with sqlite3.connect(self.alerts_db) as conn:
            cursor = conn.execute(
                """SELECT alert_type, severity, message, timestamp
                   FROM alerts ORDER BY timestamp DESC LIMIT ?""",
                (limit,)
            )
            return [{"type": row[0], "severity": row[1], "message": row[2], "timestamp": row[3]}
                    for row in cursor.fetchall()]
