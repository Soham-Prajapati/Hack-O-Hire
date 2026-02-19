
import asyncio
import sys
import os
import pandas as pd
from datetime import datetime

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.llm_engine import LLMEngine

async def evaluate_scenario(engine, scenario_name, csv_filename):
    print(f"\n{'='*50}")
    print(f"EVALUATING SCENARIO: {scenario_name.upper()}")
    print(f"{'='*50}")

    # 1. Load Data
    csv_path = os.path.join(os.path.dirname(__file__), f"../data/sample_data/{csv_filename}")
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_filename} not found at {csv_path}")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    # Mock Customer Data (Customize based on scenario)
    customer_profiles = {
        "smurfing": {"name": "Rajesh Gupta", "id": "CUST-101", "risk_profile": "Medium", "occupation": "Small Business Owner"},
        "layering": {"name": "Priya Sharma", "id": "CUST-202", "risk_profile": "High", "occupation": "Import/Export Trader"},
        "structuring": {"name": "Amit Patel", "id": "CUST-303", "risk_profile": "Medium", "occupation": "Cashier"}
    }
    
    profile = customer_profiles.get(scenario_name, {"name": "Test Subject", "id": "CUST-999", "risk_profile": "High"})

    # Limit transactions for context window usage
    transactions = df.head(15).to_dict(orient="records")
    
    case_data = {
        "customer": profile,
        "transactions": transactions
    }

    # 2. Generate SAR
    print(f"Generating SAR for {profile['name']} ({len(transactions)} txns)...")
    try:
        result = await engine.generate_sar(case_data)
    except Exception as e:
        print(f"❌ Generation Failed: {e}")
        return
    
    narrative = result.get("narrative", {})
    audit_trail = result.get("audit_trail", [])
    scores = result.get("quality_score", {})
    
    # 3. Chat Sanity Check
    print("Running Chat Sanity Check...")
    chat_query = "What is the total suspicious amount and the main typology?"
    try:
        # Use empty history for the sanity check as per new signature
        chat_response = await engine.chat_with_sar(
            case_data=case_data, 
            history=[], 
            query=chat_query, 
            sar_narrative=str(narrative)
        )
    except Exception as e:
        chat_response = f"Chat Failed: {e}"
        print(f"❌ Chat Failed: {e}")
    
    # 4. Save Output to File
    output_dir = os.path.join(os.path.dirname(__file__), "evaluation_results")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_file = os.path.join(output_dir, f"eval_{scenario_name}_{timestamp}.txt")
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"SCENARIO: {scenario_name.upper()}\n")
            f.write(f"DATE: {datetime.now()}\n")
            f.write(f"{'='*50}\n\n")
            
            f.write(f"### CUSTOMER PROFILE\n{profile}\n\n")
            
            f.write(f"### GENERATED NARRATIVE\n")
            if isinstance(narrative, dict):
                f.write(f"INTRODUCTION:\n{narrative.get('introduction', '')}\n\n")
                f.write(f"BODY:\n{narrative.get('body', '')}\n\n")
                f.write(f"CONCLUSION:\n{narrative.get('conclusion', '')}\n\n")
            else:
                f.write(f"{narrative}\n\n")
            
            f.write(f"### QUALITY SCORES\n{scores}\n\n")
            
            f.write(f"### CHAT SANITY CHECK\n")
            f.write(f"Q: {chat_query}\n")
            f.write(f"A: {chat_response}\n\n")
            
            f.write(f"### AUDIT TRAIL PREVIEW (First 5 Steps)\n")
            for step in audit_trail[:5]:
                 f.write(f"[{step.get('step')}] {step.get('action')}: {str(step.get('output'))[:50]}...\n")

        print(f"Result saved to: {output_file}")
    except Exception as e:
        print(f"Failed to save output: {e}")


async def main():
    print("Initializing LLM Engine...")
    try:
        engine = LLMEngine()
    except Exception as e:
        print(f"❌ Failed to initialize engine: {e}")
        return

    scenarios = [
        # ("smurfing", "scenario_smurfing.csv"),
        ("layering", "scenario_layering.csv"),
        # ("structuring", "scenario_structuring.csv")
    ]
    
    print(f"Starting evaluation of {len(scenarios)} scenarios...")
    for name, csv_file in scenarios:
        await evaluate_scenario(engine, name, csv_file)
    print("\nEvaluation Complete.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
