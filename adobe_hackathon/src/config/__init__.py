"""
Configuration modules for Enhanced PDF Outline Extractor
Contains language patterns, settings, and performance configurations
"""

from .language_config import (
    LANGUAGE_PATTERNS,
    MULTILINGUAL_HEADING_PATTERNS,
    MULTILINGUAL_HEADING_KEYWORDS,
    PERFORMANCE_SETTINGS,
    OUTPUT_SETTINGS
)

__all__ = [
    "LANGUAGE_PATTERNS",
    "MULTILINGUAL_HEADING_PATTERNS", 
    "MULTILINGUAL_HEADING_KEYWORDS",
    "PERFORMANCE_SETTINGS",
    "OUTPUT_SETTINGS"
] 