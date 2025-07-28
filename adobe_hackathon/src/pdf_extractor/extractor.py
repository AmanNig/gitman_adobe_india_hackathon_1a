"""
Enhanced PDF Outline Extractor - Main Extractor Class
Multilingual PDF structure extraction with Indian language support
"""

import json
import sys
import os
import re
import time
from typing import Dict, List, Tuple, Optional
import fitz  # PyMuPDF
from collections import defaultdict, Counter

from src.config.language_config import (
    MULTILINGUAL_HEADING_PATTERNS,
    MULTILINGUAL_HEADING_KEYWORDS,
    PERFORMANCE_SETTINGS,
    OUTPUT_SETTINGS
)
from src.utils.language_detector import LanguageDetector
from src.utils.font_analyzer import FontAnalyzer


class MultilingualPDFOutlineExtractor:
    """
    Enhanced PDF Outline Extractor with multilingual support
    Supports all Indian languages and international languages
    """
    
    def __init__(self):
        # Initialize utilities
        self.language_detector = LanguageDetector()
        self.font_analyzer = FontAnalyzer()
        
        # Performance tracking
        self.processing_times = {}
        self.detected_languages = set()
        
        # Settings
        self.heading_score_threshold = PERFORMANCE_SETTINGS['heading_score_threshold']
        self.max_processing_time = PERFORMANCE_SETTINGS['max_processing_time']
    
    def extract_text_elements(self, pdf_path: str) -> List[Dict]:
        """
        Extract text elements with font and position information
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            List[Dict]: List of text elements with formatting information
        """
        try:
            doc = fitz.open(pdf_path)
            text_elements = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get text blocks with formatting
                blocks = page.get_text("dict")
                
                for block in blocks["blocks"]:
                    if "lines" in block:  # Text block
                        for line in block["lines"]:
                            line_text = ""
                            spans_info = []
                            
                            for span in line["spans"]:
                                text = span["text"].strip()
                                if text:
                                    line_text += text + " "
                                    spans_info.append(span)
                            
                            if line_text.strip() and spans_info:
                                # Use the most common font size in the line
                                font_sizes = [span["size"] for span in spans_info]
                                avg_font_size = sum(font_sizes) / len(font_sizes)
                                
                                # Check if any span is bold
                                is_bold = any(span["flags"] & 2**4 for span in spans_info)
                                
                                # Get font name from the first span
                                font_name = spans_info[0]["font"] if spans_info else "Unknown"
                                
                                # Detect language for this text element
                                detected_lang = self.language_detector.detect_language(line_text.strip())
                                self.detected_languages.add(detected_lang)
                                
                                text_elements.append({
                                    'text': line_text.strip(),
                                    'font_size': round(avg_font_size, 1),
                                    'font_name': font_name,
                                    'is_bold': is_bold,
                                    'page': page_num + 1,
                                    'bbox': spans_info[0]["bbox"],
                                    'language': detected_lang
                                })
            
            doc.close()
            return text_elements
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}", file=sys.stderr)
            return []
    
    def is_heading_by_pattern_multilingual(self, text: str, level: str, language: str) -> bool:
        """
        Check if text matches heading patterns for given level and language
        
        Args:
            text (str): Text to check
            level (str): Heading level ('H1', 'H2', 'H3')
            language (str): Language code
            
        Returns:
            bool: True if text matches heading patterns
        """
        text_clean = text.strip()
        patterns = MULTILINGUAL_HEADING_PATTERNS.get(language, MULTILINGUAL_HEADING_PATTERNS['en'])
        
        if level == 'H1':
            level_patterns = patterns.get('h1', [])
        elif level == 'H2':
            level_patterns = patterns.get('h2', [])
        elif level == 'H3':
            level_patterns = patterns.get('h3', [])
        else:
            return False
        
        for pattern in level_patterns:
            if re.match(pattern, text_clean, re.IGNORECASE):
                return True
        
        return False
    
    def is_heading_by_keywords_multilingual(self, text: str, language: str) -> bool:
        """
        Check if text contains heading keywords in the specified language
        
        Args:
            text (str): Text to check
            language (str): Language code
            
        Returns:
            bool: True if text contains heading keywords
        """
        text_lower = text.lower()
        keywords = MULTILINGUAL_HEADING_KEYWORDS.get(language, MULTILINGUAL_HEADING_KEYWORDS['en'])
        
        # Check if any word is a heading keyword
        words = text_lower.split()
        for word in words:
            if word in keywords:
                return True
        
        # Check for common heading phrases
        for keyword in keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    def calculate_heading_score_multilingual(self, element: Dict, stats: Dict) -> float:
        """
        Calculate a score indicating how likely this element is a heading
        
        Args:
            element (Dict): Text element with formatting information
            stats (Dict): Font analysis statistics
            
        Returns:
            float: Heading confidence score (0-100)
        """
        text = element['text']
        font_size = element['font_size']
        is_bold = element['is_bold']
        language = element.get('language', 'en')
        
        score = 0.0
        
        # Font size score (0-40 points)
        thresholds = stats.get('thresholds', {})
        if font_size >= thresholds.get('title', font_size + 2):
            score += 40
        elif font_size >= thresholds.get('h1', font_size + 1.5):
            score += 30
        elif font_size >= thresholds.get('h2', font_size + 1.0):
            score += 20
        elif font_size >= thresholds.get('h3', font_size + 0.5):
            score += 10
        
        # Bold text bonus (0-20 points)
        if is_bold:
            score += 20
        
        # Pattern matching score (0-20 points)
        for level in ['H1', 'H2', 'H3']:
            if self.is_heading_by_pattern_multilingual(text, level, language):
                score += 20
                break
        
        # Keyword matching score (0-10 points)
        if self.is_heading_by_keywords_multilingual(text, language):
            score += 10
        
        # Length penalty (headings are usually short)
        if len(text) > 100:
            score -= 10
        elif len(text) < 3:
            score -= 20
        
        # Position bonus (headings often start with numbers or letters)
        if re.match(r'^[A-Za-z0-9\u0900-\u097F\u0980-\u09FF\u0C00-\u0C7F\u0B80-\u0BFF\u0A80-\u0AFF\u0C80-\u0CFF\u0D00-\u0D7F\u0A00-\u0A7F\u0600-\u06FF\u0B00-\u0B7F]', text):
            score += 5
        
        return max(0, score)
    
    def determine_heading_level_multilingual(self, element: Dict, stats: Dict) -> Optional[str]:
        """
        Determine the heading level based on font size and patterns
        
        Args:
            element (Dict): Text element with formatting information
            stats (Dict): Font analysis statistics
            
        Returns:
            Optional[str]: Heading level ('H1', 'H2', 'H3') or None
        """
        font_size = element['font_size']
        text = element['text']
        language = element.get('language', 'en')
        
        # Check patterns first
        if self.is_heading_by_pattern_multilingual(text, 'H1', language):
            return 'H1'
        elif self.is_heading_by_pattern_multilingual(text, 'H2', language):
            return 'H2'
        elif self.is_heading_by_pattern_multilingual(text, 'H3', language):
            return 'H3'
        
        # Use font size thresholds
        thresholds = stats.get('thresholds', {})
        if font_size >= thresholds.get('title', font_size + 2):
            return 'H1'
        elif font_size >= thresholds.get('h1', font_size + 1.5):
            return 'H1'
        elif font_size >= thresholds.get('h2', font_size + 1.0):
            return 'H2'
        elif font_size >= thresholds.get('h3', font_size + 0.5):
            return 'H3'
        
        return None
    
    def extract_title_multilingual(self, text_elements: List[Dict], stats: Dict) -> str:
        """
        Extract the document title with multilingual support
        
        Args:
            text_elements (List[Dict]): List of text elements
            stats (Dict): Font analysis statistics
            
        Returns:
            str: Document title
        """
        if not text_elements:
            return "Untitled Document"
        
        # Look for the largest font size element on the first page
        first_page_elements = [elem for elem in text_elements if elem['page'] == 1]
        
        if not first_page_elements:
            return "Untitled Document"
        
        # Sort by font size (descending) and score
        candidates = []
        for elem in first_page_elements:
            score = self.calculate_heading_score_multilingual(elem, stats)
            candidates.append((elem, score))
        
        candidates.sort(key=lambda x: (x[0]['font_size'], x[1]), reverse=True)
        
        # Return the best candidate
        if candidates:
            return candidates[0][0]['text']
        
        return "Untitled Document"
    
    def extract_headings_multilingual(self, text_elements: List[Dict], stats: Dict) -> List[Dict]:
        """
        Extract headings from the document with multilingual support
        
        Args:
            text_elements (List[Dict]): List of text elements
            stats (Dict): Font analysis statistics
            
        Returns:
            List[Dict]: List of extracted headings
        """
        headings = []
        
        for element in text_elements:
            score = self.calculate_heading_score_multilingual(element, stats)
            
            # Only consider elements with a good heading score
            if score >= self.heading_score_threshold:
                level = self.determine_heading_level_multilingual(element, stats)
                
                if level:
                    headings.append({
                        'level': level,
                        'text': element['text'],
                        'page': element['page'],
                        'language': element.get('language', 'en'),
                        'font_size': float(element['font_size']),
                        'is_bold': element['is_bold'],
                        'confidence_score': float(score)
                    })
        
        # Remove duplicates and sort by page, then by level
        unique_headings = []
        seen_texts = set()
        
        for heading in headings:
            text_normalized = heading['text'].strip().lower()
            if text_normalized not in seen_texts:
                seen_texts.add(text_normalized)
                unique_headings.append(heading)
        
        # Sort by page number, then by level hierarchy
        level_order = {'H1': 1, 'H2': 2, 'H3': 3}
        unique_headings.sort(key=lambda x: (x['page'], level_order.get(x['level'], 4)))
        
        return unique_headings
    
    def process_pdf_multilingual(self, pdf_path: str) -> Dict:
        """
        Main method to process a PDF and extract outline with multilingual support
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Dict: Extracted outline with metadata
        """
        start_time = time.time()
        
        try:
            # Extract text elements
            text_elements = self.extract_text_elements(pdf_path)
            
            if not text_elements:
                return {
                    "title": "Untitled Document",
                    "outline": [],
                    "metadata": {
                        "pages": 0,
                        "text_elements": 0,
                        "detected_languages": [],
                        "multilingual_support": True,
                        "processing_time": 0.0
                    }
                }
            
            # Analyze font distribution
            stats = self.font_analyzer.analyze_font_distribution(text_elements)
            
            # Extract title and headings
            title = self.extract_title_multilingual(text_elements, stats)
            headings = self.extract_headings_multilingual(text_elements, stats)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            self.processing_times[pdf_path] = processing_time
            
            # Add metadata
            metadata = {
                "pages": max(elem['page'] for elem in text_elements) if text_elements else 0,
                "text_elements": len(text_elements),
                "body_font_size": stats.get('body_font_size', 0),
                "unique_font_sizes": stats.get('unique_font_sizes', 0),
                "size_thresholds": stats.get('thresholds', {}),
                "font_distribution": stats.get('font_distribution', {}),
                "detected_languages": list(self.detected_languages),
                "multilingual_support": True,
                "processing_time": round(processing_time, 2),
                "language_detection_methods": self.language_detector.detection_methods,
                "font_statistics": stats.get('statistics', {}),
                "font_consistency": self.font_analyzer.analyze_font_consistency(text_elements)
            }
            
            return {
                "title": title,
                "outline": headings,
                "metadata": metadata
            }
            
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {e}", file=sys.stderr)
            return {
                "title": "Error Processing Document",
                "outline": [],
                "metadata": {
                    "pages": 0, 
                    "text_elements": 0,
                    "detected_languages": [],
                    "multilingual_support": True,
                    "processing_time": 0.0,
                    "error": str(e)
                }
            }
    
    def get_supported_languages(self) -> Dict:
        """Get information about supported languages"""
        return self.language_detector.get_supported_languages()
    
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics and statistics"""
        return {
            "processing_times": self.processing_times,
            "detected_languages": list(self.detected_languages),
            "font_statistics": self.font_analyzer.get_font_statistics(),
            "settings": {
                "heading_score_threshold": self.heading_score_threshold,
                "max_processing_time": self.max_processing_time
            }
        } 