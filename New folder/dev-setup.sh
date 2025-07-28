#!/bin/bash

# =========================================================================
# DEVELOPMENT SETUP SCRIPT
# =========================================================================

echo "🚀 Setting up OCR Application for Development..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "📋 Checking dependencies..."

if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ All dependencies are installed."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please update it with your configuration."
else
    echo "✅ .env file already exists."
fi

# Create uploads directory
echo "📁 Creating uploads directory..."
mkdir -p uploads
chmod 755 uploads
echo "✅ Uploads directory created."

# Build and start services
echo "🏗️ Building and starting services..."
docker-compose -f docker-compose.dev.yml up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check Faktur service
if curl -f http://localhost:5001/health >/dev/null 2>&1; then
    echo "✅ Faktur service is healthy"
else
    echo "❌ Faktur service is not responding"
fi

# Check Bukti Setor service
if curl -f http://localhost:5002/health >/dev/null 2>&1; then
    echo "✅ Bukti Setor service is healthy"
else
    echo "❌ Bukti Setor service is not responding"
fi

echo ""
echo "🎉 Development setup complete!"
echo ""
echo "📡 Services available at:"
echo "   - Faktur Service (Tesseract):   http://localhost:5001"
echo "   - Bukti Setor Service (EasyOCR): http://localhost:5002"
echo "   - PostgreSQL Database:          localhost:5432"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: docker-compose -f docker-compose.dev.yml logs -f"
echo "   - Stop services: docker-compose -f docker-compose.dev.yml down"
echo "   - Restart services: docker-compose -f docker-compose.dev.yml restart"
echo ""
echo "📖 For deployment to Railway, see RAILWAY_DEPLOYMENT.md"
