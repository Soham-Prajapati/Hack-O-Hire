"""
Typology Classifier — XGBoost-based suspicious activity pattern classifier.

Owner: HET ONLY

Classifies transaction sets into AML typologies:
  - structuring (splitting deposits under thresholds)
  - smurfing    (many small senders → one receiver)
  - layering    (rapid multi-hop fund movement)
  - round_tripping (money returns to origin)
  - normal      (benign activity)

Uses SHAP for feature-level explanations.
"""
import os
import warnings
from typing import Optional

import numpy as np
import pandas as pd
import joblib
from xgboost import XGBClassifier

warnings.filterwarnings("ignore", category=FutureWarning)

# --- Paths ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_MODEL_PATH = os.path.join(_HERE, "typology_model.joblib")

# --- Label mapping ---
TYPOLOGY_LABELS = ["normal", "structuring", "smurfing", "layering", "round_tripping"]
_LABEL_TO_INT = {lab: i for i, lab in enumerate(TYPOLOGY_LABELS)}


# =========================================================================== #
#  Feature Engineering
# =========================================================================== #

def extract_features(transactions: list[dict]) -> dict:
    """
    Extract ML features from a list of transaction dicts.

    Features:
        total_amount          – sum of all txn amounts
        avg_amount            – mean txn amount
        num_transactions      – number of transactions
        num_unique_senders    – distinct senders
        num_unique_receivers  – distinct receivers
        time_window_days      – span from first to last txn
        avg_time_gap_hours    – mean gap between consecutive txns
        max_single_txn        – largest single transaction
        below_threshold_ratio – fraction of txns under ₹1,00,000
        txn_type_diversity    – number of distinct transfer types
    """
    if not transactions:
        return {k: 0.0 for k in [
            "total_amount", "avg_amount", "num_transactions",
            "num_unique_senders", "num_unique_receivers",
            "time_window_days", "avg_time_gap_hours",
            "max_single_txn", "below_threshold_ratio", "txn_type_diversity",
        ]}

    df = pd.DataFrame(transactions)

    # Amount features
    amounts = pd.to_numeric(df.get("amount", pd.Series(dtype=float)), errors="coerce").fillna(0)
    total_amount = float(amounts.sum())
    avg_amount = float(amounts.mean()) if len(amounts) > 0 else 0.0
    max_single_txn = float(amounts.max()) if len(amounts) > 0 else 0.0
    n = len(df)
    below_threshold = int((amounts < 100000).sum())
    below_threshold_ratio = below_threshold / n if n > 0 else 0.0

    # Counter-party features
    senders = df.get("sender", pd.Series(dtype=str))
    receivers = df.get("receiver", pd.Series(dtype=str))
    num_unique_senders = int(senders.nunique()) if not senders.empty else 0
    num_unique_receivers = int(receivers.nunique()) if not receivers.empty else 0

    # Time features
    time_window_days = 0.0
    avg_time_gap_hours = 0.0
    if "timestamp" in df.columns:
        try:
            ts = pd.to_datetime(df["timestamp"], errors="coerce").dropna().sort_values()
            if len(ts) >= 2:
                time_window_days = (ts.iloc[-1] - ts.iloc[0]).total_seconds() / 86400
                gaps = ts.diff().dropna().dt.total_seconds() / 3600
                avg_time_gap_hours = float(gaps.mean())
        except Exception:
            pass

    # Type diversity
    txn_types = df.get("type", pd.Series(dtype=str))
    txn_type_diversity = int(txn_types.nunique()) if not txn_types.empty else 0

    return {
        "total_amount": total_amount,
        "avg_amount": avg_amount,
        "num_transactions": float(n),
        "num_unique_senders": float(num_unique_senders),
        "num_unique_receivers": float(num_unique_receivers),
        "time_window_days": time_window_days,
        "avg_time_gap_hours": avg_time_gap_hours,
        "max_single_txn": max_single_txn,
        "below_threshold_ratio": below_threshold_ratio,
        "txn_type_diversity": float(txn_type_diversity),
    }


FEATURE_NAMES = [
    "total_amount", "avg_amount", "num_transactions",
    "num_unique_senders", "num_unique_receivers",
    "time_window_days", "avg_time_gap_hours",
    "max_single_txn", "below_threshold_ratio", "txn_type_diversity",
]


# =========================================================================== #
#  Synthetic Training Data Generator
# =========================================================================== #

