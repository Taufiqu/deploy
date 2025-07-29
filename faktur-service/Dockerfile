# =========================================================================
# FAKTUR SERVICE WITH DATABASE SUPPORT
# =========================================================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app_minimal.py .
COPY models.py .
COPY utils/ ./utils/

# Railway dynamic port binding
CMD gunicorn --bind 0.0.0.0:$PORT app_minimal:app
