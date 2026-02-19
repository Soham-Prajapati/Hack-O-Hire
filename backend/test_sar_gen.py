import asyncio
import sys
import os
import pandas as pd

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.llm_engine import LLMEngine

async def main():
    print("Loading data...")
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "../data/sample_data/scenario_smurfing.csv")
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print("CSV not found, using mock data")
        df = pd.DataFrame([{"amount": 9000, "type": "cash_deposit"}])
    
    # Simple data structuring for test
    case_data = {
        "customer": {
            "name": "Test Subject",
            "id": "CUST-999",
            "risk_profile": "High"
        },
        "transactions": df.head(10).to_dict(orient="records") # Limit to 10 for speed
    }
    
    print("Initializing Engine...")
    engine = LLMEngine()
    
    print("Generating SAR...")
    result = await engine.generate_sar(case_data)
    
    print("\n=== NARRATIVE ===")
    narrative_str = f"INTRODUCTION\n{result['narrative']['introduction']}\n\nBODY\n{result['narrative']['body']}\n\nCONCLUSION\n{result['narrative']['conclusion']}"
    print(narrative_str)
    
    print("\n=== AUDIT TRAIL ===")
    for step in result["audit_trail"]:
        print(f"[{step['step']}] {step['action']}: {str(step['output'])[:100]}...")

    print("\n=== TESTING CHAT WITH SAR ===")
    queries = [
        "What is the total suspicious amount?",
        "Why is this activity considered suspicious?",
        "Who are the main subjects involved?"
    ]

    for q in queries:
        print(f"\nUser: {q}")
        response = await engine.chat_with_sar(case_data, [], q)
        print(f"AI: {response}")

if __name__ == "__main__":
    asyncio.run(main())
