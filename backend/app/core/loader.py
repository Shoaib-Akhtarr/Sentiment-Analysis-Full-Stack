
# ==========================================
# FILE 5: app/core/loader.py
# ==========================================
import joblib
import os
from app.core.config import MODEL_PATH, VECTORIZER_PATH

MODEL = None
VECTORIZER = None

def load_model_and_vectorizer():
    """Load trained model and vectorizer from disk"""
    global MODEL, VECTORIZER
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Please run training script first: python scripts/train_model.py"
        )
    
    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(
            f"Vectorizer not found at {VECTORIZER_PATH}. "
            "Please run training script first."
        )
    
    try:
        MODEL = joblib.load(MODEL_PATH)
        VECTORIZER = joblib.load(VECTORIZER_PATH)
        print("✅ Model and Vectorizer loaded successfully!")
    except Exception as e:
        raise Exception(f"Error loading model/vectorizer: {str(e)}")

# Auto-load on import
try:
    load_model_and_vectorizer()
except FileNotFoundError as e:
    print(f"⚠️ Warning: {str(e)}")
    MODEL = None
    VECTORIZER = None

