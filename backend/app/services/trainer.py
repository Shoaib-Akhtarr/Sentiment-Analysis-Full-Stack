# ==========================================
# FILE 13: app/services/trainer.py
# ==========================================
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from app.utils.preprocess import clean_text
from app.core.config import (
    MODEL_PATH, VECTORIZER_PATH, RESULTS_PATH,
    RANDOM_STATE, TEST_SIZE, MAX_FEATURES, NGRAM_RANGE
)

def train_model_from_csv(df: pd.DataFrame) -> dict:
    """
    Train model from DataFrame
    
    Args:
        df: DataFrame with 'text' and 'label' columns
        
    Returns:
        dict with training results
    """
    # Preprocess
    df = df.copy()
    df['label'] = df['label'].astype(str).str.strip().str.lower()
    df['label'] = df['label'].replace({'0': 'ham', '1': 'spam'})
    df['text'] = df['text'].astype(str).apply(clean_text)
    df = df.dropna(subset=['text', 'label']).reset_index(drop=True)
    
    print(f"📊 Total samples: {len(df)}")
    
    # Split data
    X_text = df['text'].tolist()
    y = df['label'].tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_text, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    # Vectorizer
    vectorizer = TfidfVectorizer(max_features=MAX_FEATURES, ngram_range=NGRAM_RANGE)
    
    # Train LinearSVC (best for most spam datasets)
    print("🔥 Training LinearSVC model...")
    pipe = Pipeline([
        ('tfidf', vectorizer),
        ('clf', LinearSVC(random_state=RANDOM_STATE, max_iter=3000))
    ])
    
    param_grid = {
        'clf__C': [0.1, 0.5, 1.0, 5.0],
        'clf__loss': ['hinge', 'squared_hinge']
    }
    
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)
    grid = GridSearchCV(pipe, param_grid, cv=cv, scoring='accuracy', verbose=1, n_jobs=-1)
    grid.fit(X_train, y_train)
    
    # Evaluate
    y_pred = grid.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Test Accuracy: {accuracy:.4f}")
    print("\n" + classification_report(y_test, y_pred))
    
    # Save model and vectorizer
    best_model = grid.best_estimator_.named_steps['clf']
    best_vectorizer = grid.best_estimator_.named_steps['tfidf']
    
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(best_vectorizer, VECTORIZER_PATH)
    
    print(f"💾 Model saved to: {MODEL_PATH}")
    print(f"💾 Vectorizer saved to: {VECTORIZER_PATH}")
    
    # Reload global model
    from app.core.loader import load_model_and_vectorizer
    load_model_and_vectorizer()
    
    return {
        "accuracy": accuracy,
        "total_samples": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "model_type": "LinearSVC",
        "best_params": grid.best_params_
    }

