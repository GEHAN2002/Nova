"""Full computer scan: index all drives and system folders."""
from __future__ import annotations
from pathlib import Path
import json
import time
from config import DATA_DIR
from system.database_manager import add_file, add_folder


class FullComputerScanner:
    """Scan entire computer including all drives and system folders."""
    
    def __init__(self):
        self.scanned_files = 0
        self.scanned_folders = 0
        self.excluded_dirs = {
            'System Volume Information',
            '$Recycle.Bin',
            'pagefile.sys',
            'hiberfil.sys',
            '.git',
            '__pycache__',
            'node_modules',
            'venv',
            '.venv',
            'AppData',  # Too large and not user-relevant
        }
    
    def get_all_drives(self) -> list[Path]:
        """Get all available drives on Windows."""
        drives = []
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            drive = Path(f"{letter}:")
            if drive.exists():
                drives.append(drive)
        return drives
    
    def should_skip(self, path: Path) -> bool:
        """Check if path should be skipped during scan."""
        try:
            # Skip system files and excluded directories
            for excluded in self.excluded_dirs:
                if excluded.lower() in str(path).lower():
                    return True
            
            # Skip hidden files/folders
            if path.name.startswith('.'):
                return True
            
            return False
        except Exception:
            return True
    
    def scan_drive(self, drive: Path, max_depth: int = 3) -> None:
        """Recursively scan a drive up to max_depth."""
        try:
            if not drive.exists() or self.should_skip(drive):
                return
            
            self._scan_directory(drive, depth=0, max_depth=max_depth)
        except Exception as e:
            print(f"Error scanning drive {drive}: {e}")
    
    def _scan_directory(self, path: Path, depth: int, max_depth: int) -> None:
        """Recursively scan directory with depth limit."""
        try:
            if depth > max_depth or self.should_skip(path):
                return
            
            for item in path.iterdir():
                try:
                    if self.should_skip(item):
                        continue
                    
                    if item.is_dir(follow_symlinks=False):
                        name = item.name.lower()
                        add_folder(name, str(item))
                        self.scanned_folders += 1
                        
                        # Recurse into subdirectories
                        if depth < max_depth:
                            self._scan_directory(item, depth + 1, max_depth)
                    
                    elif item.is_file(follow_symlinks=False):
                        stem = item.stem.lower()
                        add_file(stem, str(item))
                        self.scanned_files += 1
                
                except (PermissionError, OSError):
                    # Skip inaccessible items
                    continue
        
        except (PermissionError, OSError) as e:
            print(f"Error scanning directory {path}: {e}")
    
    def scan_full_computer(self) -> dict:
        """Perform full computer scan across all drives."""
        print("🔍 Starting full computer scan...")
        start_time = time.time()
        
        try:
            drives = self.get_all_drives()
            print(f"Found {len(drives)} drive(s): {[str(d) for d in drives]}")
            
            for drive in drives:
                print(f"Scanning {drive}...")
                self.scan_drive(drive, max_depth=4)
                print(f"  ✓ Found {self.scanned_files} files, {self.scanned_folders} folders")
            
            elapsed = time.time() - start_time
            
            result = {
                "status": "complete",
                "files_indexed": self.scanned_files,
                "folders_indexed": self.scanned_folders,
                "time_seconds": round(elapsed, 2),
                "drives_scanned": len(drives)
            }
            
            print(f"\n✅ Scan complete in {elapsed:.1f}s")
            print(f"   Indexed {self.scanned_files} files in {self.scanned_folders} folders")
            
            return result
        
        except Exception as e:
            print(f"❌ Full scan error: {e}")
            return {"status": "error", "message": str(e)}
    
    def save_scan_metadata(self, metadata: dict) -> None:
        """Save scan metadata to file."""
        try:
            metadata_file = DATA_DIR / "scan_metadata.json"
            metadata['timestamp'] = time.time()
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            print(f"Error saving scan metadata: {e}")


def run_full_computer_scan() -> dict:
    """Execute full computer scan."""
    scanner = FullComputerScanner()
    result = scanner.scan_full_computer()
    scanner.save_scan_metadata(result)
    return result
