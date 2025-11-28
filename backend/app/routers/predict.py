
# ==========================================
# FILE 7: app/routers/predict.py
# ==========================================
from fastapi import APIRouter, HTTPException
from app.schemas.request import PredictRequest, BatchRequest, PredictResponse, BatchResponse
from app.services.predictor import predict_single, predict_batch

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
def predict_endpoint(request: PredictRequest):
    """
    Single message prediction
    
    Example:
    ```json
    {
        "message": "Congratulations! You won $1000. Click here to claim."
    }
    ```
    """
    try:
        result = predict_single(request.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/predict_batch", response_model=BatchResponse)
def predict_batch_endpoint(request: BatchRequest):
    """
    Batch prediction for multiple messages
    
    Example:
    ```json
    {
        "messages": [
            "Hello, how are you?",
            "Win $1000 now! Click here!",
            "Meeting at 3pm tomorrow"
        ]
    }
    ```
    """
    try:
        results = predict_batch(request.messages)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

