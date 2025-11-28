
# ==========================================
# FILE 17: scripts/train_model.py
# ==========================================
"""
Model Training Script
Trains ML model on cleaned_dataset.csv

Usage:
    python scripts/train_model.py
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from app.core.config import CLEANED_DATA_PATH
from app.services.trainer import train_model_from_csv

def train():
    """Train model from cleaned dataset"""
    
    # Check if cleaned data exists
    if not CLEANED_DATA_PATH.exists():
        print(f"❌ Error: {CLEANED_DATA_PATH} not found!")
        print("Please run: python scripts/clean_data.py first")
        return
    
    print(f"📂 Loading data from: {CLEANED_DATA_PATH}")
    df = pd.read_csv(CLEANED_DATA_PATH)
    
    print("🚀 Starting model training...")
    result = train_model_from_csv(df)
    
    print("\n" + "="*50)
    print("🎉 Training Complete!")
    print("="*50)
    print(f"✅ Accuracy: {result['accuracy']:.4f}")
    print(f"📊 Total samples: {result['total_samples']}")
    print(f"🔧 Model type: {result['model_type']}")
    print(f"⚙️ Best params: {result['best_params']}")

if __name__ == "__main__":
    train()

