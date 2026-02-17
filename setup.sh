#!/usr/bin/env bash
# ============================================================
# SAR Narrative Generator — One-Command Setup Script
# ============================================================
# Usage:    ./setup.sh [role]
#
# Roles:
#   shubh   - Core + Backend (FastAPI, SQLAlchemy, PostgreSQL)
#   dev     - Core + LLM/RAG (LangChain, ChromaDB, Ollama client)
#   siddh   - Core only (Streamlit frontend)
#   het     - Core + ML (XGBoost, scikit-learn, SHAP)
#   sakshi  - Nothing to install (docs only)
#   all     - Everything except Ollama model
#
# After install, your personal install log is saved at:
#   setup_logs/<your-name>_installed.md
# ============================================================

set -e

ROLE="${1:-shubh}"
VENV_DIR=".venv"
PYTHON_CMD="python3"
LOG_DIR="setup_logs"
LOG_FILE="$LOG_DIR/${ROLE}_installed.md"

# Capitalize first letter (zsh-compatible)
ROLE_CAP="$(echo "$ROLE" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')"

echo ""
echo "🏦 SAR Narrative Generator — Setup"
echo "==================================="
echo "Role: $ROLE_CAP"
echo ""

# --- Step 1: Create venv ---
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo "✅ Virtual environment created at $VENV_DIR/"
else
    echo "✅ Virtual environment already exists at $VENV_DIR/"
fi

# Activate
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
PYTHON_VER="$(python --version 2>&1)"
echo "🐍 $PYTHON_VER"

# --- Step 2: Upgrade pip ---
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q

# --- Step 3: Install core packages (everyone needs these) ---
CORE_PACKAGES="streamlit fastapi uvicorn pandas plotly python-dotenv python-multipart httpx pydantic pydantic-settings networkx"

echo ""
echo "📥 Installing core packages (Streamlit + FastAPI + Pandas)..."
pip install $CORE_PACKAGES -q
echo "✅ Core packages installed"

ROLE_PACKAGES=""
ROLE_DESCRIPTION=""
NOT_INSTALLED=""

# --- Step 4: Role-specific packages ---
case "$ROLE" in
    shubh)
        ROLE_PACKAGES="sqlalchemy alembic psycopg[binary] fpdf2"
        ROLE_DESCRIPTION="Backend + AI Integration Lead (FastAPI, SQLAlchemy, PostgreSQL)"
        NOT_INSTALLED="- langchain, chromadb, ollama (Dev)
- xgboost, scikit-learn, shap (Het)
- Ollama app + Llama 3.1 8B model (~4.7 GB)"
        echo ""
        echo "📥 Installing Shubh's packages (Backend + DB)..."
        pip install sqlalchemy alembic "psycopg[binary]" fpdf2 -q
        echo "✅ Backend packages installed"
        ;;
    dev)
        ROLE_PACKAGES="langchain langchain-community langchain-ollama chromadb ollama"
        ROLE_DESCRIPTION="LLM/RAG + AI Core Lead (Ollama, LangChain, ChromaDB)"
        NOT_INSTALLED="- sqlalchemy, alembic, psycopg, fpdf2 (Shubh)
- xgboost, scikit-learn, shap (Het)
- Ollama + Llama 3.1 model: use docker-compose up -d ollama"
        echo ""
        echo "📥 Installing Dev's packages (LLM + RAG)..."
        pip install $ROLE_PACKAGES -q
        echo "✅ LLM/RAG packages installed"
        echo ""
        echo "⚠️  To set up Ollama with Docker:"
        echo "   docker-compose up -d ollama"
        echo "   docker exec sargen_ollama ollama pull llama3.1:8b"
        ;;
    siddh)
        ROLE_DESCRIPTION="Frontend Lead (Streamlit UI)"
        NOT_INSTALLED="- sqlalchemy, psycopg, fpdf2 (Shubh)
- langchain, chromadb, ollama (Dev)
- xgboost, scikit-learn, shap (Het)
- Ollama app + Llama 3.1 8B model"
        echo ""
        echo "ℹ️  Siddh (Frontend) — core packages are all you need!"
        ;;
    het)
        ROLE_PACKAGES="xgboost scikit-learn shap joblib"
        ROLE_DESCRIPTION="Data & ML Engineer (XGBoost, SHAP, datasets)"
        NOT_INSTALLED="- sqlalchemy, psycopg, fpdf2 (Shubh)
