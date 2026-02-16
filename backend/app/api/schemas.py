"""
Pydantic models for API request/response schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# --- Enums ---

class SARStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    REJECTED = "rejected"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# --- Transaction & Customer Models ---

class Transaction(BaseModel):
    txn_id: str
    sender: str
    receiver: str
    amount: float
    currency: str = "INR"
    timestamp: str
    type: str = "NEFT"


class Customer(BaseModel):
    name: str
    account_id: str
    kyc_status: str = "verified"
    business_type: Optional[str] = None
    avg_monthly_volume: Optional[float] = None


class CaseData(BaseModel):
    case_id: Optional[str] = None
    transactions: list[Transaction]
    customer: Customer


# --- SAR Narrative Models ---

class SARNarrative(BaseModel):
    introduction: str
    body: str
    conclusion: str


class AuditStep(BaseModel):
    step: int
    agent: str
    action: str
    data_points_used: list[str] = []
    rules_matched: list[str] = []
    output: str
    timestamp: Optional[str] = None


class QualityScore(BaseModel):
    completeness: float = 0.0
    compliance: float = 0.0
    readability: float = 0.0
    evidence_linkage: float = 0.0


class TypologyResult(BaseModel):
    prediction: str
    confidence: float
    top_features: dict[str, float] = {}


class SARResponse(BaseModel):
    sar_id: str
    case_id: str
    narrative: SARNarrative
    audit_trail: list[AuditStep] = []
    quality_score: QualityScore
    typology: Optional[TypologyResult] = None
    status: SARStatus = SARStatus.DRAFT
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


# --- API Request/Response Models ---

class GenerateSARRequest(BaseModel):
    case_id: str


class UpdateSARRequest(BaseModel):
    narrative: SARNarrative


class CaseListItem(BaseModel):
    case_id: str
    customer_name: str
    alert_type: str = "Suspicious Transaction"
    risk_level: RiskLevel = RiskLevel.MEDIUM
    sar_status: SARStatus = SARStatus.DRAFT
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class CaseListResponse(BaseModel):
    cases: list[CaseListItem]
    total: int
