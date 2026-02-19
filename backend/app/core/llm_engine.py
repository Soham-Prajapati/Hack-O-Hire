"""
LLM Engine — Ollama + Llama 3.1 8B integration for SAR narrative generation.

Owner: P2
"""
from typing import Optional


# SAR generation system prompt
SAR_SYSTEM_PROMPT = """You are an expert Anti-Money Laundering (AML) Compliance Officer at a major financial institution. Your task is to write a Suspicious Activity Report (SAR) narrative that strictly adheres to **FinCEN guidance**.

## OBJECTIVE
Generate a clean, professional, and audit-ready narrative that explains the suspicious activity clearly to law enforcement. Use **active voice**, be **concise**, and avoid speculation.

## MANDATORY STRUCTURE
Use these exact headers:

### INTRODUCTION
- **Executive Summary:** One clear sentence stating why this SAR is being filed (e.g., "This SAR is being filed to report potential structuring and smurfing activity...").
- **Subject:** Identify the main subject(s) (e.g., "The activity involves customer [Name], account [ID]...").
- **Timeframe:** Mention the start and end dates of the review period.
- **Investigation Source:** How was this alert triggered? (e.g., "Internal TM alert for rapid movement of funds").

### BODY (The 5Ws + How)
- **WHO:** Full identity of subject(s), occupation, risk profile, and any known adverse media or negative history.
- **WHAT:** Detailed chronology of transactions. Group similar transactions (e.g., "Between Jan 1 and Jan 5, 2026, the subject received 5 incoming high-value credits totaling $50,000...").
- **WHEN:** Specific dates and times (use Format: Month DD, YYYY).
- **WHERE:** Branch locations, originating jurisdictions, beneficiary banks.
- **WHY:** The core analysis. Why is this suspicious? (e.g., "The activity is inconsistent with the customer's profile as a student..." or "Rounds dollar amounts suggest an attempt to avoid reporting thresholds...").
- **HOW:** The mechanism (e.g., "Funds were layered through multiple accounts using NEFT transfers...").

### CONCLUSION
- **Summary:** Reiterate the total suspicious amount and the potential typology (e.g., "Total suspicious activity: $150,000. Suspected typology: Money Laundering / Layering.").
- **Action Taken:** (e.g., "The account has been placed on watch," or "Exit decision recommended.").
- **Data Source:** Reference internal records (e.g., "Core Banking System," "KYC File").
- **Contact:** "For further information, please contact the AML Compliance Department."

## STYLE GUIDELINES (STRICT)
1.  **Dates:** Use "Jan 15, 2026" format. Avoid "yesterday" or "last week".
2.  **Amounts:** Use "USD 50,000" or "INR 50,000" format.
3.  **Tone:** Formal, objective, authoritative. No "I think" or "It seems". Use "The data indicates...".
4.  **Formatting:** Use bullet points for lists of transactions to improve readability.
5.  **No Fluff:** Do not include greeting or closing remarks (e.g., no "Here is your SAR"). Just the report.
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

        # Use placeholders to avoid LangChain parsing curly braces in the content as variables
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message_content}"),
            ("user", "{user_message_content}")
        ])

        # 5. Chain with Callbacks
        chain = prompt | llm | StrOutputParser()

        try:
            # Pass audit logger as callback
            narrative_text = await chain.ainvoke(
                {
                    "system_message_content": system_message, 
                    "user_message_content": user_message_content
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

    async def chat_with_sar(self, case_data: dict, history: list[dict], query: str, sar_narrative: Optional[str] = None) -> str:
        """
        Chat with the SAR context (RAG + Conversation History + Generated Narrative).
        """
        from langchain_ollama import ChatOllama
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        # 1. Retrieve Context
        # We include the case data in the query context implicitly
        context_query = f"{query} related to {case_data.get('customer', {}).get('name', 'Customer')}"
        try:
            retrieved_docs = await self.rag_pipeline.retrieve_context(context_query, top_k=3)
            context_str = "\n".join([f"- {d['content']}" for d in retrieved_docs])
        except Exception:
            context_str = "No specific regulatory context found."
        
        # 2. Build Prompt
        system_prompt = """You are an AI assistant helping a compliance officer analyze a suspicious activity case.
        Use the provided Case Data, SAR Narrative (if available), and Regulatory Context to answer the user's question.
        If you don't know the answer, say so. Be professional and concise."""
        
        case_summary = f"Customer: {case_data.get('customer', {})}\nTransactions Summary: {len(case_data.get('transactions', []))} transactions."
        
        # Convert history to string format (naive approach for now)
        history_str = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in history[-5:]]) # Last 5 messages
        
        user_prompt_parts = [
            "### CASE DATA:",
            case_summary,
            "\n### REGULATORY CONTEXT:",
            context_str,
            "\n### CHAT HISTORY:",
            history_str
        ]

        if sar_narrative:
            user_prompt_parts.insert(2, f"\n### GENERATED SAR NARRATIVE:\n{sar_narrative}")

        user_prompt_parts.append(f"\n### USER QUESTION:\n{query}")
        
        user_prompt = "\n".join(user_prompt_parts)
        
        # 3. Call LLM
        llm = ChatOllama(
            model=self.model,
            base_url=self.base_url,
            temperature=0.4,
            keep_alive="5m"
        )
        
        # Use placeholders to avoid LangChain parsing curly braces in the content as variables
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt_content}"),
            ("user", "{user_prompt_content}")
        ])
        
        chain = prompt | llm | StrOutputParser()
        
        try:
            response = await chain.ainvoke({
                "system_prompt_content": system_prompt,
                "user_prompt_content": user_prompt
            })
            return response
        except Exception as e:
            return f"I encountered an error answering that: {e}"
