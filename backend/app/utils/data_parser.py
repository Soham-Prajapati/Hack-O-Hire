"""
Data Parser — Handles CSV/JSON ingestion and normalization.

Owner: P4
"""
import json
from typing import Optional


def parse_csv(file_content: bytes, filename: str) -> dict:
    """
    Parse uploaded CSV file into normalized case data format.

    Expected CSV columns: txn_id, sender, receiver, amount, currency, timestamp, type

    Args:
        file_content: Raw bytes of the uploaded file
        filename: Name of the uploaded file

    Returns:
        Dict matching the CaseData schema (see schemas.py)

    TODO (P4):
    1. Use pandas to read CSV from bytes
    2. Normalize column names (handle variations)
    3. Extract unique customer info
    4. Return structured CaseData dict
    """
    # Placeholder — P4 implements this
    return {
        "case_id": None,
        "transactions": [],
        "customer": {
            "name": "Unknown",
            "account_id": "Unknown",
            "kyc_status": "pending",
        },
    }


def parse_json(file_content: bytes, filename: str) -> dict:
    """
    Parse uploaded JSON file into normalized case data format.

    Args:
        file_content: Raw bytes of the uploaded file
        filename: Name of the uploaded file

    Returns:
        Dict matching the CaseData schema
    """
    try:
        data = json.loads(file_content.decode("utf-8"))
        return data
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}


def parse_file(file_content: bytes, filename: str) -> dict:
    """Parse a file based on its extension."""
    if filename.endswith(".csv"):
        return parse_csv(file_content, filename)
    elif filename.endswith(".json"):
        return parse_json(file_content, filename)
    else:
        return {"error": f"Unsupported file format: {filename}"}
