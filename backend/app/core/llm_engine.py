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
        
        # Initialize RAG Pipeline
        from app.core.rag_pipeline import RAGPipeline
        self.rag_pipeline = RAGPipeline()

    async def generate_sar(self, case_data: dict) -> dict:
        """
        Generate a SAR narrative from case data with RAG and Audit Trail.
        """
        from langchain_ollama import ChatOllama
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        from app.core.audit_logger import AuditLogger
        
        # 1. Initialize Audit Logger
        audit_logger = AuditLogger()
        audit_logger.log_step(1, "LLM Engine", "Started SAR Generation", output=f"Case Data: {str(case_data)[:200]}...")

        # 2. Retrieve Context (RAG)
        query = f"Suspicious activity for customer {case_data.get('customer', {}).get('name', 'Unknown')}"
        
        audit_logger.log_step(2, "RAG Pipeline", "Retrieving Content", output=f"Query: {query}")
        retrieved_docs = await self.rag_pipeline.retrieve_context(query)
        
        context_str = "\n".join([f"- {d['content']} (Source: {d['source']})" for d in retrieved_docs])
        audit_logger.log_step(3, "RAG Pipeline", "Context Retrieved", output=f"Found {len(retrieved_docs)} documents.")

        # 3. Initialize LLM
        llm = ChatOllama(
            model=self.model,
            base_url=self.base_url,
            temperature=0.2,
            keep_alive="5m"
        )

        # 4. Build Prompt
        system_message = self.system_prompt
        user_message_content = self._build_prompt(case_data, context_str)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            ("user", "{user_message}")
        ])

        # 5. Chain with Callbacks
        chain = prompt | llm | StrOutputParser()

        try:
            # Pass audit logger as callback
            narrative_text = await chain.ainvoke(
                {
                    "system_message": system_message, 
                    "user_message": user_message_content
                }, 
                config={'callbacks': [audit_logger]}
            )
            
            # 6. Parse Response
            sections = self._parse_narrative(narrative_text)
            
            # 7. Finalize Audit Trail
            audit_logger.log_step(5, "LLM Engine", "Parsing Complete", output="Narrative structured into sections.")
            
            return {
                "narrative": sections,
                "audit_trail": audit_logger.get_trail(),
                "quality_score": {
                    "completeness": 0.9, 
                    "compliance": 0.85, 
                    "readability": 0.9, 
                    "evidence_linkage": 0.8
                },
                "typology": None,
            }
        except Exception as e:
            audit_logger.log_step(99, "Error", "Generation Failed", output=str(e))
            return {
                "narrative": {
                    "introduction": "Error generating SAR.",
                    "body": str(e),
                    "conclusion": "Please check LLM connection."
                },
                "audit_trail": audit_logger.get_trail(),
                "quality_score": {},
                "typology": None
            }

    def _build_prompt(self, case_data: dict, context: Optional[str] = None) -> str:
        """Build the full prompt from case data and RAG context."""
        
        customer_str = str(case_data.get('customer', 'Unknown Customer'))
        transactions_str = str(case_data.get('transactions', 'No Transactions'))
        
        prompt_parts = [
            "Generate a Suspicious Activity Report (SAR) narrative based on the following data:\n",
            f"CUSTOMER DETAILS:\n{customer_str}\n",
            f"SUSPICIOUS TRANSACTIONS:\n{transactions_str}\n"
        ]
        
        if context:
            prompt_parts.append(f"\nRELEVANT REGULATORY GUIDANCE:\n{context}\n")
            
        prompt_parts.append("\nEnsure you explicitly cover the 5Ws (Who, What, When, Where, Why) and How.")
        
        return "\n".join(prompt_parts)

    def _parse_narrative(self, text: str) -> dict:
        """Heuristic parsing of the narrative into sections."""
        lower_text = text.lower()
        
        intro_start = lower_text.find("introduction")
        body_start = lower_text.find("body")
        conclusion_start = lower_text.find("conclusion")
        
        if intro_start == -1 or body_start == -1 or conclusion_start == -1:
             # Fallback if structure is missing
            return {
                "introduction": "Generated Narrative",
                "body": text,
                "conclusion": "End of Narrative"
            }

        # Extract sections (naive slicing)
        # Adjust indices to skip the headers
        intro_text = text[intro_start:body_start].replace("###", "").replace("INTRODUCTION", "").strip()
        body_text = text[body_start:conclusion_start].replace("###", "").replace("BODY", "").strip()
        conclusion_text = text[conclusion_start:].replace("###", "").replace("CONCLUSION", "").strip()
        
        return {
            "introduction": intro_text,
            "body": body_text,
            "conclusion": conclusion_text
        }
