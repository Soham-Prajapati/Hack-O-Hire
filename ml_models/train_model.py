"""
Train and save the XGBoost Typology Classifier.
"""
import os
import sys

# Ensure we can import from local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typology_classifier import TypologyClassifier

def main():
    print("Initializing classifier...")
    clf = TypologyClassifier()
    
    print("Training model (generating synthetic data)...")
    stats = clf.train(n_per_class=2000)
    
    print("\nTraining Stats:")
    print(f"Accuracy:  {stats['accuracy']:.4f}")
    print(f"F1 Score:  {stats['f1']:.4f}")
    
    print(f"\nModel saved to: {clf.model_path}")

if __name__ == "__main__":
    main()
