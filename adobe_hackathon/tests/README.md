# Test Suite - Enhanced PDF Outline Extractor

## 📋 Overview

This directory contains comprehensive test suites for the Enhanced PDF Outline Extractor modular system. The tests ensure code quality, functionality, and reliability.

## 🧪 Test Structure

```
tests/
├── test_language_detection.py    # Language detection tests
├── test_font_analysis.py         # Font analysis tests
├── run_tests.py                  # Test runner script
└── README.md                     # This file
```

## 🚀 Running Tests

### Run All Tests
```bash
# From project root
python tests/run_tests.py

# Or from tests directory
cd tests
python run_tests.py
```

### Run Specific Test
```bash
# Run only language detection tests
python tests/run_tests.py language_detection

# Run only font analysis tests
python tests/run_tests.py font_analysis
```

### Run Individual Test Files
```bash
# Run language detection tests directly
python tests/test_language_detection.py

# Run font analysis tests directly
python tests/test_font_analysis.py
```

## 📊 Test Coverage

### Language Detection Tests (`test_language_detection.py`)
- ✅ English language detection
- ✅ Hindi language detection
- ✅ Bengali language detection
- ✅ Telugu language detection
- ✅ Tamil language detection
- ✅ Short text fallback handling
- ✅ Empty text handling
- ✅ Supported languages information
- ✅ Indian language identification
- ✅ Language name retrieval
- ✅ Detection methods availability

### Font Analysis Tests (`test_font_analysis.py`)
- ✅ Font distribution analysis
- ✅ Font threshold calculation
- ✅ Body font size retrieval
- ✅ Heading detection logic
- ✅ Heading level determination
- ✅ Comprehensive font statistics
- ✅ Font consistency analysis
- ✅ Empty elements handling
- ✅ Single element handling

## 🎯 Test Features

### Comprehensive Coverage
- **Unit Tests**: Individual module testing
- **Edge Cases**: Empty inputs, single elements, boundary conditions
- **Error Handling**: Graceful failure recovery
- **Data Validation**: Input/output format verification

### Multilingual Testing
- **Indian Languages**: Hindi, Bengali, Telugu, Tamil
- **Script Detection**: Unicode range testing
- **Fallback Mechanisms**: Default language handling
- **Language Support**: Complete language list validation

### Font Analysis Testing
- **Statistical Analysis**: Mean, median, standard deviation
- **Threshold Calculation**: Dynamic heading detection
- **Font Consistency**: Multi-font document analysis
- **Performance**: Efficient calculation verification

## 📈 Test Results

### Expected Output
```
============================================================
ENHANCED PDF OUTLINE EXTRACTOR - TEST SUITE
============================================================
test_english_detection (test_language_detection.TestLanguageDetection) ... ok
test_hindi_detection (test_language_detection.TestLanguageDetection) ... ok
test_bengali_detection (test_language_detection.TestLanguageDetection) ... ok
...

============================================================
TEST SUMMARY
============================================================
Tests run: 25
Failures: 0
Errors: 0
Skipped: 0
Time taken: 1.23 seconds
✅ All tests passed!
```

## 🔧 Test Configuration

### Dependencies
Tests require the same dependencies as the main system:
- PyMuPDF
- langdetect
- langid
- numpy

### Environment Setup
```bash
# Install test dependencies
pip install -r requirements.txt

# Ensure src directory is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

## 🐛 Debugging Tests

### Verbose Output
```bash
# Run with verbose output
python -m unittest tests.test_language_detection -v
```

### Individual Test Debugging
```bash
# Run specific test method
python -m unittest tests.test_language_detection.TestLanguageDetection.test_hindi_detection
```

### Test Discovery
```bash
# Discover all tests
python -m unittest discover tests -p "test_*.py"
```

## 📝 Adding New Tests

### Test File Structure
```python
#!/usr/bin/env python3
"""
Test Module Name
Brief description of what this test module covers
"""

import sys
import os
import unittest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from module_name import ClassName


class TestClassName(unittest.TestCase):
    """Test cases for ClassName functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def test_specific_functionality(self):
        """Test specific functionality"""
        # Test implementation
        pass


if __name__ == '__main__':
    unittest.main()
```

### Test Naming Conventions
- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<functionality_description>`

## 🎯 Best Practices

### Test Design
- **Isolation**: Each test should be independent
- **Clarity**: Clear test names and descriptions
- **Coverage**: Test both success and failure cases
- **Performance**: Keep tests fast and efficient

### Test Data
- **Sample Data**: Use realistic but minimal test data
- **Edge Cases**: Include boundary conditions
- **Multilingual**: Test with various languages
- **Formats**: Test different input formats

### Maintenance
- **Regular Updates**: Update tests when code changes
- **Documentation**: Keep test documentation current
- **Performance**: Monitor test execution time
- **Coverage**: Maintain high test coverage

---

**Run tests regularly to ensure system reliability! 🧪✅** 