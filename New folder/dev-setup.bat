@echo off
REM =========================================================================
REM DEVELOPMENT SETUP SCRIPT FOR WINDOWS
REM =========================================================================

echo 🚀 Setting up OCR Application for Development...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ All dependencies are installed.

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ✅ Created .env file. Please update it with your configuration.
) else (
    echo ✅ .env file already exists.
)

REM Create uploads directory
echo 📁 Creating uploads directory...
if not exist uploads mkdir uploads
echo ✅ Uploads directory created.

REM Build and start services
echo 🏗️ Building and starting services...
docker-compose -f docker-compose.dev.yml up --build -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 30 /nobreak >nul

REM Check service health
echo 🔍 Checking service health...

REM Check Faktur service
curl -f http://localhost:5001/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Faktur service is not responding
) else (
    echo ✅ Faktur service is healthy
)

REM Check Bukti Setor service
curl -f http://localhost:5002/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Bukti Setor service is not responding
) else (
    echo ✅ Bukti Setor service is healthy
)

echo.
echo 🎉 Development setup complete!
echo.
echo 📡 Services available at:
echo    - Faktur Service (Tesseract):   http://localhost:5001
echo    - Bukti Setor Service (EasyOCR): http://localhost:5002
echo    - PostgreSQL Database:          localhost:5432
echo.
echo 🔧 Useful commands:
echo    - View logs: docker-compose -f docker-compose.dev.yml logs -f
echo    - Stop services: docker-compose -f docker-compose.dev.yml down
echo    - Restart services: docker-compose -f docker-compose.dev.yml restart
echo.
echo 📖 For deployment to Railway, see RAILWAY_DEPLOYMENT.md

pause
