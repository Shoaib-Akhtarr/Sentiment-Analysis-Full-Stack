
# ==========================================
# FILE 16: scripts/clean_data.py
# ==========================================
"""
Data Cleaning Script
Converts raw_dataset.csv to cleaned_dataset.csv

Usage:
    python scripts/clean_data.py
"""

import pandas as pd
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import RAW_DATA_PATH, CLEANED_DATA_PATH
from app.utils.preprocess import clean_text

def clean_dataset():
    """Clean raw dataset and save cleaned version"""
    
    # Check if raw data exists
    if not RAW_DATA_PATH.exists():
        print(f"❌ Error: {RAW_DATA_PATH} not found!")
        print(f"Please place your CSV file at: {RAW_DATA_PATH}")
        return
    
    print(f"📂 Reading data from: {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH)
    
    # Validate columns
    required_cols = ['text', 'label']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in dataset!")
    
    print(f"📊 Original dataset size: {len(df)} rows")
    
    # Keep only required columns
    df = df[required_cols].copy()
    
    # Clean text
    print("🧹 Cleaning text...")
    df['text'] = df['text'].astype(str).apply(clean_text)
    
    # Normalize labels
    df['label'] = df['label'].astype(str).str.strip().str.lower()
    df['label'] = df['label'].replace({'0': 'ham', '1': 'spam'})
    
    # Drop missing values
    df = df.dropna(subset=['text', 'label'])
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove empty texts
    df = df[df['text'].str.len() > 0]
    
    print(f"✅ Cleaned dataset size: {len(df)} rows")
    print(f"📈 Label distribution:\n{df['label'].value_counts()}")
    
    # Save cleaned data
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"💾 Cleaned dataset saved to: {CLEANED_DATA_PATH}")

if __name__ == "__main__":
    clean_dataset()

