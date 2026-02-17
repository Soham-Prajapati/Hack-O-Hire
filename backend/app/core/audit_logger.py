"""
Audit Logger — Captures every step of SAR generation for explainability.

Owner: P2
"""
from datetime import datetime
from typing import Any
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult


class AuditLogger(BaseCallbackHandler):
    """
    Logs every step of the multi-agent SAR generation pipeline.
    Captures: input_data → prompt → retrieved_context → llm_response → reasoning
    """

    def __init__(self):
        super().__init__()
        self.entries: list[dict] = []
        self.current_step = 0

    def log_step(
        self,
        step: int,
        agent: str,
        action: str,
        data_points_used: list[str] = None,
        rules_matched: list[str] = None,
        output: str = "",
    ) -> dict:
        """Log a single step explicitly."""
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

    def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        self.current_step += 1
        self.log_step(
            step=self.current_step,
            agent="LLM Engine",
            action="Prompting Model",
            output=prompts[0] if prompts else "No prompt captured"
        )

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        self.current_step += 1
        text = response.generations[0][0].text
        self.log_step(
            step=self.current_step,
            agent="LLM Engine",
            action="Generated Response",
            output=text[:500] + "..." if len(text) > 500 else text
        )

    def on_chain_start(
        self, serialized: dict[str, Any], inputs: dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""
        pass

    def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        pass

    def get_trail(self) -> list[dict]:
        """Return the complete audit trail."""
        return self.entries

    def clear(self):
        """Reset the audit trail for a new SAR generation."""
        self.entries = []
        self.current_step = 0

