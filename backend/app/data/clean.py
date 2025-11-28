import pandas as pd
import os

# Input & Output paths
INPUT_FILE = "raw.csv"       # original dataset
OUTPUT_FILE = "cleaned_dataset.csv"  # cleaned dataset to be used in training

# Check if input exists
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"{INPUT_FILE} not found. Place your CSV in the data folder.")

# Load CSV
df = pd.read_csv(INPUT_FILE)

# Keep only 'label' and 'text'
required_cols = ['label', 'text']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in dataset!")

df_cleaned = df[required_cols].copy()

# Drop empty rows
df_cleaned.dropna(subset=['label', 'text'], inplace=True)

# Optional: remove duplicate rows
df_cleaned.drop_duplicates(inplace=True)

# Strip text whitespace
df_cleaned['text'] = df_cleaned['text'].astype(str).str.strip()
df_cleaned['label'] = df_cleaned['label'].astype(str).str.strip().str.lower()

# Map numeric labels if needed (example: 0 -> ham, 1 -> spam)
df_cleaned['label'] = df_cleaned['label'].replace({'0':'ham','1':'spam'})

# Save cleaned CSV
df_cleaned.to_csv(OUTPUT_FILE, index=False)

print(f"Cleaned dataset saved to {OUTPUT_FILE}")
print(f"Total rows: {len(df_cleaned)}")
import pandas as pd
import os

# Input & Output paths
INPUT_FILE = "raw_dataset.csv"       # original dataset
OUTPUT_FILE = "cleaned_dataset.csv"  # cleaned dataset to be used in training

# Check if input exists
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"{INPUT_FILE} not found. Place your CSV in the data folder.")

# Load CSV
df = pd.read_csv(INPUT_FILE)

# Keep only 'label' and 'text'
required_cols = ['label', 'text']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in dataset!")

df_cleaned = df[required_cols].copy()

# Drop empty rows
df_cleaned.dropna(subset=['label', 'text'], inplace=True)

# Optional: remove duplicate rows
df_cleaned.drop_duplicates(inplace=True)

# Strip text whitespace
df_cleaned['text'] = df_cleaned['text'].astype(str).str.strip()
df_cleaned['label'] = df_cleaned['label'].astype(str).str.strip().str.lower()

# Map numeric labels if needed (example: 0 -> ham, 1 -> spam)
df_cleaned['label'] = df_cleaned['label'].replace({'0':'ham','1':'spam'})

# Save cleaned CSV
df_cleaned.to_csv(OUTPUT_FILE, index=False)

print(f"Cleaned dataset saved to {OUTPUT_FILE}")
print(f"Total rows: {len(df_cleaned)}")
