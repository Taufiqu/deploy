# =========================================================================
# DOCKERFILE FOR BUKTI SETOR SERVICE - RAILWAY OPTIMIZED
# =========================================================================
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-ind \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p /app/uploads

# Expose port (Railway will set PORT env var)
EXPOSE 5002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5002}/health || exit 1

# Run the application with Railway PORT support
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5002} --workers 1 --timeout 60 app_bukti_setor:app"]