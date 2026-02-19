"""
Data Parser — Handles CSV/JSON ingestion and normalization.

Owner: HET ONLY

Parses uploaded CSV/JSON files into CaseData format matching
the integration contracts in SAR_TODO_ROUND1.md.
"""
import io
import json
import uuid
import re
from typing import Optional

import pandas as pd


# ---------------------------------------------------------------------------
#  Column name normalization map
# ---------------------------------------------------------------------------
_COLUMN_ALIASES = {
    # txn_id
    "txn_id": "txn_id",
    "transaction_id": "txn_id",
    "trans_id": "txn_id",
    "id": "txn_id",
    # sender
    "sender": "sender",
    "sender_name": "sender",
    "originator": "sender",
    "from": "sender",
    "from_name": "sender",
    # receiver
    "receiver": "receiver",
    "receiver_name": "receiver",
    "beneficiary": "receiver",
    "to": "receiver",
    "to_name": "receiver",
    # amount
    "amount": "amount",
    "txn_amount": "amount",
    "transaction_amount": "amount",
    "value": "amount",
    # currency
    "currency": "currency",
    "ccy": "currency",
    "curr": "currency",
    # timestamp
    "timestamp": "timestamp",
    "date": "timestamp",
    "txn_date": "timestamp",
    "transaction_date": "timestamp",
    "datetime": "timestamp",
    # type
    "type": "type",
    "txn_type": "type",
    "transaction_type": "type",
    "payment_type": "type",
    "method": "type",
    # sender_account
    "sender_account": "sender_account",
    "from_account": "sender_account",
    "originator_account": "sender_account",
    # receiver_account
    "receiver_account": "receiver_account",
    "to_account": "receiver_account",
    "beneficiary_account": "receiver_account",
}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names using the alias map."""
    # Lowercase and strip whitespace
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    rename_map = {}
    for col in df.columns:
        if col in _COLUMN_ALIASES:
            rename_map[col] = _COLUMN_ALIASES[col]

    df = df.rename(columns=rename_map)
    return df


def _detect_customer(df: pd.DataFrame) -> dict:
    """Auto-detect the primary subject (most frequent receiver) as the customer."""
    customer = {
        "name": "Unknown",
        "account_id": "Unknown",
        "kyc_status": "verified",
        "business_type": None,
        "avg_monthly_volume": 0,
    }

    if "receiver" not in df.columns or df.empty:
        return customer

    # Most frequent receiver is likely the subject
    receiver_counts = df["receiver"].value_counts()
    if receiver_counts.empty:
        return customer

    primary = receiver_counts.index[0]
    customer["name"] = str(primary)

    # Try to get account ID
    if "receiver_account" in df.columns:
        accts = df.loc[df["receiver"] == primary, "receiver_account"]
        if not accts.empty:
            customer["account_id"] = str(accts.iloc[0])

    # Compute average monthly volume
    if "amount" in df.columns:
        incoming = df.loc[df["receiver"] == primary, "amount"]
        customer["avg_monthly_volume"] = round(float(incoming.sum()), 2)

    return customer


def _build_transactions(df: pd.DataFrame) -> list[dict]:
    """Convert DataFrame rows to list of transaction dicts."""
    required_cols = ["txn_id", "sender", "receiver", "amount", "timestamp"]
    transactions = []

    # Generate txn_ids if missing
    if "txn_id" not in df.columns:
        df["txn_id"] = [f"TXN-{i+1:03d}" for i in range(len(df))]

    for _, row in df.iterrows():
        txn = {
            "txn_id": str(row.get("txn_id", "")),
            "sender": str(row.get("sender", "Unknown")),
            "receiver": str(row.get("receiver", "Unknown")),
            "amount": float(row.get("amount", 0)),
            "currency": str(row.get("currency", "INR")),
            "timestamp": str(row.get("timestamp", "")),
            "type": str(row.get("type", "NEFT")),
        }
        transactions.append(txn)

    return transactions


# ---------------------------------------------------------------------------
#  Geospatial Enrichment
# ---------------------------------------------------------------------------
import random

INDIAN_CITIES_COORDS = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Ahmedabad": (23.0225, 72.5714),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Surat": (21.1702, 72.8311),
    "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873)
}

def _get_random_coords() -> tuple[float, float]:
    """Return Lat/Lon with slight jitter around a random major Indian city."""
    city = random.choice(list(INDIAN_CITIES_COORDS.keys()))
    base_lat, base_lon = INDIAN_CITIES_COORDS[city]
    # Add jitter (approx 1-5 km radius)
    lat = base_lat + random.uniform(-0.05, 0.05)
    lon = base_lon + random.uniform(-0.05, 0.05)
    return lat, lon

# ---------------------------------------------------------------------------
#  Public API
# ---------------------------------------------------------------------------

def parse_csv(file_content: bytes, filename: str) -> dict:
    """
    Parse uploaded CSV file into normalized case data format.

    Args:
        file_content: Raw bytes of the uploaded file
        filename: Name of the uploaded file

    Returns:
        Dict matching the CaseData integration contract:
        {
            "case_id": "CASE-XXX",
            "transactions": [...],
            "customer": { "name": ..., "account_id": ..., ... }
        }
    """
    try:
        df = pd.read_csv(io.BytesIO(file_content))
    except Exception as e:
        return {"error": f"Failed to read CSV: {e}"}

    if df.empty:
        return {"error": "CSV file is empty"}

    # Normalize column names
    df = _normalize_columns(df)

    # Handle missing values
    df = df.fillna("")

    # Convert amount to numeric
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    # Build output
    transactions = _build_transactions(df)
    customer = _detect_customer(df)

    # Generate a case_id from filename
    base_name = re.sub(r"[^a-zA-Z0-9]", "_", filename.replace(".csv", "")).upper()
    case_id = f"CASE-{base_name[:8]}"

    return {
        "case_id": case_id,
        "transactions": transactions,
        "customer": customer,
    }


def parse_json(file_content: bytes, filename: str = "") -> dict:
    """Parse a JSON file."""
    try:
        data = json.loads(file_content.decode("utf-8"))
        # Validate structure...
        # Inject coords if missing
        if "transactions" in data:
            for txn in data["transactions"]:
                if "lat" not in txn:
                    lat, lon = _get_random_coords()
                    txn["lat"] = lat
                    txn["lon"] = lon
        return data
    except Exception as e:
        return {"error": f"Invalid JSON: {e}"}

def parse_file(file_content: bytes, filename: str) -> dict:
    """Dispatcher."""
    if filename.endswith(".csv"):
        return parse_csv(file_content, filename)
    elif filename.endswith(".json"):
        return parse_json(file_content, filename)
    else:
        return {"error": "Unsupported file format"}
