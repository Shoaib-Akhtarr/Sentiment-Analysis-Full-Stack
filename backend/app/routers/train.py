
# ==========================================
# FILE 8: app/routers/train.py
# ==========================================
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from io import StringIO
from app.services.trainer import train_model_from_csv

router = APIRouter()

@router.post("/upload")
async def train_from_csv(file: UploadFile = File(...)):
    """
    Upload CSV and train model
    
    CSV format required:
    - Columns: 'text', 'label'
    - Labels: 'spam' or 'ham' (or 0/1)
    
    Example CSV:
    ```
    text,label
    "Hello friend",ham
    "Win $1000 now!",spam
    ```
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        # Validate columns
        if 'text' not in df.columns or 'label' not in df.columns:
            raise HTTPException(
                status_code=400, 
                detail="CSV must contain 'text' and 'label' columns"
            )
        
        # Train model
        result = train_model_from_csv(df)
        
        return JSONResponse(content={
            "status": "success",
            "message": "Model trained successfully!",
            "accuracy": result['accuracy'],
            "total_samples": result['total_samples'],
            "model_type": result['model_type']
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")

