# 📦 Downloaded Things — What's Installed & Where

> Last updated: Feb 17, 2026 01:00 AM IST  
> **Total disk usage of `.venv/`:** ~300 MB

---

## 🐍 Python Virtual Environment (`.venv/`)

**Python version:** 3.13.12 (Homebrew)  
**Location:** `/Users/shubh/Developer/hackathon/Hack-O-Hire/.venv/`

### Core App Packages (what YOU need)

| Package | Version | Size | Purpose |
|---------|---------|------|---------|
| **streamlit** | 1.54.0 | ~30 MB | Frontend UI framework |
| **fastapi** | 0.129.0 | ~2 MB | Backend REST API |
| **uvicorn** | 0.40.0 | ~1 MB | ASGI server for FastAPI |
| **pandas** | 2.3.3 | ~50 MB | Data manipulation |
| **plotly** | 6.5.2 | ~15 MB | Interactive charts |
| **pydantic** | 2.12.5 | ~5 MB | Data validation & schemas |
| **pydantic-settings** | 2.13.0 | ~1 MB | Settings management |
| **httpx** | 0.28.1 | ~1 MB | HTTP client (frontend → backend) |
| **python-dotenv** | 1.2.1 | ~50 KB | `.env` file loader |
| **python-multipart** | 0.0.22 | ~50 KB | File upload support |

### Auto-installed Dependencies (pulled in by the above)

| Package | Pulled by | Purpose |
|---------|-----------|---------|
| numpy | pandas | Numerical computing |
| pyarrow | pandas/streamlit | Data serialization |
| pillow | streamlit | Image support |
| jinja2 | fastapi/streamlit | HTML templating |
| starlette | fastapi | ASGI framework |
| requests | streamlit | HTTP client |
| tornado | streamlit | WebSocket server |
| protobuf | streamlit | Data serialization |
| altair | streamlit | Charting library |
| gitpython | streamlit | Git integration |

---

## 🚫 NOT Installed Yet (Heavy / Optional)

These are in `backend/requirements.txt` but NOT installed in your venv. Install them only when needed:

| Package | Install Size | RAM Needed | Who Needs It | Install Command |
|---------|-------------|-----------|-------------|-----------------|
| **langchain** + community | ~20 MB | 500 MB | Dev (LLM pipeline) | `pip install langchain langchain-community langchain-ollama` |
| **chromadb** | ~100 MB | 1 GB | Dev (vector DB) | `pip install chromadb` |
| **xgboost** | ~150 MB | 500 MB | Het (ML classifier) | `pip install xgboost` |
| **scikit-learn** | ~30 MB | 200 MB | Het (ML utilities) | `pip install scikit-learn` |
| **shap** | ~50 MB | 500 MB | Het (explainability) | `pip install shap` |
| **sqlalchemy + alembic** | ~10 MB | 50 MB | Shubh (DB ORM) | `pip install sqlalchemy alembic` |
| **psycopg** | ~5 MB | 50 MB | Shubh (PostgreSQL) | `pip install "psycopg[binary]"` |
| **ollama (Python client)** | ~1 MB | N/A | Dev | `pip install ollama` |
| **fpdf2** | ~5 MB | 50 MB | Shubh (PDF export) | `pip install fpdf2` |

### 🦙 Ollama + Llama 3.1 Model

| Item | Size | RAM Needed | Where to Install |
|------|------|-----------|-----------------|
| **Ollama app** | ~500 MB | 200 MB | Dev's machine OR Docker |
| **Llama 3.1 8B model** | **~4.7 GB** | **~6 GB** | Dev's machine OR Docker |

> ⚠️ **Shubh: Do NOT install Ollama on your 8GB RAM laptop.** Use Docker (see `docker-compose.yml`) or let Dev run it on his machine. The Python client (`pip install ollama`) is tiny (~1 MB) and just talks to Ollama over HTTP — that's all you need locally.

---

## 📊 Disk Usage Summary

| Component | Size | Installed? |
|-----------|------|:---:|
| `.venv/` (core packages) | ~300 MB | ✅ Yes |
| LangChain + ChromaDB | ~120 MB | ❌ No |
| XGBoost + scikit-learn + SHAP | ~230 MB | ❌ No |
| Ollama + Llama 3.1 8B | **~5.2 GB** | ❌ No |
| **Total if everything installed** | **~5.85 GB** | — |
| **Total on YOUR machine** | **~300 MB** | ✅ |

---

## 💡 Who Installs What

| Person | What to Install | Extra Space Needed |
|--------|----------------|-------------------|
| **Shubh** | Core packages only (already done ✅) | 0 MB more |
| **Dev** | + langchain + chromadb + ollama (Docker) | ~620 MB + 4.7 GB model |
| **Siddh** | Core packages only (frontend) | ~300 MB |
| **Het** | + xgboost + scikit-learn + shap | ~230 MB |
| **Sakshi** | Nothing (docs only) | 0 MB |
