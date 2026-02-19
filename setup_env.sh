#!/bin/bash

# setup_env.sh — One-click setup for Hack-O-Hire environment
# Owners: Shubh & Dev

set -e  # Exit on error

echo "🚀 Starting Hack-O-Hire Environment Setup..."

# 1. Python Environment Setup
echo "🐍 Checking Python environment..."
if [ ! -d ".venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv .venv
else
    echo "   Virtual environment exists."
fi

# Activate venv
source .venv/bin/activate
echo "   Activated .venv"

# 2. Install Dependencies
echo "📦 Installing backend dependencies..."
pip install --upgrade pip
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
    echo "   ✅ Backend dependencies installed."
else
    echo "   ⚠️ backend/requirements.txt not found!"
fi

echo "📦 Installing frontend dependencies..."
if [ -f "frontend/requirements.txt" ]; then
    pip install -r frontend/requirements.txt
    echo "   ✅ Frontend dependencies installed."
else
    echo "   ⚠️ frontend/requirements.txt not found!"
fi

# 3. Ollama Setup
echo "🦙 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "   Ollama is installed."
    
    # Check if server is running
    if pgrep -x "ollama" > /dev/null; then
        echo "   Ollama server is running."
    else
        echo "   Starting Ollama server in background..."
        ollama serve &
        sleep 5  # Wait for it to start
    fi
    
    # Pull Model
    echo "   Pulling Llama 3.1 8B model (this may take a while)..."
    ollama pull llama3.1:8b
    echo "   ✅ Model ready."
else
    echo "   ❌ Ollama not found. Please install Ollama manually from https://ollama.com"
fi

# 4. Docker Setup (Skipped - Not Required for Prototype)
echo "🐳 Docker check skipped (Running in lightweight local mode)."

echo ""
echo "🎉 Setup Complete!"
echo "👉 Run './start.sh' to launch the application."
