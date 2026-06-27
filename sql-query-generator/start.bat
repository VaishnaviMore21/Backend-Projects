@echo off
REM SQL Query Generator - Start Script for Windows

echo Starting SQL Query Generator...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo Building Docker images...
docker-compose build
if errorlevel 1 (
    echo Error building images
    pause
    exit /b 1
)

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak

echo.
echo Checking PostgreSQL...
docker-compose exec -T postgres pg_isready -U sqlgen

echo.
echo Checking Ollama...
timeout /t 5 /nobreak

echo.
echo Pulling Ollama model (mistral)...
docker-compose exec ollama ollama pull mistral

echo.
echo All services are running!
echo.
echo Access the application:
echo   Web UI: http://localhost:5000
echo   API: http://localhost:5000/api
echo.
echo PostgreSQL:
echo   Host: localhost:5432
echo   Username: sqlgen
echo   Password: SecurePassword123!
echo   Database: business_db
echo.
echo Ollama:
echo   URL: http://localhost:11434
echo   Model: mistral
echo.
echo To view logs:
echo   docker-compose logs -f app
echo.
echo To stop all services:
echo   docker-compose down
echo.
pause
