# ==========================================
# FILE 15: app/utils/preprocess.py
# ==========================================
import re
import html

def clean_text(text: str) -> str:
    """
    Clean and normalize text for ML model
    
    Steps:
    1. Decode HTML entities
    2. Convert to lowercase
    3. Remove URLs
    4. Remove special characters
    5. Normalize whitespace
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text string
    """
    if not isinstance(text, str):
        return ""
    
    # Decode HTML entities (e.g., &amp; -> &)
    text = html.unescape(text)
    
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' ', text)
    
    # Remove special characters (keep only alphanumeric and spaces)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
