#!/usr/bin/env python3
"""
Test Runner for Enhanced PDF Outline Extractor
Runs all test suites for the modular system
"""

import sys
import os
import unittest
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def run_all_tests():
    """Run all test suites"""
    print("="*60)
    print("ENHANCED PDF OUTLINE EXTRACTOR - TEST SUITE")
    print("="*60)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        
        # Print failure details
        if result.failures:
            print("\nFAILURES:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
        
        if result.errors:
            print("\nERRORS:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
        
        return 1


def run_specific_test(test_name):
    """Run a specific test module"""
    print(f"Running specific test: {test_name}")
    
    # Import and run specific test
    if test_name == 'language_detection':
        from tests.test_language_detection import TestLanguageDetection
        suite = unittest.TestLoader().loadTestsFromTestCase(TestLanguageDetection)
    elif test_name == 'font_analysis':
        from tests.test_font_analysis import TestFontAnalysis
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFontAnalysis)
    else:
        print(f"Unknown test: {test_name}")
        return 1
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        return run_specific_test(test_name)
    else:
        # Run all tests
        return run_all_tests()


if __name__ == '__main__':
    sys.exit(main()) 