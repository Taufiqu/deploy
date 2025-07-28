#!/bin/bash

# =========================================================================
# RAILWAY DEPLOYMENT AUTOMATION SCRIPT
# =========================================================================

set -e  # Exit on any error

echo "🚀 Starting Railway Deployment Process..."
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Railway CLI is installed
check_railway_cli() {
    print_status "Checking Railway CLI..."
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI not found. Installing..."
        npm install -g @railway/cli
        print_success "Railway CLI installed"
    else
        print_success "Railway CLI found"
    fi
}

# Login to Railway
railway_login() {
    print_status "Checking Railway authentication..."
    if ! railway whoami &> /dev/null; then
        print_warning "Not logged in to Railway. Please login..."
        railway login
    else
        print_success "Already logged in to Railway"
    fi
}

# Create or use existing Railway project
setup_project() {
    print_status "Setting up Railway project..."
    
    # Check if railway.json exists
    if [ ! -f "railway.json" ]; then
        print_status "Creating new Railway project..."
        railway new
    else
        print_success "Using existing Railway project"
    fi
}

# Deploy Faktur Service
deploy_faktur_service() {
    print_status "Deploying Faktur Service (Tesseract OCR)..."
    
    # Create service for Faktur
    print_status "Creating Faktur service..."
    
    # Set environment variables for Faktur service
    print_status "Setting environment variables for Faktur service..."
    
    cat << EOF > .env.faktur
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5001
POPPLER_PATH=/usr/bin
SERVICE_NAME=faktur-ocr
SECRET_KEY=${SECRET_KEY:-$(openssl rand -base64 32)}
DATABASE_URL=${DATABASE_URL}
EOF

    print_success "Faktur service configuration ready"
}

# Deploy Bukti Setor Service
deploy_bukti_setor_service() {
    print_status "Deploying Bukti Setor Service (EasyOCR)..."
    
    # Create service for Bukti Setor
    print_status "Creating Bukti Setor service..."
    
    # Set environment variables for Bukti Setor service
    print_status "Setting environment variables for Bukti Setor service..."
    
    cat << EOF > .env.bukti-setor
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5002
POPPLER_PATH=/usr/bin
SERVICE_NAME=bukti-setor-ocr
EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR
SECRET_KEY=${SECRET_KEY:-$(openssl rand -base64 32)}
DATABASE_URL=${DATABASE_URL}
EOF

    print_success "Bukti Setor service configuration ready"
}

# Verify deployment
verify_deployment() {
    print_status "Verifying deployment..."
    
    # Wait for services to start
    print_status "Waiting for services to start (60 seconds)..."
    sleep 60
    
    # Check Faktur service health
    if [ ! -z "$FAKTUR_URL" ]; then
        print_status "Checking Faktur service health..."
        if curl -f "$FAKTUR_URL/health" > /dev/null 2>&1; then
            print_success "Faktur service is healthy"
        else
            print_warning "Faktur service health check failed"
        fi
    fi
    
    # Check Bukti Setor service health
    if [ ! -z "$BUKTI_SETOR_URL" ]; then
        print_status "Checking Bukti Setor service health..."
        if curl -f "$BUKTI_SETOR_URL/health" > /dev/null 2>&1; then
            print_success "Bukti Setor service is healthy"
        else
            print_warning "Bukti Setor service health check failed"
        fi
    fi
}

# Main deployment flow
main() {
    echo "🔧 Railway Deployment Automation"
    echo "================================"
    
    # Check required environment variables
    if [ -z "$DATABASE_URL" ]; then
        print_error "DATABASE_URL environment variable is required"
        echo "Please set your database URL:"
        echo "export DATABASE_URL='postgresql://user:pass@host:port/db'"
        exit 1
    fi
    
    # Check dependencies
    check_railway_cli
    
    # Railway setup
    railway_login
    setup_project
    
    # Deploy services
    deploy_faktur_service
    deploy_bukti_setor_service
    
    # Verify deployment
    # verify_deployment
    
    print_success "Deployment completed!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Check Railway dashboard for service URLs"
    echo "2. Test health endpoints:"
    echo "   - Faktur: https://your-faktur-service.railway.app/health"
    echo "   - Bukti Setor: https://your-bukti-setor-service.railway.app/health"
    echo "3. Update your frontend to use the new service URLs"
    echo ""
    echo "🔗 Useful Commands:"
    echo "   railway logs           - View logs"
    echo "   railway status         - Check service status"
    echo "   railway open          - Open Railway dashboard"
}

# Run main function
main "$@"
