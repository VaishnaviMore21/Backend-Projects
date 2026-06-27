#!/bin/bash

# Build Script for Real-Time Notification System

echo "================================"
echo "Building Notification System"
echo "================================"
echo ""

# Check if Maven is installed
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven is not installed. Please install Maven to continue."
    exit 1
fi

echo "✅ Maven is installed"
echo ""

# Clean and build
echo "Running: mvn clean install"
mvn clean install

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Run: docker-compose up -d"
    echo "2. Access API: http://localhost:8080/api"
else
    echo ""
    echo "❌ Build failed!"
    exit 1
fi