- langchain, chromadb, ollama (Dev)
- Ollama app + Llama 3.1 8B model"
        echo ""
        echo "📥 Installing Het's packages (ML + Data)..."
        pip install $ROLE_PACKAGES -q
        echo "✅ ML packages installed"
        ;;
    sakshi)
        ROLE_DESCRIPTION="Docs, PPT & Submission Lead"
        NOT_INSTALLED="- All Python packages (docs role only)"
        echo ""
        echo "ℹ️  Sakshi (Docs) — no Python packages needed!"
        echo "   Just work on the submission doc and PPT."
        ;;
    all)
        ROLE_DESCRIPTION="Full install (all packages)"
        NOT_INSTALLED="- Ollama app + Llama 3.1 8B model (use Docker)"
        echo ""
        echo "📥 Installing ALL packages..."
        pip install -r backend/requirements.txt -r frontend/requirements.txt -q
        echo "✅ All packages installed"
        ;;
    *)
        echo "❌ Unknown role: $ROLE"
        echo "   Valid roles: shubh, dev, siddh, het, sakshi, all"
        exit 1
        ;;
esac

# --- Step 5: Create directories ---
echo ""
echo "📁 Ensuring project directories exist..."
mkdir -p data/sample_data screenshots ml_models backend/knowledge_base/sar_templates backend/knowledge_base/regulations "$LOG_DIR"

# --- Step 6: Copy .env ---
if [ ! -f ".env" ]; then
    cp .env.example .env 2>/dev/null && echo "✅ .env created from .env.example" || true
fi

# --- Step 7: Generate per-person install log ---
echo ""
echo "📝 Generating your personal install log → $LOG_FILE"

VENV_SIZE="$(du -sh "$VENV_DIR" 2>/dev/null | cut -f1)"
SETUP_TIME="$(date '+%Y-%m-%d %I:%M %p %Z')"
MACHINE_HOST="$(hostname)"
OS_INFO="$(uname -srm)"
PIP_FREEZE="$(pip freeze 2>/dev/null)"
PACKAGE_COUNT="$(echo "$PIP_FREEZE" | wc -l | tr -d ' ')"

{
echo "# Install Log — $ROLE_CAP"
echo ""
echo "> **Auto-generated by \`setup.sh\`** — do not edit manually."
echo "> Re-run \`./setup.sh $ROLE\` to update this file."
echo ""
echo "| Field | Value |"
echo "|-------|-------|"
echo "| **Person** | $ROLE_CAP |"
echo "| **Role** | $ROLE_DESCRIPTION |"
echo "| **Setup Date** | $SETUP_TIME |"
echo "| **Machine** | $MACHINE_HOST |"
echo "| **OS** | $OS_INFO |"
echo "| **Python** | $PYTHON_VER |"
echo "| **Venv Path** | \`.venv/\` |"
echo "| **Venv Size** | $VENV_SIZE |"
echo "| **Total Packages** | $PACKAGE_COUNT |"
echo ""
echo "---"
echo ""
echo "## Core Packages (shared by everyone)"
echo ""
echo "\`\`\`"
echo "$CORE_PACKAGES" | tr ' ' '\n'
echo "\`\`\`"
echo ""
echo "## Role-Specific Packages"
echo ""
echo "\`\`\`"
if [ -n "$ROLE_PACKAGES" ]; then
    echo "$ROLE_PACKAGES" | tr ' ' '\n'
else
    echo "(none — core only)"
fi
echo "\`\`\`"
echo ""
echo "## NOT Installed (other roles' packages)"
echo ""
echo "$NOT_INSTALLED"
echo ""
echo "---"
echo ""
echo "## Full Package List (\`pip freeze\`)"
echo ""
echo "\`\`\`"
echo "$PIP_FREEZE"
echo "\`\`\`"
} > "$LOG_FILE"

echo "✅ Install log saved to $LOG_FILE"

# --- Summary ---
echo ""
echo "==================================="
echo "🎉 Setup complete for $ROLE_CAP!"
echo "==================================="
echo ""
echo "📄 Your install log:  $LOG_FILE"
echo ""
echo "To run the app:"
echo "  source .venv/bin/activate"
echo "  cd frontend && streamlit run app.py"
echo ""
echo "To run the backend API:"
echo "  source .venv/bin/activate"
echo "  cd backend && uvicorn app.main:app --reload --port 8000"
echo ""
echo "To start Ollama via Docker:"
echo "  docker-compose up -d ollama"
echo ""
