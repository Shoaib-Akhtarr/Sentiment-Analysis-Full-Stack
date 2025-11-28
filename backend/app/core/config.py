import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = APP_DIR / "core" / "models"

# Model paths
MODEL_PATH = MODELS_DIR / "model_best.pkl"
VECTORIZER_PATH = MODELS_DIR / "vectorizer.pkl"
RESULTS_PATH = MODELS_DIR / "training_results.csv"

# Data paths
RAW_DATA_PATH = DATA_DIR / "raw_dataset.csv"
CLEANED_DATA_PATH = DATA_DIR / "cleaned_dataset.csv"

# Training settings
RANDOM_STATE = 42
TEST_SIZE = 0.15
MAX_FEATURES = 40000
NGRAM_RANGE = (1, 2)

# Model parameters
MODELS_CONFIG = {
    'MultinomialNB': {'alpha': [0.01, 0.05, 0.1, 0.5, 1.0]},
    'LogisticRegression': {'C': [0.1, 0.5, 1.0, 5.0, 10.0]},
    'LinearSVC': {'C': [0.1, 0.5, 1.0, 5.0], 'loss': ['hinge', 'squared_hinge']},
}

# Create directories if they don't exist
MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

