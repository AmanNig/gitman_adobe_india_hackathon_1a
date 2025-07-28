"""
Font Analysis Utilities for Enhanced PDF Outline Extractor
Provides font size analysis and statistical calculations
"""

import statistics
from typing import Dict, List
from collections import Counter


class FontAnalyzer:
    """Font analysis and statistics utility"""
    
    def __init__(self):
        self.font_stats = {}
    
    def analyze_font_distribution(self, text_elements: List[Dict]) -> Dict:
        """
        Analyze font size distribution to determine thresholds
        
        Args:
            text_elements (List[Dict]): List of text elements with font information
            
        Returns:
            Dict: Font analysis statistics and thresholds
        """
        if not text_elements:
            return {}
        
        # Extract font sizes and names
        font_sizes = [elem['font_size'] for elem in text_elements]
        font_names = [elem.get('font_name', 'Unknown') for elem in text_elements]
        font_sizes.sort()
        
        # Calculate basic statistics
        mean_size = statistics.mean(font_sizes)
        std_size = statistics.stdev(font_sizes) if len(font_sizes) > 1 else 0
        median_size = statistics.median(font_sizes)
        
        # Find the most common font size (likely body text)
        size_counts = Counter(font_sizes)
        body_font_size = size_counts.most_common(1)[0][0]
        
        # Analyze font names
        font_counter = Counter(font_names)
        
        # Determine thresholds based on standard deviations
        thresholds = {
            'title': body_font_size + 2 * std_size,
            'h1': body_font_size + 1.5 * std_size,
            'h2': body_font_size + 1.0 * std_size,
            'h3': body_font_size + 0.5 * std_size,
            'body': body_font_size,
            'small': body_font_size - 0.5 * std_size
        }
        
        # Calculate percentiles
        percentiles = {
            'p10': statistics.quantiles(font_sizes, n=10)[0] if len(font_sizes) > 1 else font_sizes[0],
            'p25': statistics.quantiles(font_sizes, n=4)[0] if len(font_sizes) > 1 else font_sizes[0],
            'p50': median_size,
            'p75': statistics.quantiles(font_sizes, n=4)[2] if len(font_sizes) > 1 else font_sizes[-1],
            'p90': statistics.quantiles(font_sizes, n=10)[8] if len(font_sizes) > 1 else font_sizes[-1]
        }
        
        # Store analysis results
        self.font_stats = {
            'body_font_size': body_font_size,
            'thresholds': thresholds,
            'font_sizes': font_sizes,
            'size_counts': dict(size_counts),
            'font_distribution': dict(font_counter.most_common(5)),
            'unique_font_sizes': len(set(font_sizes)),
            'statistics': {
                'mean': mean_size,
                'median': median_size,
                'std_dev': std_size,
                'min': min(font_sizes),
                'max': max(font_sizes),
                'range': max(font_sizes) - min(font_sizes)
            },
            'percentiles': percentiles
        }
        
        return self.font_stats
    
    def get_font_thresholds(self) -> Dict:
        """Get font size thresholds for heading detection"""
        return self.font_stats.get('thresholds', {})
    
    def get_body_font_size(self) -> float:
        """Get the most common font size (body text)"""
        return self.font_stats.get('body_font_size', 12.0)
    
    def is_likely_heading(self, font_size: float) -> bool:
        """
        Check if a font size is likely to be a heading
        
        Args:
            font_size (float): Font size to check
            
        Returns:
            bool: True if likely a heading
        """
        thresholds = self.get_font_thresholds()
        return font_size >= thresholds.get('h3', font_size + 1)
    
    def get_heading_level(self, font_size: float) -> str:
        """
        Determine heading level based on font size
        
        Args:
            font_size (float): Font size to analyze
            
        Returns:
            str: Heading level ('H1', 'H2', 'H3', or 'body')
        """
        thresholds = self.get_font_thresholds()
        
        if font_size >= thresholds.get('title', font_size + 2):
            return 'H1'
        elif font_size >= thresholds.get('h1', font_size + 1.5):
            return 'H1'
        elif font_size >= thresholds.get('h2', font_size + 1.0):
            return 'H2'
        elif font_size >= thresholds.get('h3', font_size + 0.5):
            return 'H3'
        else:
            return 'body'
    
    def get_font_statistics(self) -> Dict:
        """Get comprehensive font statistics"""
        return self.font_stats
    
    def analyze_font_consistency(self, text_elements: List[Dict]) -> Dict:
        """
        Analyze font consistency across the document
        
        Args:
            text_elements (List[Dict]): List of text elements
            
        Returns:
            Dict: Font consistency analysis
        """
        if not text_elements:
            return {}
        
        # Group by font name
        font_groups = {}
        for elem in text_elements:
            font_name = elem.get('font_name', 'Unknown')
            if font_name not in font_groups:
                font_groups[font_name] = []
            font_groups[font_name].append(elem['font_size'])
        
        # Analyze each font group
        font_analysis = {}
        for font_name, sizes in font_groups.items():
            font_analysis[font_name] = {
                'count': len(sizes),
                'mean_size': statistics.mean(sizes),
                'std_size': statistics.stdev(sizes) if len(sizes) > 1 else 0,
                'min_size': min(sizes),
                'max_size': max(sizes),
                'size_range': max(sizes) - min(sizes)
            }
        
        return font_analysis 