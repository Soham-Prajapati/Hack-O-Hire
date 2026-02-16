"""
Audit Logger — Captures every step of SAR generation for explainability.

Owner: P2
"""
from datetime import datetime


class AuditLogger:
    """
    Logs every step of the multi-agent SAR generation pipeline.

    Captures: input_data → prompt → retrieved_context → llm_response → reasoning

    TODO (P2):
    - Implement as LangChain CallbackHandler
    - Store entries in PostgreSQL audit_logs table
    - Generate reasoning traces with data provenance
    """

    def __init__(self):
        self.entries: list[dict] = []

    def log_step(
        self,
        step: int,
        agent: str,
        action: str,
        data_points_used: list[str] = None,
        rules_matched: list[str] = None,
        output: str = "",
    ) -> dict:
        """Log a single step in the SAR generation pipeline."""
        entry = {
            "step": step,
            "agent": agent,
            "action": action,
            "data_points_used": data_points_used or [],
            "rules_matched": rules_matched or [],
            "output": output,
            "timestamp": datetime.now().isoformat(),
        }
        self.entries.append(entry)
        return entry

    def get_trail(self) -> list[dict]:
        """Return the complete audit trail."""
        return self.entries

    def clear(self):
        """Reset the audit trail for a new SAR generation."""
        self.entries = []
