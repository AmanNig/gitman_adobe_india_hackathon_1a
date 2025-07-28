"""
Language Detection Utilities for Enhanced PDF Outline Extractor
Provides multilingual language detection capabilities
"""

import re
from typing import Optional

# Language detection imports
try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

try:
    import langid
    LANGID_AVAILABLE = True
except ImportError:
    LANGID_AVAILABLE = False

from src.config.language_config import LANGUAGE_PATTERNS


class LanguageDetector:
    """Multilingual language detection utility"""
    
    def __init__(self):
        self.language_patterns = LANGUAGE_PATTERNS
        self.detection_methods = {
            'regex': True,
            'langdetect': LANGDETECT_AVAILABLE,
            'langid': LANGID_AVAILABLE
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of the text using multiple methods
        
        Args:
            text (str): Text to detect language for
            
        Returns:
            str: Language code (e.g., 'en', 'hi', 'te')
        """
        if not text or len(text.strip()) < 10:
            return 'en'  # Default to English for short text
        
        # Method 1: Regex pattern matching
        detected_lang = self._detect_by_regex(text)
        if detected_lang:
            return detected_lang
        
        # Method 2: langdetect (if available)
        if LANGDETECT_AVAILABLE:
            detected_lang = self._detect_by_langdetect(text)
            if detected_lang:
                return detected_lang
        
        # Method 3: langid (if available)
        if LANGID_AVAILABLE:
            detected_lang = self._detect_by_langid(text)
            if detected_lang:
                return detected_lang
        
        return 'en'  # Default to English
    
    def _detect_by_regex(self, text: str) -> Optional[str]:
        """Detect language using regex patterns"""
        for lang_code, pattern in self.language_patterns.items():
            if re.search(pattern, text):
                return lang_code
        return None
    
    def _detect_by_langdetect(self, text: str) -> Optional[str]:
        """Detect language using langdetect library"""
        try:
            detected = detect(text)
            if detected in self.language_patterns:
                return detected
        except Exception:
            pass
        return None
    
    def _detect_by_langid(self, text: str) -> Optional[str]:
        """Detect language using langid library"""
        try:
            detected = langid.classify(text)[0]
            if detected in self.language_patterns:
                return detected
        except Exception:
            pass
        return None
    
    def get_supported_languages(self) -> dict:
        """Get information about supported languages and detection methods"""
        return {
            'supported_languages': list(self.language_patterns.keys()),
            'detection_methods': self.detection_methods,
            'indian_languages': [
                'hi', 'bn', 'te', 'ta', 'gu', 'kn', 'ml', 'pa', 'ur', 'or', 'as', 'mr', 'sa'
            ],
            'international_languages': [
                'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko', 'ar', 'th'
            ]
        }
    
    def is_indian_language(self, lang_code: str) -> bool:
        """Check if the language code represents an Indian language"""
        indian_languages = [
            'hi', 'bn', 'te', 'ta', 'gu', 'kn', 'ml', 'pa', 'ur', 'or', 'as', 'mr', 'sa'
        ]
        return lang_code in indian_languages
    
    def get_language_name(self, lang_code: str) -> str:
        """Get the full name of a language from its code"""
        language_names = {
            'hi': 'Hindi',
            'bn': 'Bengali',
            'te': 'Telugu',
            'ta': 'Tamil',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'ur': 'Urdu',
            'or': 'Odia',
            'as': 'Assamese',
            'mr': 'Marathi',
            'sa': 'Sanskrit',
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'th': 'Thai'
        }
        return language_names.get(lang_code, 'Unknown') 