def _generate_training_data(n_per_class: int = 1000, seed: int = 42) -> tuple:
    """Generate synthetic training data for each typology class."""
    rng = np.random.RandomState(seed)
    rows = []

    for _ in range(n_per_class):
        # --- NORMAL ---
        rows.append({
            "label": 0,
            "total_amount": rng.uniform(50000, 500000),
            "avg_amount": rng.uniform(10000, 100000),
            "num_transactions": rng.randint(1, 10),
            "num_unique_senders": rng.randint(1, 4),
            "num_unique_receivers": rng.randint(1, 4),
            "time_window_days": rng.uniform(1, 30),
            "avg_time_gap_hours": rng.uniform(12, 168),     # hours between txns
            "max_single_txn": rng.uniform(10000, 200000),
            "below_threshold_ratio": rng.uniform(0.0, 0.4),
            "txn_type_diversity": rng.randint(1, 3),
        })

        # --- STRUCTURING ---
        n_txn = rng.randint(10, 30)
        amt = rng.uniform(80000, 99000)
        rows.append({
            "label": 1,
            "total_amount": amt * n_txn,
            "avg_amount": amt,
            "num_transactions": n_txn,
            "num_unique_senders": 1,                          # same sender
            "num_unique_receivers": 1,                        # same receiver
            "time_window_days": rng.uniform(1, 5),
            "avg_time_gap_hours": rng.uniform(0.5, 4),
            "max_single_txn": rng.uniform(85000, 99900),     # always under 1L
            "below_threshold_ratio": rng.uniform(0.9, 1.0),  # most under thresh
            "txn_type_diversity": 1,                          # single type
        })

        # --- SMURFING ---
        n_senders = rng.randint(8, 25)
        avg_a = rng.uniform(70000, 150000)
        rows.append({
            "label": 2,
            "total_amount": avg_a * n_senders,
            "avg_amount": avg_a,
            "num_transactions": n_senders,
            "num_unique_senders": n_senders,                  # many unique senders
            "num_unique_receivers": 1,                        # single receiver
            "time_window_days": rng.uniform(1, 7),
            "avg_time_gap_hours": rng.uniform(0.5, 6),
            "max_single_txn": rng.uniform(100000, 200000),
            "below_threshold_ratio": rng.uniform(0.3, 0.8),
            "txn_type_diversity": rng.randint(1, 3),
        })

        # --- LAYERING ---
        n_hops = rng.randint(8, 20)
        base_amt = rng.uniform(1000000, 5000000)
        rows.append({
            "label": 3,
            "total_amount": base_amt * 0.95 * n_hops,        # amounts decrease
            "avg_amount": base_amt * 0.95,
            "num_transactions": n_hops,
            "num_unique_senders": n_hops - rng.randint(0, 3), # many intermediaries
            "num_unique_receivers": n_hops - rng.randint(0, 3),
            "time_window_days": rng.uniform(0.1, 3),          # very fast
            "avg_time_gap_hours": rng.uniform(0.2, 3),        # rapid hops
            "max_single_txn": base_amt * rng.uniform(0.9, 1.1),
            "below_threshold_ratio": rng.uniform(0.0, 0.2),   # large amounts
            "txn_type_diversity": rng.randint(2, 4),           # mixed types
        })

        # --- ROUND TRIPPING ---
        amt_rt = rng.uniform(500000, 3000000)
        rows.append({
            "label": 4,
            "total_amount": amt_rt * rng.uniform(2, 6),
            "avg_amount": amt_rt,
            "num_transactions": rng.randint(4, 12),
            "num_unique_senders": rng.randint(2, 5),
            "num_unique_receivers": rng.randint(2, 5),         # sender = receiver
            "time_window_days": rng.uniform(5, 30),
            "avg_time_gap_hours": rng.uniform(12, 72),
            "max_single_txn": amt_rt * rng.uniform(0.9, 1.5),
            "below_threshold_ratio": rng.uniform(0.0, 0.3),
            "txn_type_diversity": rng.randint(2, 4),
        })

    df = pd.DataFrame(rows)
    X = df[FEATURE_NAMES].values
    y = df["label"].values
    return X, y


# =========================================================================== #
#  Classifier
# =========================================================================== #

