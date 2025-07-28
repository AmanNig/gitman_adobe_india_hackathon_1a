#!/usr/bin/env python3
"""
Test Language Detection Module
Tests the multilingual language detection capabilities
"""

import sys
import os
import unittest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.utils.language_detector import LanguageDetector


class TestLanguageDetection(unittest.TestCase):
    """Test cases for language detection functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = LanguageDetector()
    
    def test_english_detection(self):
        """Test English language detection"""
        text = "This is a sample English text for testing language detection."
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, 'en')
    
    def test_hindi_detection(self):
        """Test Hindi language detection"""
        text = "यह एक हिंदी पाठ है जो परीक्षण के लिए है।"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, 'hi')
    
    def test_bengali_detection(self):
        """Test Bengali language detection"""
        text = "এটি একটি বাংলা পাঠ যা পরীক্ষার জন্য।"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, 'bn')
    
    def test_telugu_detection(self):
        """Test Telugu language detection"""
        text = "ఇది టెస్టింగ్ కోసం ఒక తెలుగు టెక్స్ట్."
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, 'te')
    
    def test_tamil_detection(self):
        """Test Tamil language detection"""
        text = "இது சோதனைக்கான ஒரு தமிழ் உரை."
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, 'ta')
    
    def test_short_text_fallback(self):
        """Test fallback to English for short text"""
        text = "Hi"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, 'en')
    
    def test_empty_text_fallback(self):
        """Test fallback to English for empty text"""
        text = ""
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, 'en')
    
    def test_supported_languages(self):
        """Test supported languages information"""
        lang_info = self.detector.get_supported_languages()
        
        # Check that we have the expected number of languages
        self.assertGreaterEqual(len(lang_info['supported_languages']), 20)
        self.assertEqual(len(lang_info['indian_languages']), 13)
        self.assertGreaterEqual(len(lang_info['international_languages']), 10)
    
    def test_indian_language_check(self):
        """Test Indian language identification"""
        self.assertTrue(self.detector.is_indian_language('hi'))
        self.assertTrue(self.detector.is_indian_language('bn'))
        self.assertTrue(self.detector.is_indian_language('te'))
        self.assertFalse(self.detector.is_indian_language('en'))
        self.assertFalse(self.detector.is_indian_language('es'))
    
    def test_language_names(self):
        """Test language name retrieval"""
        self.assertEqual(self.detector.get_language_name('hi'), 'Hindi')
        self.assertEqual(self.detector.get_language_name('en'), 'English')
        self.assertEqual(self.detector.get_language_name('xx'), 'Unknown')
    
    def test_detection_methods(self):
        """Test detection methods availability"""
        methods = self.detector.detection_methods
        self.assertTrue(methods['regex'])  # Regex should always be available
        # langdetect and langid may or may not be available depending on installation


if __name__ == '__main__':
    unittest.main() 