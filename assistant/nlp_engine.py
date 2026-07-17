"""Advanced Natural Language Processing for intent recognition."""
import re
from typing import Tuple, Dict, Optional
from difflib import SequenceMatcher

class IntentRecognizer:
    """Recognize user intent with fuzzy matching and ambiguity resolution."""
    
    # Intent patterns with priority
    INTENTS = {
        "file_operations": {
            "patterns": [
                r"(?:open|show|find|locate)\s+(.+)",
                r"(?:delete|remove)\s+(?:file\s+)?(.+)",
                r"(?:copy|move|rename)\s+(.+)\s+to\s+(.+)",
                r"(?:zip|compress|extract)\s+(.+)"
            ],
            "priority": 1
        },
        "app_launch": {
            "patterns": [
                r"(?:open|launch|start)\s+([\w\s]+)$",
                r"(?:run|execute)\s+([\w\s]+)"
            ],
            "priority": 2
        },
        "system_control": {
            "patterns": [
                r"(?:fullscreen|maximize|minimize|snap)\s*(.+)?",
                r"(?:shutdown|restart|sleep|lock)\s+(?:the\s+)?computer",
                r"(?:take|capture)\s+(?:a\s+)?screenshot"
            ],
            "priority": 3
        },
        "search_web": {
            "patterns": [
                r"(?:search|google|find)\s+(?:on\s+web\s+)?(.+)",
                r"what is (.+)",
                r"tell me about (.+)"
            ],
            "priority": 4
        },
        "scheduling": {
            "patterns": [
                r"(?:remind|remind me)\s+(?:in|to)\s+(.+)",
                r"(?:schedule|set|create)\s+(?:a\s+)?(?:reminder|alarm)\s+(.+)",
                r"(?:at|in)\s+(\d+\s+(?:minutes|hours|days))"
            ],
            "priority": 5
        },
        "query": {
            "patterns": [
                r"(.+)\?$"
            ],
            "priority": 6
        }
    }
    
    def recognize(self, text: str) -> Tuple[str, Dict]:
        """Recognize intent from user input.
        
        Returns:
            Tuple of (intent_type, extracted_data)
        """
        text = text.lower().strip()
        
        # Sort by priority
        sorted_intents = sorted(
            self.INTENTS.items(),
            key=lambda x: x[1]["priority"]
        )
        
        for intent_type, config in sorted_intents:
            for pattern in config["patterns"]:
                match = re.search(pattern, text)
                if match:
                    groups = match.groups()
                    return intent_type, {
                        "raw_input": text,
                        "matched_pattern": pattern,
                        "extracted": groups[0] if groups else None,
                        "groups": groups
                    }
        
        return "unknown", {"raw_input": text}
    
    def resolve_ambiguity(self, options: list, user_input: str) -> Optional[str]:
        """Resolve ambiguous matches using fuzzy matching.
        
        Args:
            options: List of possible matches
            user_input: User's clarifying input
        
        Returns:
            Best matching option or None
        """
        if not options:
            return None
        
        best_match = None
        best_ratio = 0
        
        for option in options:
            ratio = SequenceMatcher(None, user_input.lower(), str(option).lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = option
        
        return best_match if best_ratio > 0.6 else None
    
    def extract_entities(self, text: str) -> Dict:
        """Extract named entities from user input.
        
        Returns:
            Dictionary of entity types to values
        """
        entities = {
            "files": re.findall(r'\b[\w\-]+\.[\w]+\b', text),
            "numbers": re.findall(r'\d+', text),
            "paths": re.findall(r'(?:[A-Z]:\\|~/)[\w\\/:.-]*', text),
            "urls": re.findall(r'https?://[^\s]+', text),
            "times": re.findall(r'\d{1,2}:\d{2}(?:\s*(?:am|pm))?', text, re.IGNORECASE)
        }
        return {k: v for k, v in entities.items() if v}
    
    def suggest_similar_command(self, failed_command: str, known_commands: list) -> Optional[str]:
        """Suggest similar command when one fails."""
        best_match = None
        best_ratio = 0
        
        for cmd in known_commands:
            ratio = SequenceMatcher(None, failed_command.lower(), cmd.lower()).ratio()
            if ratio > best_ratio and ratio > 0.6:
                best_ratio = ratio
                best_match = cmd
        
        return best_match
