#!/bin/bash

# ========================================
# QUICK DEPLOY SCRIPT - FAKTUR SERVICE
# ========================================

echo "🚀 DEPLOYING FAKTUR SERVICE TO RAILWAY"
echo "======================================"

echo "📋 Step 1: Verify files..."
if [ ! -f "faktur-service/app_faktur.py" ]; then
    echo "❌ app_faktur.py not found!"
    exit 1
fi

if [ ! -f "faktur-service/Dockerfile.faktur" ]; then
    echo "❌ Dockerfile.faktur not found!"
    exit 1
fi

echo "✅ All required files found"

echo "📋 Step 2: Environment variables needed:"
echo "DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.co:5432/postgres"
echo "SUPABASE_URL=https://xxxxx.supabase.co"
echo "SUPABASE_ANON_KEY=your_anon_key_here"
echo "FLASK_ENV=production"
echo "FLASK_APP=app_faktur.py"
echo "SECRET_KEY=your-production-secret-key"
echo "PORT=5001"
echo "SERVICE_NAME=faktur-ocr-service"

echo ""
echo "📋 Step 3: Railway Configuration:"
echo "Root Directory: faktur-service"
echo "Dockerfile: Dockerfile.faktur"
echo "Port: 5001"

echo ""
echo "📋 Step 4: Test after deployment:"
echo "curl https://your-faktur-url.railway.app/health"

echo ""
echo "✅ FAKTUR SERVICE DEPLOYMENT GUIDE COMPLETE"
echo "Now deploy in Railway dashboard!"
