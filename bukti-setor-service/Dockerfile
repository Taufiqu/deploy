# =========================================================================
# DOCKERFILE FOR BUKTI SETOR SERVICE (EASYOCR)
# =========================================================================
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    FLASK_ENV=production \
    PYTHONPATH=/app \
    EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR

# Install system dependencies for EasyOCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgstreamer-plugins-base1.0-0 \
    libgstreamer1.0-0 \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Install PyTorch CPU version first (separate to avoid conflicts)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other requirements
RUN pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# Pre-download EasyOCR models to reduce startup time
RUN python -c "import easyocr; reader = easyocr.Reader(['id', 'en'], gpu=False, model_storage_directory='/tmp/easyocr_models')" && \
    mkdir -p /home/appuser/.EasyOCR && \
    cp -r /tmp/easyocr_models/* /home/appuser/.EasyOCR/ && \
    rm -rf /tmp/easyocr_models

# Copy application code
COPY . .

# Create uploads directory and set permissions
RUN mkdir -p /app/uploads && \
    chown -R appuser:appuser /app && \
    chown -R appuser:appuser /home/appuser/.EasyOCR

# Switch to non-root user
USER appuser

# Set Poppler path for production
ENV POPPLER_PATH=/usr/bin

# Expose port
EXPOSE 5002

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5002/health || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "1", "--timeout", "180", "app_bukti_setor:app"]
