#!/bin/bash

echo "🚀 Setting up the environment..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Build Docker containers
echo "🐳 Building Docker containers..."
docker-compose build

echo "✅ Setup complete! Run 'docker-compose up -d' to start the system."