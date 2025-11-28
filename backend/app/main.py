from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predict, train
import uvicorn

app = FastAPI(
    title="Spam Detection API",
    description="Machine Learning based Spam/Ham classifier",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend ke liye - production mein restrict karo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(predict.router, prefix="/api", tags=["Prediction"])
app.include_router(train.router, prefix="/api/train", tags=["Training"])

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Spam Detection API is active!",
        "endpoints": {
            "predict": "/api/predict",
            "batch_predict": "/api/predict_batch",
            "train": "/api/train/upload"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    print("🚀 Starting FastAPI Server...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

