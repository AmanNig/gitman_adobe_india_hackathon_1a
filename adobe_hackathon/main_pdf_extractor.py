#!/usr/bin/env python3
"""
Enhanced PDF Outline Extractor - Main CLI Script
Modular multilingual PDF structure extraction with Indian language support
"""

import argparse
import sys
import os
import json
import time
from typing import Dict, List, Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pdf_extractor import MultilingualPDFOutlineExtractor


class PDFExtractorCLI:
    """Command-line interface for the Enhanced PDF Outline Extractor"""
    
    def __init__(self):
        self.extractor = MultilingualPDFOutlineExtractor()
        self.input_dir = 'input'
        self.output_dir = 'output'
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
    
    def validate_input_directory(self) -> bool:
        """Validate that input directory exists and contains PDF files"""
        if not os.path.exists(self.input_dir):
            print(f"Error: Input directory '{self.input_dir}' does not exist")
            return False
        
        pdf_files = [f for f in os.listdir(self.input_dir) if f.lower().endswith('.pdf')]
        if not pdf_files:
            print(f"Error: No PDF files found in '{self.input_dir}' directory")
            return False
        
        print(f"Found {len(pdf_files)} PDF files in input directory")
        return True
    
    def process_single_pdf(self, pdf_path: str, output_file: Optional[str] = None) -> Dict:
        """Process a single PDF file"""
        print(f"Processing: {os.path.basename(pdf_path)}")
        
        start_time = time.time()
        result = self.extractor.process_pdf_multilingual(pdf_path)
        processing_time = time.time() - start_time
        
        # Save result if output file specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Results saved to: {output_file}")
        
        print(f"  ✓ Found {len(result.get('outline', []))} headings")
        print(f"  ✓ Languages: {result.get('metadata', {}).get('detected_languages', [])}")
        print(f"  ✓ Processing time: {processing_time:.2f}s")
        
        return result
    
    def process_directory(self, languages: Optional[List[str]] = None) -> Dict:
        """Process all PDF files in the input directory"""
        print("\n" + "="*60)
        print("ENHANCED PDF OUTLINE EXTRACTOR - MULTILINGUAL")
        print("="*60)
        
        # Validate input
        if not self.validate_input_directory():
            return {"success": False, "error": "Input validation failed"}
        
        # Get PDF files
        pdf_files = [f for f in os.listdir(self.input_dir) if f.lower().endswith('.pdf')]
        
        overall_start_time = time.time()
        all_results = {}
        total_headings = 0
        detected_languages = set()
        
        # Process each PDF
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.input_dir, pdf_file)
            output_file = os.path.join(self.output_dir, pdf_file.replace('.pdf', '_outline.json'))
            
            result = self.process_single_pdf(pdf_path, output_file)
            
            # Collect statistics
            all_results[pdf_file] = result
            total_headings += len(result.get('outline', []))
            detected_languages.update(result.get('metadata', {}).get('detected_languages', []))
        
        overall_time = time.time() - overall_start_time
        
        # Save combined results
        combined_output = os.path.join(self.output_dir, 'pdf_outline_results.json')
        with open(combined_output, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        # Generate summary
        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "success": True,
            "overall_processing_time": overall_time,
            "total_pdfs": len(pdf_files),
            "total_headings": total_headings,
            "detected_languages": list(detected_languages),
            "combined_output": combined_output,
            "individual_results": all_results,
            "performance_metrics": self.extractor.get_performance_metrics()
        }
        
        # Save summary
        summary_file = os.path.join(self.output_dir, 'extraction_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*60)
        print("EXTRACTION SUMMARY")
        print("="*60)
        print(f"✓ Overall processing time: {overall_time:.2f} seconds")
        print(f"✓ Total PDFs processed: {len(pdf_files)}")
        print(f"✓ Total headings extracted: {total_headings}")
        print(f"✓ Languages detected: {list(detected_languages)}")
        print(f"✓ Combined results: {combined_output}")
        print(f"✓ Summary report: {summary_file}")
        
        return summary
    
    def show_language_support(self):
        """Display detailed language support information"""
        print("\n" + "="*80)
        print("LANGUAGE SUPPORT ANALYSIS")
        print("="*80)
        
        lang_info = self.extractor.get_supported_languages()
        
        print("\n🇮🇳 INDIAN LANGUAGES SUPPORT:")
        indian_langs = {
            'hi': 'Hindi (हिंदी)',
            'bn': 'Bengali (বাংলা)',
            'te': 'Telugu (తెలుగు)',
            'ta': 'Tamil (தமிழ்)',
            'gu': 'Gujarati (ગુજરાતી)',
            'kn': 'Kannada (ಕನ್ನಡ)',
            'ml': 'Malayalam (മലയാളം)',
            'pa': 'Punjabi (ਪੰਜਾਬੀ)',
            'ur': 'Urdu (اردو)',
            'or': 'Odia (ଓଡ଼ିଆ)',
            'as': 'Assamese (অসমীয়া)',
            'mr': 'Marathi (मराठी)',
            'sa': 'Sanskrit (संस्कृत)'
        }
        
        for code, name in indian_langs.items():
            print(f"  ✓ {code}: {name}")
        
        print("\n🌍 INTERNATIONAL LANGUAGES SUPPORT:")
        international_langs = {
            'en': 'English',
            'es': 'Spanish (Español)',
            'fr': 'French (Français)',
            'de': 'German (Deutsch)',
            'it': 'Italian (Italiano)',
            'pt': 'Portuguese (Português)',
            'ru': 'Russian (Русский)',
            'zh': 'Chinese (中文)',
            'ja': 'Japanese (日本語)',
            'ko': 'Korean (한국어)',
            'ar': 'Arabic (العربية)',
            'th': 'Thai (ไทย)'
        }
        
        for code, name in international_langs.items():
            print(f"  ✓ {code}: {name}")
        
        print("\n🔧 TECHNICAL CAPABILITIES:")
        print("  ✓ Language Detection: Regex patterns, LangDetect, LangID")
        print("  ✓ Unicode Script Support for all Indian languages")
        print("  ✓ Font Analysis and Heading Detection")
        print("  ✓ Multilingual Pattern Matching")
        print("  ✓ Statistical Font Analysis")
        
        print("\n📊 PERFORMANCE METRICS:")
        print("  ✓ Model Size: < 1GB (CPU optimized)")
        print("  ✓ Processing Time: < 60 seconds for 3-5 documents")
        print("  ✓ Offline Operation: No internet required")
        print("  ✓ Memory Efficient: Optimized for CPU-only execution")
        
        print(f"\n📋 DETECTION METHODS:")
        for method, available in lang_info['detection_methods'].items():
            status = "✓ Available" if available else "✗ Not available"
            print(f"  {status}: {method}")
    
    def show_architecture(self):
        """Display the modular architecture information"""
        print("\n" + "="*80)
        print("MODULAR ARCHITECTURE")
        print("="*80)
        
        print("\n📁 PROJECT STRUCTURE:")
        print("  src/")
        print("  ├── config/")
        print("  │   └── language_config.py          # Language patterns and settings")
        print("  ├── utils/")
        print("  │   ├── language_detector.py        # Language detection utilities")
        print("  │   └── font_analyzer.py            # Font analysis utilities")
        print("  ├── pdf_extractor/")
        print("  │   ├── __init__.py                 # Module initialization")
        print("  │   └── extractor.py                # Main extractor class")
        print("  ├── tests/                          # Unit tests")
        print("  └── docs/                           # Documentation")
        
        print("\n🔧 MODULES:")
        print("  ✓ Language Configuration: Centralized language patterns and settings")
        print("  ✓ Language Detector: Multilingual language detection utilities")
        print("  ✓ Font Analyzer: Statistical font analysis and threshold calculation")
        print("  ✓ PDF Extractor: Main extraction logic with modular design")
        
        print("\n🎯 BENEFITS:")
        print("  ✓ Modular Design: Easy to maintain and extend")
        print("  ✓ Separation of Concerns: Each module has a specific responsibility")
        print("  ✓ Reusability: Components can be used independently")
        print("  ✓ Testability: Each module can be tested in isolation")
        print("  ✓ Configuration Management: Centralized settings")
        print("  ✓ Scalability: Easy to add new languages and features")


def main():
    """Main function with command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description="Enhanced PDF Outline Extractor - Multilingual with Indian Language Support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all PDFs in input directory
  python main_pdf_extractor.py

  # Process a single PDF file
  python main_pdf_extractor.py --file input/document.pdf

  # Show language support information
  python main_pdf_extractor.py --show-languages

  # Show modular architecture
  python main_pdf_extractor.py --show-architecture

  # Custom input/output directories
  python main_pdf_extractor.py --input-dir my_pdfs --output-dir my_results

Features:
  ✓ Support for 13 Indian languages (Hindi, Bengali, Telugu, Tamil, etc.)
  ✓ Support for 12 international languages
  ✓ Modular architecture for easy maintenance
  ✓ Performance optimized for CPU-only execution
  ✓ Comprehensive font analysis and heading detection
        """
    )
    
    parser.add_argument('--file', type=str,
                       help='Process a single PDF file')
    parser.add_argument('--input-dir', type=str, default='input',
                       help='Input directory containing PDF files (default: input)')
    parser.add_argument('--output-dir', type=str, default='output',
                       help='Output directory for results (default: output)')
    parser.add_argument('--languages', type=str,
                       help='Comma-separated list of language codes to focus on')
    parser.add_argument('--show-languages', action='store_true',
                       help='Show detailed language support information')
    parser.add_argument('--show-architecture', action='store_true',
                       help='Show modular architecture information')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = PDFExtractorCLI()
    cli.input_dir = args.input_dir
    cli.output_dir = args.output_dir
    
    # Show information if requested
    if args.show_languages:
        cli.show_language_support()
        return
    
    if args.show_architecture:
        cli.show_architecture()
        return
    
    # Parse languages if specified
    languages = None
    if args.languages:
        languages = [lang.strip() for lang in args.languages.split(',')]
    
    # Process based on arguments
    if args.file:
        # Process single file
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' does not exist")
            sys.exit(1)
        
        output_file = os.path.join(cli.output_dir, 
                                  os.path.basename(args.file).replace('.pdf', '_outline.json'))
        result = cli.process_single_pdf(args.file, output_file)
        
        if not result.get('outline'):
            print("Warning: No headings were extracted from the document")
    else:
        # Process directory
        result = cli.process_directory(languages)
        
        if not result.get('success', False):
            print(f"Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)


if __name__ == "__main__":
    main() 