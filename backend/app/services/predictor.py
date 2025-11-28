# FILE 12: app/services/predictor.py
# ==========================================
from app.utils.preprocess import clean_text
from app.core.loader import MODEL, VECTORIZER

def predict_single(message: str) -> dict:
    """
    Predict single message
    
    Args:
        message: Raw text message
        
    Returns:
        dict with prediction, probability, and original message
    """
    if MODEL is None or VECTORIZER is None:
        raise Exception("Model not loaded. Run training first.")
    
    # Clean text
    cleaned = clean_text(message)
    
    # Vectorize
    X = VECTORIZER.transform([cleaned])
    
    # Predict
    prediction = MODEL.predict(X)[0]
    
    # Get probability
    try:
        proba = MODEL.predict_proba(X)[0].max()
    except AttributeError:
        # If model doesn't support predict_proba (like SVC)
        proba = 0.0
    
    # Map prediction to string
    prediction_str = "SPAM" if str(prediction).lower() in ["1", "spam"] else "HAM"
    
    return {
        "prediction": prediction_str,
        "probability": float(proba),
        "original_message": message
    }


def predict_batch(messages: list) -> list:
    """
    Predict multiple messages
    
    Args:
        messages: List of raw text messages
        
    Returns:
        List of prediction results
    """
    if MODEL is None or VECTORIZER is None:
        raise Exception("Model not loaded. Run training first.")
    
    # Clean all texts
    cleaned = [clean_text(msg) for msg in messages]
    
    # Vectorize
    X = VECTORIZER.transform(cleaned)
    
    # Predict
    predictions = MODEL.predict(X)
    
    # Get probabilities
    try:
        probas = MODEL.predict_proba(X).max(axis=1)
    except AttributeError:
        probas = [0.0] * len(messages)
    
    # Format results
    results = []
    for msg, pred, prob in zip(messages, predictions, probas):
        prediction_str = "SPAM" if str(pred).lower() in ["1", "spam"] else "HAM"
        results.append({
            "prediction": prediction_str,
            "probability": float(prob),
            "original_message": msg
        })
    
    return results