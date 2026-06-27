#!/bin/bash

# SQL Query Generator - Start Script

echo "🚀 Starting SQL Query Generator..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "📦 Building Docker images..."
docker-compose build

echo ""
echo "🌐 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Wait for PostgreSQL to be ready
echo "📊 Checking PostgreSQL..."
docker-compose exec -T postgres pg_isready -U sqlgen

# Wait for Ollama to be ready
echo "🤖 Checking Ollama..."
sleep 5

echo ""
echo "📥 Pulling Ollama model (mistral)..."
docker-compose exec ollama ollama pull mistral

echo ""
echo "✅ All services are running!"
echo ""
echo "🔗 Access the application:"
echo "   Web UI: http://localhost:5000"
echo "   API: http://localhost:5000/api"
echo ""
echo "📊 Access PostgreSQL:"
echo "   Host: localhost:5432"
echo "   Username: sqlgen"
echo "   Password: SecurePassword123!"
echo "   Database: business_db"
echo ""
echo "🤖 Ollama:"
echo "   URL: http://localhost:11434"
echo "   Model: mistral"
echo ""
echo "📋 View logs:"
echo "   docker-compose logs -f app"
echo ""
echo "🛑 To stop all services:"
echo "   docker-compose down"
echo ""
