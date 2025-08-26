"""Intent classification and natural language processing"""

from enum import Enum
from typing import Dict, Tuple
import re


class Intent(Enum):
    """Supported intents for license operations"""
    GET_LICENSE = "get_license"
    APPLY_LICENSE = "apply_license"
    UNKNOWN = "unknown"


class IntentClassifier:
    """Simple rule-based intent classifier"""
    
    def __init__(self) -> None:
        # Keywords that suggest license application/update
        self.apply_keywords = {
            'apply', 'update', 'upload', 'install', 'set', 'put', 
            'change', 'replace', 'renew', 'activate'
        }
        
        # Keywords that suggest license retrieval/viewing
        self.get_keywords = {
            'get', 'show', 'check', 'view', 'list', 'display', 
            'status', 'details', 'info', 'information', 'see'
        }
    
    def classify(self, text: str) -> Tuple[Intent, float]:
        """
        Classify user intent from natural language text
        
        Returns:
            Tuple of (Intent, confidence_score)
        """
        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))
        
        apply_matches = len(words.intersection(self.apply_keywords))
        get_matches = len(words.intersection(self.get_keywords))
        
        # Calculate confidence based on keyword matches
        total_matches = apply_matches + get_matches
        
        if total_matches == 0:
            # Default to get if no clear intent
            return Intent.GET_LICENSE, 0.5
        
        if apply_matches > get_matches:
            confidence = min(0.9, 0.6 + (apply_matches * 0.1))
            return Intent.APPLY_LICENSE, confidence
        elif get_matches > apply_matches:
            confidence = min(0.9, 0.6 + (get_matches * 0.1))
            return Intent.GET_LICENSE, confidence
        else:
            # Tie - default to get
            return Intent.GET_LICENSE, 0.5
    
    def extract_instance_hint(self, text: str) -> str:
        """Extract instance ID hints from text"""
        # Look for patterns like "pf-prod-1", "instance pf-dev-2", etc.
        patterns = [
            r'\bpf-\w+-\d+\b',
            r'\binstance\s+(\w+[-\w]*)',
            r'\bnode\s+(\w+[-\w]*)',
            r'\bserver\s+(\w+[-\w]*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                if pattern.startswith(r'\b(pf-'):
                    return match.group(0)
                else:
                    return match.group(1)
        
        return ""


# Global classifier instance
classifier = IntentClassifier()
