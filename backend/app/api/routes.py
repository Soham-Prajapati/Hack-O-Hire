"""
API Routes — SAR Narrative Generator
Owner: SHUBH ONLY

Wires together:
  - Het's data_parser.parse_file()      → upload endpoint
  - Dev's LLMEngine.generate_sar()      → generate endpoint
  - Het's TypologyClassifier.predict()  → generate endpoint (typology)
"""
import uuid
import sys
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.schemas import (
    CaseData,
    SARResponse,
    SARNarrative,
    SARStatus,
    GenerateSARRequest,
    UpdateSARRequest,
    CaseListItem,
    CaseListResponse,
    AuditStep,
    QualityScore,
    TypologyResult,
    RiskLevel,
    UploadResponse,
)
from datetime import datetime

# --- Ensure ml_models is importable ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

router = APIRouter()

# In-memory storage (will be replaced with PostgreSQL later)
cases_store: dict[str, dict] = {}       # case_id → parsed case data dict
sars_store: dict[str, SARResponse] = {}  # sar_id  → SARResponse
case_to_sar: dict[str, str] = {}         # case_id → sar_id  (quick lookup)

# --------------------------------------------------------------------------- #
#  Lazy-initialized singletons for LLM + ML (avoids import failures at boot)
# --------------------------------------------------------------------------- #
_llm_engine = None
_typology_classifier = None


def _get_llm_engine():
    """Lazily initialize the LLM engine (Dev's module)."""
    global _llm_engine
    if _llm_engine is None:
        try:
            from app.core.llm_engine import LLMEngine
            _llm_engine = LLMEngine()
        except Exception as e:
            print(f"[WARN] Could not load LLMEngine: {e}")
            _llm_engine = None
    return _llm_engine


def _get_typology_classifier():
    """Lazily initialize the typology classifier (Het's module)."""
    global _typology_classifier
    if _typology_classifier is None:
        try:
            from ml_models.typology_classifier import TypologyClassifier
            _typology_classifier = TypologyClassifier()
        except Exception as e:
            print(f"[WARN] Could not load TypologyClassifier: {e}")
            _typology_classifier = None
    return _typology_classifier


# =========================================================================== #
#  1. UPLOAD — Parse CSV/JSON via Het's data_parser
# =========================================================================== #

