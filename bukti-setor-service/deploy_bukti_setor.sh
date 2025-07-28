#!/bin/bash

# ========================================
# QUICK DEPLOY SCRIPT - BUKTI SETOR SERVICE
# ========================================

echo "🚀 DEPLOYING BUKTI SETOR SERVICE TO RAILWAY"
echo "==========================================="

echo "📋 Step 1: Verify files..."
if [ ! -f "bukti-setor-service/app_bukti_setor.py" ]; then
    echo "❌ app_bukti_setor.py not found!"
    exit 1
fi

if [ ! -f "bukti-setor-service/Dockerfile.bukti-setor" ]; then
    echo "❌ Dockerfile.bukti-setor not found!"
    exit 1
fi

echo "✅ All required files found"

echo "📋 Step 2: Environment variables needed:"
echo "DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.co:5432/postgres"
echo "SUPABASE_URL=https://xxxxx.supabase.co"
echo "SUPABASE_ANON_KEY=your_anon_key_here"
echo "FLASK_ENV=production"
echo "FLASK_APP=app_bukti_setor.py"
echo "SECRET_KEY=your-production-secret-key"
echo "PORT=5002"
echo "SERVICE_NAME=bukti-setor-ocr-service"
echo "EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR"

echo ""
echo "📋 Step 3: Railway Configuration:"
echo "Root Directory: bukti-setor-service"
echo "Dockerfile: Dockerfile.bukti-setor"
echo "Port: 5002"

echo ""
echo "📋 Step 4: Test after deployment:"
echo "curl https://your-bukti-setor-url.railway.app/health"

echo ""
echo "⚠️  IMPORTANT: This service takes 10-15 minutes to deploy (EasyOCR models download)"

echo ""
echo "✅ BUKTI SETOR SERVICE DEPLOYMENT GUIDE COMPLETE"
echo "Now deploy in Railway dashboard!"
