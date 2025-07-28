# =========================================================================
# ULTRA MINIMAL TEST DOCKERFILE
# =========================================================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy minimal requirements  
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy minimal app
COPY app_minimal.py .

# Railway dynamic port binding
CMD gunicorn --bind 0.0.0.0:$PORT app_minimal:app
