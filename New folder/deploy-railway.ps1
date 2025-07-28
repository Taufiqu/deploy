# =========================================================================
# RAILWAY DEPLOYMENT AUTOMATION SCRIPT (PowerShell)
# =========================================================================

param(
    [string]$DatabaseUrl = "",
    [string]$SecretKey = ""
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

function Check-Prerequisites {
    Write-Status "Checking prerequisites..."
    
    # Check Node.js
    try {
        $nodeVersion = node --version
        Write-Success "Node.js found: $nodeVersion"
    } catch {
        Write-Error "Node.js not found. Please install Node.js first."
        exit 1
    }
    
    # Check Railway CLI
    try {
        $railwayVersion = railway --version
        Write-Success "Railway CLI found: $railwayVersion"
    } catch {
        Write-Warning "Railway CLI not found. Installing..."
        npm install -g @railway/cli
        Write-Success "Railway CLI installed"
    }
}

function Set-EnvironmentVariables {
    Write-Status "Setting up environment variables..."
    
    # Generate secret key if not provided
    if ([string]::IsNullOrEmpty($SecretKey)) {
        $SecretKey = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Guid]::NewGuid().ToString()))
    }
    
    # Validate database URL
    if ([string]::IsNullOrEmpty($DatabaseUrl)) {
        Write-Error "Database URL is required!"
        Write-Host "Please provide database URL using -DatabaseUrl parameter"
        Write-Host "Example: .\deploy-railway.ps1 -DatabaseUrl 'postgresql://user:pass@host:port/db'"
        exit 1
    }
    
    Write-Success "Environment variables configured"
}

function Create-EnvFiles {
    Write-Status "Creating environment files..."
    
    # Faktur service environment
    $fakturEnv = @"
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5001
POPPLER_PATH=/usr/bin
SERVICE_NAME=faktur-ocr
SECRET_KEY=$SecretKey
DATABASE_URL=$DatabaseUrl
LOG_LEVEL=INFO
"@
    
    $fakturEnv | Out-File -FilePath ".env.faktur" -Encoding UTF8
    Write-Success "Created .env.faktur"
    
    # Bukti Setor service environment
    $buktiSetorEnv = @"
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5002
POPPLER_PATH=/usr/bin
SERVICE_NAME=bukti-setor-ocr
EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR
SECRET_KEY=$SecretKey
DATABASE_URL=$DatabaseUrl
LOG_LEVEL=INFO
"@
    
    $buktiSetorEnv | Out-File -FilePath ".env.bukti-setor" -Encoding UTF8
    Write-Success "Created .env.bukti-setor"
}

function Test-LocalServices {
    Write-Status "Testing local services (optional)..."
    
    Write-Host ""
    Write-Host "To test locally before deployment:"
    Write-Host "1. Install dependencies: pip install -r requirements-faktur.txt"
    Write-Host "2. Run Faktur service: python app_faktur.py"
    Write-Host "3. Run Bukti Setor service: python app_bukti_setor.py"
    Write-Host "4. Test endpoints: python test_services.py"
    Write-Host ""
}

function Show-DeploymentInstructions {
    Write-Status "Showing Railway deployment instructions..."
    
    Write-Host ""
    Write-Host "🚀 MANUAL DEPLOYMENT STEPS FOR RAILWAY:" -ForegroundColor $Green
    Write-Host "========================================"
    Write-Host ""
    
    Write-Host "1. CREATE RAILWAY PROJECT:" -ForegroundColor $Yellow
    Write-Host "   - Go to https://railway.app"
    Write-Host "   - Create new project"
    Write-Host "   - Connect your GitHub repository"
    Write-Host ""
    
    Write-Host "2. CREATE FAKTUR SERVICE:" -ForegroundColor $Yellow
    Write-Host "   - Add new service to project"
    Write-Host "   - Set Dockerfile path: Dockerfile.faktur"
    Write-Host "   - Set health check path: /health"
    Write-Host "   - Add environment variables from .env.faktur"
    Write-Host ""
    
    Write-Host "3. CREATE BUKTI SETOR SERVICE:" -ForegroundColor $Yellow
    Write-Host "   - Add another service to same project"
    Write-Host "   - Set Dockerfile path: Dockerfile.bukti-setor"
    Write-Host "   - Set health check path: /health"
    Write-Host "   - Add environment variables from .env.bukti-setor"
    Write-Host ""
    
    Write-Host "4. DEPLOY:" -ForegroundColor $Yellow
    Write-Host "   - Push changes to GitHub"
    Write-Host "   - Railway will automatically deploy both services"
    Write-Host ""
    
    Write-Host "📋 ENVIRONMENT VARIABLES TO SET IN RAILWAY:" -ForegroundColor $Green
    Write-Host "============================================"
    Write-Host ""
    Write-Host "For both services:"
    Write-Host "DATABASE_URL=$DatabaseUrl"
    Write-Host "SECRET_KEY=$SecretKey"
    Write-Host "FLASK_ENV=production"
    Write-Host "FLASK_DEBUG=false"
    Write-Host "POPPLER_PATH=/usr/bin"
    Write-Host ""
    Write-Host "For Faktur Service only:"
    Write-Host "PORT=5001"
    Write-Host "SERVICE_NAME=faktur-ocr"
    Write-Host ""
    Write-Host "For Bukti Setor Service only:"
    Write-Host "PORT=5002"
    Write-Host "SERVICE_NAME=bukti-setor-ocr"
    Write-Host "EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR"
    Write-Host ""
}

function Main {
    Write-Host "🚀 Railway Deployment Setup for OCR Services" -ForegroundColor $Green
    Write-Host "=============================================" -ForegroundColor $Green
    Write-Host ""
    
    Check-Prerequisites
    Set-EnvironmentVariables
    Create-EnvFiles
    Test-LocalServices
    Show-DeploymentInstructions
    
    Write-Success "Setup completed!"
    Write-Host ""
    Write-Host "📁 Files created:" -ForegroundColor $Blue
    Write-Host "  - .env.faktur (Faktur service environment)"
    Write-Host "  - .env.bukti-setor (Bukti Setor service environment)"
    Write-Host ""
    Write-Host "📖 Next steps:" -ForegroundColor $Blue
    Write-Host "  1. Follow the manual deployment instructions above"
    Write-Host "  2. Read RAILWAY_DEPLOYMENT.md for detailed guide"
    Write-Host "  3. Test your deployed services"
    Write-Host ""
}

# Run main function
Main
