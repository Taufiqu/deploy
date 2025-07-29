# =========================================================================
# FAKTUR SERVICE - PRODUCTION VERSION
# =========================================================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY models.py .
COPY .env.local .

# Create uploads directory
RUN mkdir -p uploads

# Expose port for Railway
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Railway dynamic port binding
CMD gunicorn --bind 0.0.0.0:$PORT app:app
