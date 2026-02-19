#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Hack-O-Hire SAR Generator — Startup sequence initiated...${NC}"

# 1. Cleanup old processes
echo -e "${BLUE}🧹 Cleaning up ports 8000 & 8501...${NC}"
lsof -ti:8000,8501 | xargs kill -9 2>/dev/null || true

# 2. Check for Ollama (AI Model)
if command -v ollama &> /dev/null; then
    if ! pgrep -x "ollama" > /dev/null; then
        echo -e "${YELLOW}⚠️  Ollama is not running! Starting it...${NC}"
        ollama serve &
        sleep 3
    else
        echo -e "${GREEN}✅ Ollama is active.${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama command not found! AI features may not work.${NC}"
    echo -e "${YELLOW}   (Please ensure Ollama is installed and in your PATH)${NC}"
fi

# 3. Start Backend
echo -e "${BLUE}🐍 Starting Backend (Port 8000)...${NC}"
cd backend
if [ -f "../.venv/bin/python3" ]; then
    ../.venv/bin/python3 -m uvicorn app.main:app --reload --port 8000 &
else
    python3 -m uvicorn app.main:app --reload --port 8000 &
fi
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
echo "   Waiting for backend to initialize..."
sleep 5

# 4. Start Frontend
echo -e "${BLUE}🎨 Starting Frontend (Port 8501)...${NC}"
cd frontend
if [ -f "../.venv/bin/python3" ]; then
    ../.venv/bin/python3 -m streamlit run app.py --server.port 8501 &
else
    streamlit run app.py --server.port 8501 &
fi
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✅ All Systems GO!${NC}"
echo -e "   - Backend Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo -e "   - Frontend UI:  ${BLUE}http://localhost:8501${NC}"
echo -e "${RED}Press CTRL+C to stop everything.${NC}"

# Cleanup function
cleanup() {
    echo -e "\n${RED}🛑 Shutting down...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT

wait $BACKEND_PID $FRONTEND_PID
