# FILE 10: app/schemas/request.py
# ==========================================
from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Text message to classify")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Congratulations! You won $1000. Click here now!"
            }
        }


class BatchRequest(BaseModel):
    messages: List[str] = Field(..., min_items=1, description="List of messages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    "Hello, how are you?",
                    "Win $1000 now!",
                    "Meeting at 3pm"
                ]
            }
        }


class PredictResponse(BaseModel):
    prediction: str = Field(..., description="SPAM or HAM")
    probability: float = Field(..., description="Confidence score (0-1)")
    original_message: str = Field(..., description="Original input message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "SPAM",
                "probability": 0.95,
                "original_message": "Win $1000 now!"
            }
        }


class BatchResponse(BaseModel):
    results: List[PredictResponse]

