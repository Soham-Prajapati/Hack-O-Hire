"""
LLM Engine — Ollama + Llama 3.1 8B integration for SAR narrative generation.

Owner: P2
"""
from typing import Optional


# SAR generation system prompt
SAR_SYSTEM_PROMPT = """You are an expert financial compliance officer specializing in writing Suspicious Activity Reports (SARs) for banking institutions. You generate clear, concise, and regulator-ready SAR narratives following FinCEN guidelines.

## Output Format
Always structure the SAR narrative in three sections:

### INTRODUCTION
- Brief statement of the SAR's purpose
- Type of suspicious activity being reported
- Reference to any previously filed SARs on the subject
- Internal investigation reference number

### BODY (Address all 5Ws + How)
- **WHO:** Identify the individuals/entities involved, account details, customer history
- **WHAT:** Describe the specific transactions/behaviors that are suspicious
- **WHEN:** Dates and timeframes of the suspicious activity
- **WHERE:** Locations, branches, jurisdictions involved
- **WHY:** Explain why the activity is suspicious given the customer's profile
- **HOW:** Detail the method of operation used

### CONCLUSION
- Summary of findings
- Actions taken or planned by the institution
- Contact information for follow-up
- Reference to supporting documentation

## Rules
- Be factual and objective — only state what the data shows
- Do NOT speculate beyond what the evidence supports
- Use professional, regulatory language
- Do NOT discriminate based on nationality, ethnicity, or religion
- Every claim must be traceable to specific data points
- Keep the narrative concise but comprehensive
"""


class LLMEngine:
    """Wrapper for Ollama LLM calls with audit trail support."""

    def __init__(self, model: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.system_prompt = SAR_SYSTEM_PROMPT

    async def generate_sar(self, case_data: dict) -> dict:
        """
        Generate a SAR narrative from case data.

        Args:
            case_data: Dict with 'transactions' and 'customer' keys

        Returns:
            Dict with 'narrative', 'audit_trail', 'quality_score', 'typology'
        """
        # TODO: Implement actual Ollama call with LangChain
        # TODO: Integrate RAG pipeline for context retrieval
        # TODO: Add audit trail callback logging

        return {
            "narrative": {
                "introduction": "[Placeholder — connect Ollama to generate]",
                "body": "[Placeholder — LLM will analyze transaction data here]",
                "conclusion": "[Placeholder — LLM will summarize findings here]",
            },
            "audit_trail": [],
            "quality_score": {
                "completeness": 0.0,
                "compliance": 0.0,
                "readability": 0.0,
                "evidence_linkage": 0.0,
            },
            "typology": None,
        }

    def _build_prompt(self, case_data: dict, context: Optional[str] = None) -> str:
        """Build the full prompt from case data and RAG context."""
        prompt_parts = [
            "Generate a SAR narrative for the following case:\n",
            f"Customer: {case_data.get('customer', {})}",
            f"Transactions: {case_data.get('transactions', [])}",
        ]
        if context:
            prompt_parts.insert(1, f"\nRelevant Regulatory Context:\n{context}\n")

        return "\n".join(prompt_parts)