class TypologyClassifier:
    """
    XGBoost classifier for AML transaction typology detection.

    Usage:
        # Training (one-time)
        clf = TypologyClassifier()
        stats = clf.train()

        # Inference
        clf = TypologyClassifier()
        clf.load_model()
        result = clf.predict(transactions)
        explanation = clf.explain(transactions)
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or _DEFAULT_MODEL_PATH
        self.model: Optional[XGBClassifier] = None
        self.typology_labels = TYPOLOGY_LABELS

    # ---- Training -------------------------------------------------------- #

    def train(self, n_per_class: int = 1000, seed: int = 42) -> dict:
        """
        Train the XGBoost classifier on synthetic data and save to disk.

        Returns:
            Dict with accuracy, f1, precision, recall, and classification report.
        """
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import (
            accuracy_score, f1_score, precision_score, recall_score,
            classification_report,
        )

        X, y = _generate_training_data(n_per_class=n_per_class, seed=seed)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=seed, stratify=y,
        )

        self.model = XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            objective="multi:softprob",
            num_class=len(TYPOLOGY_LABELS),
            eval_metric="mlogloss",
            use_label_encoder=False,
            random_state=seed,
            verbosity=0,
        )
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        prec = precision_score(y_test, y_pred, average="weighted")
        rec = recall_score(y_test, y_pred, average="weighted")
        report = classification_report(
            y_test, y_pred,
            target_names=TYPOLOGY_LABELS,
            output_dict=True,
        )

        # Save model
        joblib.dump(self.model, self.model_path)
        print(f"[TypologyClassifier] Model saved to {self.model_path}")
        print(f"[TypologyClassifier] Accuracy={acc:.4f}  F1={f1:.4f}  "
              f"Precision={prec:.4f}  Recall={rec:.4f}")

        return {
            "accuracy": round(acc, 4),
            "f1": round(f1, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "classification_report": report,
        }

    # ---- Model Loading --------------------------------------------------- #

    def load_model(self):
        """Load trained model from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. Run train() first."
            )
        self.model = joblib.load(self.model_path)
        print(f"[TypologyClassifier] Model loaded from {self.model_path}")

    # ---- Prediction ------------------------------------------------------ #

    def predict(self, transactions: list[dict]) -> dict:
        """
        Predict the typology for a set of transactions.

        Args:
            transactions: List of transaction dicts

        Returns:
            Dict matching the integration contract:
            {
                "typology": "structuring",
                "confidence": 0.92,
                "top_features": {
                    "num_unique_senders": 0.35,
                    "total_amount": 0.28,
                    "time_window_days": 0.22
                }
            }
        """
        if self.model is None:
            self.load_model()

        features = extract_features(transactions)
        X = np.array([[features[f] for f in FEATURE_NAMES]])

        probas = self.model.predict_proba(X)[0]
        pred_idx = int(np.argmax(probas))
        confidence = float(probas[pred_idx])
        typology = TYPOLOGY_LABELS[pred_idx]

        # Feature importances from the model (global)
        importances = self.model.feature_importances_
        feat_imp = {
            FEATURE_NAMES[i]: round(float(importances[i]), 4)
            for i in np.argsort(importances)[::-1][:5]
        }

        return {
            "typology": typology,
            "confidence": round(confidence, 4),
            "risk_score": int(confidence * 100) if typology != "normal" else int(confidence * 10),
            "top_features": feat_imp,
        }

    # ---- SHAP Explanations ----------------------------------------------- #

    def explain(self, transactions: list[dict]) -> dict:
        """
        Generate SHAP explanation for the prediction.

        Returns:
            Dict with:
            {
                "typology": "structuring",
                "confidence": 0.92,
                "features": {
                    "below_threshold_ratio": 0.45,
                    "num_unique_senders": -0.12,
                    ...
                }
            }
        """
        if self.model is None:
            self.load_model()

        import shap

        features = extract_features(transactions)
        X = np.array([[features[f] for f in FEATURE_NAMES]])

        # Prediction
        probas = self.model.predict_proba(X)[0]
        pred_idx = int(np.argmax(probas))
        typology = TYPOLOGY_LABELS[pred_idx]
        confidence = float(probas[pred_idx])

        # SHAP values
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)

        # shap_values shape: (n_samples, n_features, n_classes) or list
        if isinstance(shap_values, list):
            # One array per class
            sv = shap_values[pred_idx][0]       # shape (n_features,)
        elif shap_values.ndim == 3:
            sv = shap_values[0, :, pred_idx]    # shape (n_features,)
        else:
            sv = shap_values[0]                 # fallback

        # Map feature names → SHAP values (sorted by absolute impact)
        feat_shap = {
            FEATURE_NAMES[i]: round(float(sv[i]), 4)
            for i in np.argsort(np.abs(sv))[::-1][:5]
        }

        return {
            "typology": typology,
            "confidence": round(confidence, 4),
            "features": feat_shap,
        }


# =========================================================================== #
#  Convenience function (matches integration contract name)
# =========================================================================== #

_singleton: Optional[TypologyClassifier] = None


def predict_typology(transactions: list[dict]) -> dict:
    """
    Module-level convenience function.

    Matches the integration contract: Het → Dev (ML Model → LLM Engine)
    Returns:
        {"typology": "...", "confidence": 0.XX, "top_features": {...}}
    """
    global _singleton
    if _singleton is None:
        _singleton = TypologyClassifier()
        _singleton.load_model()
    return _singleton.predict(transactions)


# =========================================================================== #
#  CLI: Train the model
# =========================================================================== #

if __name__ == "__main__":
    print("=" * 60)
    print("  Typology Classifier — Training")
    print("=" * 60)
    clf = TypologyClassifier()
    stats = clf.train()
    print(f"\nAccuracy : {stats['accuracy']}")
    print(f"F1 Score : {stats['f1']}")
    print(f"Precision: {stats['precision']}")
    print(f"Recall   : {stats['recall']}")

    # Quick test on demo data
    print("\n--- Testing on demo scenarios ---")
    import pandas as pd  # noqa: F811
    data_dir = os.path.join(_HERE, "..", "data", "sample_data")
    for scenario in ["scenario_smurfing", "scenario_layering", "scenario_structuring"]:
        csv_path = os.path.join(data_dir, f"{scenario}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            result = clf.predict(df.to_dict("records"))
            expl = clf.explain(df.to_dict("records"))
            print(f"  {scenario:30s} → {result['typology']:15s} "
                  f"(conf={result['confidence']:.2f})  "
                  f"SHAP top: {list(expl['features'].keys())[:3]}")
        else:
            print(f"  {scenario:30s} → [file not found]")

    print("\nDone!")