@router.post("/upload", response_model=UploadResponse, tags=["Data"])
async def upload_data(file: UploadFile = File(...)):
    """Upload transaction/customer data (CSV or JSON).

    Uses Het's data_parser to parse the file into the CaseData format defined
    in the integration contracts.
    """
    if not file.filename.endswith((".csv", ".json")):
        raise HTTPException(status_code=400, detail="Only CSV and JSON files are supported")

    content = await file.read()
    case_id = f"CASE-{uuid.uuid4().hex[:6].upper()}"

    # --- Parse using Het's data parser ---
    try:
        from app.utils.data_parser import parse_file
        parsed = parse_file(content, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse file: {e}")

    if "error" in parsed:
        raise HTTPException(status_code=400, detail=parsed["error"])

    # Assign case_id
    parsed["case_id"] = case_id
    parsed["filename"] = file.filename
    parsed["uploaded_at"] = datetime.now().isoformat()

    # Store parsed case data
    cases_store[case_id] = parsed

    transactions = parsed.get("transactions", [])
    customer = parsed.get("customer", {})
    customer_name = customer.get("name", "Unknown") if isinstance(customer, dict) else "Unknown"

    return UploadResponse(
        case_id=case_id,
        filename=file.filename,
        status="uploaded",
        message=f"Data uploaded successfully. {len(transactions)} transactions parsed.",
        transaction_count=len(transactions),
        customer_name=customer_name,
    )


# =========================================================================== #
#  2. GENERATE SAR — LLMEngine + TypologyClassifier
# =========================================================================== #

@router.post("/generate-sar", response_model=SARResponse, tags=["SAR"])
async def generate_sar(request: GenerateSARRequest):
    """Generate a SAR narrative for a given case.

    Pipeline:
      1. Look up parsed case data
      2. Run Het's TypologyClassifier.predict()
      3. Call Dev's LLMEngine.generate_sar()
      4. Bundle into SARResponse
    """
    case_id = request.case_id

    # --- Fetch case data ---
    if case_id not in cases_store:
        raise HTTPException(
            status_code=404,
            detail=f"Case {case_id} not found. Upload data first via POST /api/upload.",
        )

    case_data = cases_store[case_id]
    transactions = case_data.get("transactions", [])

    sar_id = f"SAR-{uuid.uuid4().hex[:6].upper()}"

    # --- Step 1: Typology prediction (Het's classifier) ---
    typology_result = None
    classifier = _get_typology_classifier()
    if classifier:
        try:
            tp = classifier.predict(transactions)
            typology_result = TypologyResult(
                prediction=tp.get("typology", "unknown"),
                confidence=tp.get("confidence", 0.0),
                top_features=tp.get("top_features", {}),
            )
        except Exception as e:
            print(f"[WARN] Typology prediction failed: {e}")

    # --- Step 2: SAR generation (Dev's LLM engine) ---
    llm = _get_llm_engine()
    narrative = SARNarrative(
        introduction="[LLM engine not connected — placeholder narrative]",
        body="[Transaction analysis pending LLM integration]",
        conclusion="[Summary pending LLM integration]",
    )
    audit_trail = []
    quality = QualityScore()

    if llm:
        try:
            result = await llm.generate_sar(case_data)

            # Parse narrative
            narr = result.get("narrative", {})
            if isinstance(narr, dict):
                narrative = SARNarrative(
                    introduction=narr.get("introduction", narrative.introduction),
                    body=narr.get("body", narrative.body),
                    conclusion=narr.get("conclusion", narrative.conclusion),
                )

            # Parse audit trail
            raw_trail = result.get("audit_trail", [])
            for i, step in enumerate(raw_trail):
                audit_trail.append(AuditStep(
                    step=step.get("step", i + 1),
                    agent=step.get("agent", "unknown"),
                    action=step.get("action", ""),
                    data_points_used=step.get("data_points_used", []),
                    rules_matched=step.get("rules_matched", []),
                    output=step.get("output", ""),
                    timestamp=step.get("timestamp", datetime.now().isoformat()),
                ))

            # Parse quality score
            qs = result.get("quality_score", {})
            if isinstance(qs, dict):
                quality = QualityScore(
                    completeness=qs.get("completeness", 0.0),
                    compliance=qs.get("compliance", 0.0),
                    readability=qs.get("readability", 0.0),
                    evidence_linkage=qs.get("evidence_linkage", 0.0),
                )

            # If LLM returned typology and we don't have one yet, use it
            if not typology_result and result.get("typology"):
                tp = result["typology"]
                typology_result = TypologyResult(
                    prediction=tp.get("prediction", "unknown"),
                    confidence=tp.get("confidence", 0.0),
                    top_features=tp.get("top_features", {}),
                )

        except Exception as e:
            print(f"[WARN] LLM generation failed: {e}")
            # Add a fallback audit step recording the failure
            audit_trail.append(AuditStep(
                step=1,
                agent="system",
                action=f"LLM generation failed: {e}",
                data_points_used=[],
                rules_matched=[],
                output="Falling back to placeholder narrative",
                timestamp=datetime.now().isoformat(),
            ))

    # If no audit trail at all, add a placeholder step
    if not audit_trail:
        audit_trail.append(AuditStep(
            step=1,
            agent="system",
            action="SAR generated (LLM engine returning placeholder data)",
            data_points_used=[],
            rules_matched=[],
            output="Awaiting full LLM integration from Dev",
            timestamp=datetime.now().isoformat(),
        ))

    # --- Build SARResponse ---
    sar = SARResponse(
        sar_id=sar_id,
        case_id=case_id,
        narrative=narrative,
        audit_trail=audit_trail,
        quality_score=quality,
        typology=typology_result,
        status=SARStatus.DRAFT,
    )

    sars_store[sar_id] = sar
    case_to_sar[case_id] = sar_id
    return sar


# =========================================================================== #
#  3. GET SAR + AUDIT TRAIL
# =========================================================================== #

@router.get("/sar/{sar_id}", response_model=SARResponse, tags=["SAR"])
async def get_sar(sar_id: str):
    """Get a SAR narrative and its audit trail."""
    if sar_id not in sars_store:
        raise HTTPException(status_code=404, detail=f"SAR {sar_id} not found")
    return sars_store[sar_id]


# =========================================================================== #
#  4. UPDATE SAR — with diff tracking
# =========================================================================== #

@router.put("/sar/{sar_id}", response_model=SARResponse, tags=["SAR"])
async def update_sar(sar_id: str, request: UpdateSARRequest):
    """Update/edit a SAR narrative (analyst edits).

    Tracks the old→new diff as an audit trail entry so every edit is recorded.
    """
    if sar_id not in sars_store:
        raise HTTPException(status_code=404, detail=f"SAR {sar_id} not found")

    sar = sars_store[sar_id]
    old_narrative = sar.narrative

    # Record the edit diff in audit trail
    diff_summary = []
    if old_narrative.introduction != request.narrative.introduction:
        diff_summary.append("introduction edited")
    if old_narrative.body != request.narrative.body:
        diff_summary.append("body edited")
    if old_narrative.conclusion != request.narrative.conclusion:
        diff_summary.append("conclusion edited")

    if diff_summary:
        sar.audit_trail.append(AuditStep(
            step=len(sar.audit_trail) + 1,
            agent="analyst",
            action=f"Manual narrative edit: {', '.join(diff_summary)}",
            data_points_used=[],
            rules_matched=[],
            output=f"Sections modified: {', '.join(diff_summary)}",
            timestamp=datetime.now().isoformat(),
        ))

    sar.narrative = request.narrative
    sar.status = SARStatus.REVIEW
    sars_store[sar_id] = sar
    return sar


# =========================================================================== #
#  5. APPROVE SAR
# =========================================================================== #

@router.post("/sar/{sar_id}/approve", tags=["SAR"])
async def approve_sar(sar_id: str):
    """Approve a SAR narrative. Records approval in the audit trail."""
    if sar_id not in sars_store:
        raise HTTPException(status_code=404, detail=f"SAR {sar_id} not found")

    sar = sars_store[sar_id]

    # Add audit step for approval
    sar.audit_trail.append(AuditStep(
        step=len(sar.audit_trail) + 1,
        agent="analyst",
        action="SAR approved for filing",
        data_points_used=[],
        rules_matched=[],
        output="Status changed from '{}' to 'approved'".format(sar.status.value),
        timestamp=datetime.now().isoformat(),
    ))

    sar.status = SARStatus.APPROVED
    sars_store[sar_id] = sar
    return {"sar_id": sar_id, "status": "approved", "message": "SAR approved successfully"}


# =========================================================================== #
#  6. LIST CASES — with real data from parsed uploads
# =========================================================================== #

@router.get("/cases", response_model=CaseListResponse, tags=["Cases"])
async def list_cases():
    """List all uploaded cases with their current SAR status."""
    items = []
    for cid, data in cases_store.items():
        # Pull customer name from parsed data
        customer = data.get("customer", {})
        customer_name = customer.get("name", data.get("filename", "Unknown")) if isinstance(customer, dict) else data.get("filename", "Unknown")

        # Check if a SAR exists for this case
        sar_status = SARStatus.DRAFT
        if cid in case_to_sar:
            sar_id = case_to_sar[cid]
            if sar_id in sars_store:
                sar_status = sars_store[sar_id].status

        items.append(CaseListItem(
            case_id=cid,
            customer_name=customer_name,
            alert_type="Suspicious Transaction",
            risk_level=RiskLevel.MEDIUM,
            sar_status=sar_status,
            created_at=data.get("uploaded_at", datetime.now().isoformat()),
        ))

    return CaseListResponse(cases=items, total=len(items))


# =========================================================================== #
#  7. AUDIT TRAIL endpoint
# =========================================================================== #

@router.get("/audit/{sar_id}", tags=["Audit"])
async def get_audit_trail(sar_id: str):
    """Get the full audit trail for a SAR."""
    if sar_id not in sars_store:
        raise HTTPException(status_code=404, detail=f"SAR {sar_id} not found")
    return {"sar_id": sar_id, "audit_trail": sars_store[sar_id].audit_trail}
