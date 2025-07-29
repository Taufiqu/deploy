# =========================================================================
# FAKTUR SERVICE - ULTRA MINIMAL FOR RAILWAY
# =========================================================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies without system deps
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip

# Copy application files
COPY app.py .
COPY models.py .

# Create uploads directory
RUN mkdir -p uploads

# Railway will set PORT automatically
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app
