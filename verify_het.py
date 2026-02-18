"""Quick verification script for Het's components."""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd

print("=" * 60)
print("  VERIFICATION: Het's Data & ML Components")
print("=" * 60)

# ----- 1. Data Parser -----
print("\n--- 1. Data Parser ---")
from app.utils.data_parser import parse_csv, parse_file

for csv_name in ["scenario_smurfing.csv", "scenario_layering.csv", "scenario_structuring.csv"]:
    path = os.path.join("data", "sample_data", csv_name)
    with open(path, "rb") as f:
        content = f.read()
    result = parse_file(content, csv_name)
    n_txn = len(result.get("transactions", []))
    cust = result.get("customer", {}).get("name", "?")
    print(f"  {csv_name:35s} -> {n_txn} txns, customer='{cust}'")
    assert n_txn > 0, f"No transactions parsed from {csv_name}"
    assert "error" not in result, f"Error in {csv_name}: {result.get('error')}"

print("  [PASS] All CSVs parsed successfully")

# ----- 2. Classifier Training -----
print("\n--- 2. Classifier Training ---")
from ml_models.typology_classifier import TypologyClassifier

clf = TypologyClassifier()
stats = clf.train()
print(f"  Accuracy : {stats['accuracy']}")
print(f"  F1 Score : {stats['f1']}")
print(f"  Precision: {stats['precision']}")
print(f"  Recall   : {stats['recall']}")
assert stats["accuracy"] > 0.80, f"Accuracy {stats['accuracy']} < 0.80"
print("  [PASS] Accuracy > 0.80")

# ----- 3. Predictions on Demo Scenarios -----
print("\n--- 3. Predictions on Demo Scenarios ---")
for csv_name in ["scenario_smurfing.csv", "scenario_layering.csv", "scenario_structuring.csv"]:
    path = os.path.join("data", "sample_data", csv_name)
    df = pd.read_csv(path)
    result = clf.predict(df.to_dict("records"))
    print(f"  {csv_name:35s} -> {result['typology']:15s} (conf={result['confidence']:.4f})")
    print(f"    top_features: {result['top_features']}")
    assert result["confidence"] > 0, f"Zero confidence for {csv_name}"

# ----- 4. SHAP Explanations -----
print("\n--- 4. SHAP Explanations ---")
df = pd.read_csv("data/sample_data/scenario_smurfing.csv")
expl = clf.explain(df.to_dict("records"))
print(f"  Typology  : {expl['typology']}")
print(f"  Confidence: {expl['confidence']}")
print(f"  SHAP features: {expl['features']}")
assert len(expl["features"]) > 0, "No SHAP features returned"
print("  [PASS] SHAP explanations working")

# ----- 5. Per-class report -----
print("\n--- 5. Classification Report ---")
report = stats["classification_report"]
for label in ["normal", "structuring", "smurfing", "layering", "round_tripping"]:
    r = report.get(label, {})
    print(f"  {label:20s}  precision={r.get('precision',0):.2f}  "
          f"recall={r.get('recall',0):.2f}  f1={r.get('f1-score',0):.2f}")

print("\n" + "=" * 60)
print("  ALL VERIFICATIONS PASSED")
print("=" * 60)
