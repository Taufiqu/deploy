# =========================================================================
# FAKTUR SERVICE - WITH POSTGRESQL SUPPORT
# =========================================================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies for PostgreSQL and OCR
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    tesseract-ocr \
    tesseract-ocr-ind \
    poppler-utils \
    libpoppler-cpp-dev \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip

# Copy application files
COPY app.py .
COPY models.py .
COPY ocr_engine.py .

# Set environment variables untuk OCR
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# Create uploads directory
RUN mkdir -p uploads

# Railway will set PORT automatically
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app
