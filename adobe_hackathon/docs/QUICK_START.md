# Quick Start Guide - Enhanced PDF Outline Extractor

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.9 or higher
- Docker (optional, for containerized deployment)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Your PDF Files
Place your PDF files in the `input/` directory:
```bash
mkdir -p input output
# Copy your PDF files to input/
```

### 3. Run the Extractor
```bash
# Process all PDFs in input directory
python main_pdf_extractor.py

# Or process a single file
python main_pdf_extractor.py --file input/your_document.pdf
```

### 4. View Results
Results will be saved in the `output/` directory:
- Individual files: `output/document_name_outline.json`
- Combined results: `output/pdf_outline_results.json`
- Summary report: `output/extraction_summary.json`

## 🐳 Docker Quick Start

### Build and Run
```bash
# Build the Docker image
docker build -t adobe-pdf-extractor .

# Run with volume mounts
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output adobe-pdf-extractor
```

## 📊 Example Output

```json
{
  "title": "Sample Document",
  "outline": [
    {
      "level": "H1",
      "text": "1. Introduction",
      "page": 1,
      "language": "en",
      "font_size": 16.0,
      "is_bold": true,
      "confidence_score": 85.5
    }
  ],
  "metadata": {
    "pages": 10,
    "detected_languages": ["en"],
    "processing_time": 2.5
  }
}
```

## 🔍 Useful Commands

```bash
# Show language support
python main_pdf_extractor.py --show-languages

# Show architecture
python main_pdf_extractor.py --show-architecture

# Custom directories
python main_pdf_extractor.py --input-dir my_pdfs --output-dir my_results
```

## 🌍 Language Support

The system automatically detects and processes:
- **13 Indian Languages**: Hindi, Bengali, Telugu, Tamil, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Odia, Assamese, Marathi, Sanskrit
- **12 International Languages**: English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Thai

## ⚡ Performance

- **Processing Time**: 15-30 seconds per document
- **Memory Usage**: < 512MB
- **Model Size**: < 1GB
- **CPU Only**: No GPU required

## 🆘 Troubleshooting

### Common Issues

1. **No PDFs found**: Ensure files are in the `input/` directory
2. **Import errors**: Run `pip install -r requirements.txt`
3. **Permission errors**: Check file permissions on input/output directories

### Getting Help

- Check the main documentation in `docs/README.md`
- Review the approach document `approach.md`
- Run tests with `python test_modular_structure.py`

## 🎯 Next Steps

1. **Customize**: Modify `src/config/language_config.py` for custom patterns
2. **Extend**: Add new languages in the configuration
3. **Integrate**: Use the modular components in your own projects
4. **Deploy**: Use Docker for production deployment

---

**Ready to extract multilingual PDF outlines! 🎉** 