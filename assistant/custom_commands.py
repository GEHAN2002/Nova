"""Custom voice commands and command aliases."""
import json
from pathlib import Path
from typing import Dict, List, Optional, Callable
import sqlite3
from datetime import datetime

class CommandAliasManager:
    """Manage custom command aliases and macros."""
    
    def __init__(self, aliases_file: str = "data/command_aliases.json"):
        self.aliases_file = Path(aliases_file)
        self.aliases_file.parent.mkdir(exist_ok=True)
        self._init_file()
    
    def _init_file(self):
        """Initialize aliases file."""
        if not self.aliases_file.exists():
            self.aliases_file.write_text(json.dumps({
                "aliases": {},
                "macros": {}
            }, indent=2))
    
    def add_alias(self, alias: str, command: str):
        """Add a command alias.
        
        Example: 'coffee' -> 'open spotify && open chrome'
        """
        data = json.loads(self.aliases_file.read_text())
        data["aliases"][alias.lower()] = command
        self.aliases_file.write_text(json.dumps(data, indent=2))
    
    def get_alias(self, alias: str) -> Optional[str]:
        """Get command for alias."""
        data = json.loads(self.aliases_file.read_text())
        return data["aliases"].get(alias.lower())
    
    def remove_alias(self, alias: str):
        """Remove an alias."""
        data = json.loads(self.aliases_file.read_text())
        if alias.lower() in data["aliases"]:
            del data["aliases"][alias.lower()]
            self.aliases_file.write_text(json.dumps(data, indent=2))
    
    def list_aliases(self) -> Dict[str, str]:
        """List all aliases."""
        data = json.loads(self.aliases_file.read_text())
        return data["aliases"]
    
    def create_macro(self, macro_name: str, steps: List[str]):
        """Create a multi-step macro.
        
        Args:
            macro_name: Name of the macro
            steps: List of commands to execute in sequence
        """
        data = json.loads(self.aliases_file.read_text())
        data["macros"][macro_name.lower()] = steps
        self.aliases_file.write_text(json.dumps(data, indent=2))
    
    def get_macro(self, macro_name: str) -> Optional[List[str]]:
        """Get steps for a macro."""
        data = json.loads(self.aliases_file.read_text())
        return data["macros"].get(macro_name.lower())
    
    def list_macros(self) -> Dict[str, List[str]]:
        """List all macros."""
        data = json.loads(self.aliases_file.read_text())
        return data["macros"]
    
    def resolve_command(self, user_input: str) -> str:
        """Resolve aliases and macros in user input."""
        # Check for direct alias
        alias = self.get_alias(user_input)
        if alias:
            return alias
        
        # Check for macro
        macro = self.get_macro(user_input)
        if macro:
            return "\n".join(macro)  # Return as multi-step command
        
        return user_input
