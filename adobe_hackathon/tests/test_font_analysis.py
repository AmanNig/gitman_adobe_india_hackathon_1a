#!/usr/bin/env python3
"""
Test Font Analysis Module
Tests the font analysis and statistical calculations
"""

import sys
import os
import unittest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.utils.font_analyzer import FontAnalyzer


class TestFontAnalysis(unittest.TestCase):
    """Test cases for font analysis functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = FontAnalyzer()
        
        # Sample text elements for testing
        self.sample_elements = [
            {'font_size': 12.0, 'font_name': 'Arial'},
            {'font_size': 12.0, 'font_name': 'Arial'},
            {'font_size': 14.0, 'font_name': 'Arial'},
            {'font_size': 16.0, 'font_name': 'Times'},
            {'font_size': 18.0, 'font_name': 'Times'},
            {'font_size': 20.0, 'font_name': 'Arial'},
            {'font_size': 24.0, 'font_name': 'Arial'},
        ]
    
    def test_font_distribution_analysis(self):
        """Test font distribution analysis"""
        stats = self.analyzer.analyze_font_distribution(self.sample_elements)
        
        # Check basic statistics
        self.assertIn('body_font_size', stats)
        self.assertIn('thresholds', stats)
        self.assertIn('font_sizes', stats)
        self.assertIn('unique_font_sizes', stats)
        
        # Check that we have the expected number of unique font sizes
        self.assertEqual(stats['unique_font_sizes'], 6)
        
        # Check that body font size is calculated (should be most common)
        self.assertIsInstance(stats['body_font_size'], (int, float))
    
    def test_font_thresholds(self):
        """Test font threshold calculation"""
        # First analyze the distribution
        self.analyzer.analyze_font_distribution(self.sample_elements)
        thresholds = self.analyzer.get_font_thresholds()
        
        # Check that thresholds are calculated
        self.assertIn('title', thresholds)
        self.assertIn('h1', thresholds)
        self.assertIn('h2', thresholds)
        self.assertIn('h3', thresholds)
        self.assertIn('body', thresholds)
        self.assertIn('small', thresholds)
        
        # Check that thresholds are numeric
        for threshold in thresholds.values():
            self.assertIsInstance(threshold, (int, float))
    
    def test_body_font_size(self):
        """Test body font size retrieval"""
        self.analyzer.analyze_font_distribution(self.sample_elements)
        body_size = self.analyzer.get_body_font_size()
        
        self.assertIsInstance(body_size, (int, float))
        self.assertGreater(body_size, 0)
    
    def test_heading_detection(self):
        """Test heading detection logic"""
        self.analyzer.analyze_font_distribution(self.sample_elements)
        
        # Test with different font sizes
        self.assertTrue(self.analyzer.is_likely_heading(24.0))  # Large font
        self.assertTrue(self.analyzer.is_likely_heading(18.0))  # Medium-large font
        self.assertFalse(self.analyzer.is_likely_heading(12.0))  # Small font
    
    def test_heading_level_determination(self):
        """Test heading level determination"""
        self.analyzer.analyze_font_distribution(self.sample_elements)
        
        # Test different font sizes
        level = self.analyzer.get_heading_level(24.0)
        self.assertIn(level, ['H1', 'H2', 'H3'])
        
        level = self.analyzer.get_heading_level(18.0)
        self.assertIn(level, ['H1', 'H2', 'H3'])
        
        level = self.analyzer.get_heading_level(12.0)
        self.assertEqual(level, 'body')
    
    def test_font_statistics(self):
        """Test comprehensive font statistics"""
        stats = self.analyzer.analyze_font_distribution(self.sample_elements)
        font_stats = self.analyzer.get_font_statistics()
        
        # Check that statistics are comprehensive
        self.assertIn('statistics', font_stats)
        self.assertIn('font_distribution', font_stats)
        self.assertIn('percentiles', font_stats)
        
        # Check basic statistics
        basic_stats = font_stats['statistics']
        self.assertIn('mean', basic_stats)
        self.assertIn('median', basic_stats)
        self.assertIn('std_dev', basic_stats)
        self.assertIn('min', basic_stats)
        self.assertIn('max', basic_stats)
        self.assertIn('range', basic_stats)
    
    def test_font_consistency_analysis(self):
        """Test font consistency analysis"""
        consistency = self.analyzer.analyze_font_consistency(self.sample_elements)
        
        # Check that we have analysis for each font
        self.assertIn('Arial', consistency)
        self.assertIn('Times', consistency)
        
        # Check that each font analysis has the expected fields
        arial_stats = consistency['Arial']
        self.assertIn('count', arial_stats)
        self.assertIn('mean_size', arial_stats)
        self.assertIn('std_size', arial_stats)
        self.assertIn('min_size', arial_stats)
        self.assertIn('max_size', arial_stats)
        self.assertIn('size_range', arial_stats)
    
    def test_empty_elements(self):
        """Test handling of empty elements"""
        empty_stats = self.analyzer.analyze_font_distribution([])
        self.assertEqual(empty_stats, {})
        
        empty_consistency = self.analyzer.analyze_font_consistency([])
        self.assertEqual(empty_consistency, {})
    
    def test_single_element(self):
        """Test handling of single element"""
        single_element = [{'font_size': 12.0, 'font_name': 'Arial'}]
        stats = self.analyzer.analyze_font_distribution(single_element)
        
        # Should still work with single element
        self.assertIn('body_font_size', stats)
        self.assertEqual(stats['body_font_size'], 12.0)
        self.assertEqual(stats['unique_font_sizes'], 1)


if __name__ == '__main__':
    unittest.main() 