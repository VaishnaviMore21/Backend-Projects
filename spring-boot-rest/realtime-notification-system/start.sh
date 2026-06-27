#!/bin/bash

# Real-Time Notification System - Startup Script

echo "================================"
echo "Real-Time Notification System"
echo "================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker to continue."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose to continue."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if containers are already running
if [ "$(docker-compose ps -q)" ]; then
    echo "⚠️  Containers are already running"
    read -p "Do you want to restart them? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Stopping containers..."
        docker-compose down
    else
        echo "Skipping restart. Containers remain running."
        docker-compose ps
        exit 0
    fi
fi

echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📊 Service URLs:"
echo "  - Notification Service: http://localhost:8080/api"
echo "  - Kafka UI: http://localhost:8888"
echo "  - PostgreSQL: localhost:5432"
echo "  - Kafka Bootstrap: localhost:9092"
echo ""
echo "📖 API Documentation:"
echo "  - Health Check: GET http://localhost:8080/api/notifications/health"
echo "  - Send Notification: POST http://localhost:8080/api/notifications/send"
echo ""
echo "📋 View logs:"
echo "  - docker-compose logs -f notification-service"
echo "  - docker-compose logs -f kafka"
echo "  - docker-compose logs -f postgresql"
echo ""
echo "🛑 Stop services:"
echo "  - docker-compose down"
echo ""
