"""
API Client — Centralized wrapper for FastAPI backend calls.
All functions return (data, error) tuples — never throw.
Falls back gracefully when backend is offline.

Owner: SIDDH ONLY
"""
import requests
import streamlit as st
from typing import Optional, Tuple, List

API_BASE = "http://localhost:8000/api"
HEALTH_URL = "http://localhost:8000/health"
TIMEOUT = 5  # seconds


# --------------------------------------------------------------------------- #
#  Health / Status
# --------------------------------------------------------------------------- #

@st.cache_data(ttl=30)
def is_backend_available():
    # type: () -> bool
    """Check if the backend is reachable (cached for 30s)."""
    try:
        r = requests.get(HEALTH_URL, timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def get_system_status():
    # type: () -> dict
    """Return component-level status for the sidebar."""
    backend_up = is_backend_available()
    return {
        "backend": backend_up,
        "ollama": backend_up,      # we infer from backend availability
        "chromadb": backend_up,
        "postgres": backend_up,
    }


# --------------------------------------------------------------------------- #
#  Upload
# --------------------------------------------------------------------------- #

def upload_file(uploaded_file):
    # type: (...) -> Tuple[Optional[dict], Optional[str]]
    """Upload a file to POST /api/upload. Returns (data, error)."""
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/octet-stream")}
        r = requests.post(f"{API_BASE}/upload", files=files, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json(), None
        else:
            return None, r.json().get("detail", f"Upload failed (HTTP {r.status_code})")
    except requests.ConnectionError:
        return None, "Backend is offline — using demo mode"
    except Exception as e:
        return None, str(e)


# --------------------------------------------------------------------------- #
#  SAR Generation
# --------------------------------------------------------------------------- #

def generate_sar(case_id):
    # type: (str) -> Tuple[Optional[dict], Optional[str]]
    """Call POST /api/generate-sar. Returns (sar_response, error)."""
    try:
        r = requests.post(f"{API_BASE}/generate-sar", json={"case_id": case_id}, timeout=60)
        if r.status_code == 200:
            return r.json(), None
        else:
            return None, r.json().get("detail", f"Generation failed (HTTP {r.status_code})")
    except requests.ConnectionError:
        return None, "Backend is offline — using demo mode"
    except Exception as e:
        return None, str(e)


# --------------------------------------------------------------------------- #
#  SAR CRUD
# --------------------------------------------------------------------------- #

def get_sar(sar_id):
    # type: (str) -> Tuple[Optional[dict], Optional[str]]
    """GET /api/sar/{sar_id}. Returns (sar_response, error)."""
    try:
        r = requests.get(f"{API_BASE}/sar/{sar_id}", timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json(), None
        else:
            return None, r.json().get("detail", f"Not found (HTTP {r.status_code})")
    except requests.ConnectionError:
        return None, "Backend is offline"
    except Exception as e:
        return None, str(e)


def update_sar(sar_id, introduction, body, conclusion):
    # type: (str, str, str, str) -> Tuple[Optional[dict], Optional[str]]
    """PUT /api/sar/{sar_id}. Returns (sar_response, error)."""
    try:
        payload = {"narrative": {"introduction": introduction, "body": body, "conclusion": conclusion}}
        r = requests.put(f"{API_BASE}/sar/{sar_id}", json=payload, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json(), None
        else:
            return None, r.json().get("detail", f"Update failed (HTTP {r.status_code})")
    except requests.ConnectionError:
        return None, "Backend is offline"
    except Exception as e:
        return None, str(e)


def approve_sar(sar_id):
    # type: (str) -> Tuple[Optional[dict], Optional[str]]
    """POST /api/sar/{sar_id}/approve. Returns (result, error)."""
    try:
        r = requests.post(f"{API_BASE}/sar/{sar_id}/approve", timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json(), None
        else:
            return None, r.json().get("detail", f"Approval failed (HTTP {r.status_code})")
    except requests.ConnectionError:
        return None, "Backend is offline"
    except Exception as e:
        return None, str(e)


# --------------------------------------------------------------------------- #
#  Cases
# --------------------------------------------------------------------------- #

def list_cases():
    # type: () -> Tuple[Optional[list], Optional[str]]
    """GET /api/cases. Returns (list_of_cases, error)."""
    try:
        r = requests.get(f"{API_BASE}/cases", timeout=TIMEOUT)
        if r.status_code == 200:
            data = r.json()
            return data.get("cases", []), None
        else:
            return None, f"Failed (HTTP {r.status_code})"
    except requests.ConnectionError:
        return None, "Backend is offline"
    except Exception as e:
        return None, str(e)


# --------------------------------------------------------------------------- #
#  Audit Trail
# --------------------------------------------------------------------------- #

def get_audit_trail(sar_id):
    # type: (str) -> Tuple[Optional[list], Optional[str]]
    """GET /api/audit/{sar_id}. Returns (audit_trail_list, error)."""
    try:
        r = requests.get(f"{API_BASE}/audit/{sar_id}", timeout=TIMEOUT)
        if r.status_code == 200:
            data = r.json()
            return data.get("audit_trail", []), None
        else:
            return None, r.json().get("detail", f"Not found (HTTP {r.status_code})")
    except requests.ConnectionError:
        return None, "Backend is offline"
    except Exception as e:
        return None, str(e)
