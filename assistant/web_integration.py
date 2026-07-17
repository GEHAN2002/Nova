"""Web search and cloud integration."""
import requests
from typing import Dict, List, Optional
import sqlite3
from pathlib import Path
from datetime import datetime

class WebIntegration:
    """Search web and integrate cloud services."""
    
    def __init__(self, cache_db: str = "data/web_cache.db"):
        self.cache_db = Path(cache_db)
        self.cache_db.parent.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize web cache."""
        with sqlite3.connect(self.cache_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS web_cache (
                    id INTEGER PRIMARY KEY,
                    query TEXT,
                    result TEXT,
                    timestamp TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cloud_services (
                    id INTEGER PRIMARY KEY,
                    service_name TEXT,
                    access_token TEXT,
                    refresh_token TEXT,
                    expires_at TIMESTAMP
                )
            """)
            conn.commit()
    
    def search_web(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search the web using DuckDuckGo (privacy-friendly).
        
        Args:
            query: Search query
            num_results: Number of results to return
        
        Returns:
            List of search results with title, snippet, and URL
        """
        # Check cache first
        cached = self._get_cache(query)
        if cached:
            return cached
        
        try:
            # Using DuckDuckGo API (no API key required)
            url = "https://duckduckgo.com/api"
            params = {"q": query, "format": "json", "no_redirect": 1}
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code != 200:
                return [{"error": "Web search unavailable"}]
            
            data = response.json()
            results = []
            
            # Parse results
            for result in data.get("Results", [])[:num_results]:
                results.append({
                    "title": result.get("Text"),
                    "url": result.get("FirstURL"),
                    "snippet": result.get("Result", "")
                })
            
            self._cache_result(query, results)
            return results
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]
    
    def _get_cache(self, query: str) -> Optional[List[Dict]]:
        """Get cached search result."""
        import json
        with sqlite3.connect(self.cache_db) as conn:
            cursor = conn.execute(
                "SELECT result FROM web_cache WHERE query = ? ORDER BY timestamp DESC LIMIT 1",
                (query,)
            )
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None
    
    def _cache_result(self, query: str, results: List[Dict]):
        """Cache search result."""
        import json
        with sqlite3.connect(self.cache_db) as conn:
            conn.execute(
                "INSERT INTO web_cache (query, result, timestamp) VALUES (?, ?, ?)",
                (query, json.dumps(results), datetime.now())
            )
            conn.commit()
    
    def link_cloud_service(self, service_name: str, access_token: str, 
                          refresh_token: str = None, expires_at: str = None):
        """Link a cloud service (Google Drive, OneDrive, etc.)."""
        with sqlite3.connect(self.cache_db) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO cloud_services 
                   (service_name, access_token, refresh_token, expires_at)
                   VALUES (?, ?, ?, ?)""",
                (service_name, access_token, refresh_token, expires_at)
            )
            conn.commit()
    
    def get_cloud_service(self, service_name: str) -> Optional[Dict]:
        """Get cloud service credentials."""
        with sqlite3.connect(self.cache_db) as conn:
            cursor = conn.execute(
                "SELECT access_token, refresh_token, expires_at FROM cloud_services WHERE service_name = ?",
                (service_name,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "access_token": row[0],
                    "refresh_token": row[1],
                    "expires_at": row[2]
                }
            return None
