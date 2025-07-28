FROM --platform=linux/amd64 python:3.9-slim

# Set environment variables for better performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install spaCy English model (small version to stay under 1GB)
RUN python -m spacy download en_core_web_sm

# Copy the modular source code structure
COPY src/ ./src/

# Copy the main CLI script
COPY main_pdf_extractor.py .

# Copy documentation
COPY docs/ ./docs/

# Copy tests (for development/testing purposes)
COPY tests/ ./tests/

# Copy project documentation
COPY approach.md .
COPY README.md .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set permissions
RUN chmod +x main_pdf_extractor.py

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Default command - run the enhanced PDF outline extractor
CMD ["python", "main_pdf_extractor.py"]