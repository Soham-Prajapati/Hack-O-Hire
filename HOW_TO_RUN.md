# 🚀 How to Run — SAR Narrative Generator

## 🧠 How Does This App Work? (Read This First)

This app has **2 separate servers** that talk to each other:

```
┌──────────────────────┐        HTTP        ┌──────────────────────┐
│   FRONTEND (Streamlit)│  ───────────────►  │   BACKEND (FastAPI)  │
│   localhost:8501      │  ◄───────────────  │   localhost:8000     │
│                       │    JSON requests   │                      │
│  • UI / Dashboard     │                    │  • API endpoints     │
│  • SAR Editor         │                    │  • LLM calls         │
│  • Audit Trail viewer │                    │  • Data processing   │
└──────────────────────┘                     └──────────────────────┘
                                                      │
                                                      │ HTTP
                                                      ▼
                                             ┌──────────────────┐
                                             │  OLLAMA (Docker)  │
                                             │  localhost:11434  │
                                             │  Llama 3.1 8B    │
                                             └──────────────────┘
```

**You need 2 terminals open** — one for frontend, one for backend.  
Right now, the frontend has **mock data hardcoded**, so it works even WITHOUT the backend.

---

## Quick Start

### Mac / Linux

```bash
# 1. Clone & setup
git clone https://github.com/Soham-Prajapati/Hack-O-Hire.git
cd Hack-O-Hire
chmod +x setup.sh
./setup.sh shubh    # Replace with your name: shubh/dev/siddh/het/sakshi
```

### Windows

```cmd
git clone https://github.com/Soham-Prajapati/Hack-O-Hire.git
cd Hack-O-Hire
setup.bat shubh     # Replace with your name: shubh/dev/siddh/het/sakshi
```

> ⚠️ Windows users: make sure Python 3.13+ is installed and added to PATH.  
> Download from https://www.python.org/downloads/ — check "Add to PATH" during install.

---

## Running the App (Day-to-Day)

### Terminal 1 — Frontend (what users see)

**Mac/Linux:**
```bash
source .venv/bin/activate
cd frontend
streamlit run app.py
# Opens http://localhost:8501
```

**Windows:**
```cmd
.venv\Scripts\activate.bat
cd frontend
streamlit run app.py
```

### Terminal 2 — Backend API (data processing)

**Mac/Linux:**
```bash
source .venv/bin/activate
cd backend
uvicorn app.main:app --reload --port 8000
# API docs at http://localhost:8000/docs
```

**Windows:**
```cmd
.venv\Scripts\activate.bat
cd backend
uvicorn app.main:app --reload --port 8000
```

### Can I run just the frontend without backend?

**YES!** Right now the frontend uses hardcoded mock data. It's fully demo-able standalone:

```bash
source .venv/bin/activate          # Mac
# .venv\Scripts\activate.bat      # Windows
cd frontend && streamlit run app.py
```

Once we integrate the backend, the frontend will call `http://localhost:8000/api/...` — but for now, mock data makes it self-contained.

---

## 🦙 Ollama Setup (Docker — Recommended)

Do NOT install Ollama directly on an 8GB RAM machine. Use Docker instead:

```bash
# Start Ollama container
docker-compose up -d ollama

# Download the model (one-time, ~4.7 GB)
docker exec sargen_ollama ollama pull llama3.1:8b

# Test it works
curl http://localhost:11434/api/generate -d '{"model":"llama3.1:8b","prompt":"Hello"}'

# Stop when done
docker-compose stop ollama
```

The model is stored in a Docker volume — survives container restarts, doesn't eat your disk.

### If Dev is running Ollama on his machine

Update your `.env` file:
```
OLLAMA_BASE_URL=http://<dev-ip-address>:11434
```

Then both frontend and backend on YOUR laptop will talk to Dev's Ollama over the network.

---

## 🐘 PostgreSQL (Optional)

Not needed for prototype — we use in-memory storage. But if you want it:

```bash
docker-compose up -d postgres
# Connection: postgresql://sargen:sargen_password@localhost:5432/sargen_db
```

---

## 📂 Who Runs What

| Person | What to Run | Terminal Commands |
|--------|------------|-------------------|
| **Shubh** | Backend + Frontend | Terminal 1: `streamlit run app.py` · Terminal 2: `uvicorn app.main:app --reload` |
| **Dev** | Ollama (Docker) | `docker-compose up -d ollama` then test with curl |
| **Siddh** | Frontend only | `cd frontend && streamlit run app.py` |
| **Het** | ML scripts | `python ml_models/typology_classifier.py` |
| **Sakshi** | Nothing | Work on docs/PPT |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `python` not found (Windows) | Install Python 3.13+ from python.org, check "Add to PATH" |
| `command not found: python3` (Mac) | `brew install python@3.13` |
| `psycopg` build fails | Already fixed — we use `psycopg[binary]` |
| ChromaDB crashes | Use Python 3.13, not 3.14 (too new for ChromaDB) |
| Ollama out of memory | Use Docker or run on a 16GB+ RAM machine |
| Port 8501 already in use | `streamlit run app.py --server.port 8502` |
| Port 8000 already in use | `uvicorn app.main:app --port 8001` |
| `setup.sh` permission denied | `chmod +x setup.sh` (Mac/Linux only) |
| Windows: `setup.sh` doesn't work | Use `setup.bat shubh` instead |
