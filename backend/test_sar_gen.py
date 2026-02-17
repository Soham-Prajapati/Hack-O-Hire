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
    print(result["narrative"])
    
    print("\n=== AUDIT TRAIL ===")
    for step in result["audit_trail"]:
        print(f"[{step['step']}] {step['action']}: {str(step['output'])[:100]}...")

if __name__ == "__main__":
    asyncio.run(main())
