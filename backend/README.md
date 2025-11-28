# 🛡️ Spam Detection API - Backend

Machine Learning powered Spam/Ham message classifier built with **FastAPI** and **Scikit-learn**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Model Training](#model-training)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

✅ **Fast & Accurate** - ML-based spam detection with 95%+ accuracy  
✅ **RESTful API** - Clean FastAPI endpoints  
✅ **Single & Batch Prediction** - Analyze one or multiple messages  
✅ **TF-IDF Vectorization** - Advanced text processing  
✅ **Multiple ML Models** - Support for LinearSVC, LogisticRegression, etc.  
✅ **CORS Enabled** - Ready for frontend integration  
✅ **Auto Model Loading** - Models load on server start  
✅ **CSV Training Support** - Upload CSV to train models  

---

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **Scikit-learn** - Machine learning library
- **Pandas** - Data manipulation
- **Joblib** - Model serialization
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

---

## 📁 Project Structure

```
spam-detection-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration settings
│   │   ├── loader.py              # Model & vectorizer loader
│   │   └── models/                # Trained ML models
│   │       ├── model_best.pkl     # Best trained model
│   │       ├── vectorizer.pkl     # TF-IDF vectorizer
│   │       └── training_results.csv
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── predict.py             # Prediction endpoints
│   │   └── train.py               # Training endpoints
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── request.py             # Pydantic models
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── predictor.py           # Prediction logic
│   │   └── trainer.py             # Training logic
│   │
│   └── utils/
│       ├── __init__.py
│       └── preprocess.py          # Text preprocessing
│
├── data/
│   ├── raw_dataset.csv            # Original dataset
│   └── cleaned_dataset.csv        # Preprocessed dataset
│
├── scripts/
│   ├── clean_data.py              # Data cleaning script
│   └── train_model.py             # Model training script
│
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/spam-detection-backend.git
cd spam-detection-backend
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Prepare Dataset

Place your dataset CSV file in `data/raw_dataset.csv` with columns:
- `text` - Message content
- `label` - Classification (spam/ham or 0/1)

### Step 5: Clean Data

```bash
python scripts/clean_data.py
```

### Step 6: Train Model

```bash
python scripts/train_model.py
```

This will:
- Train multiple ML models
- Select the best performer
- Save model to `app/core/models/`
- Display accuracy metrics

### Step 7: Start Server

```bash
uvicorn app.main:app --reload
```

Server will run at: **http://127.0.0.1:8000**

---

## 📖 Usage

### Interactive API Documentation

Visit **http://127.0.0.1:8000/docs** for Swagger UI

### Example Requests

#### 1. Single Message Prediction

```bash
curl -X POST http://127.0.0.1:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"message":"Congratulations! You won $1000!"}'
```

**Response:**
```json
{
  "prediction": "SPAM",
  "probability": 0.95,
  "original_message": "Congratulations! You won $1000!"
}
```

#### 2. Batch Prediction

```bash
curl -X POST http://127.0.0.1:8000/api/predict_batch \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "Hello, how are you?",
      "Win money now!",
      "Meeting at 3pm"
    ]
  }'
```

**Response:**
```json
{
  "results": [
    {
      "prediction": "HAM",
      "probability": 0.92,
      "original_message": "Hello, how are you?"
    },
    {
      "prediction": "SPAM",
      "probability": 0.88,
      "original_message": "Win money now!"
    },
    {
      "prediction": "HAM",
      "probability": 0.85,
      "original_message": "Meeting at 3pm"
    }
  ]
}
```

---

## 🌐 API Endpoints

### Root Endpoint

```
GET /
```

Returns API status and available endpoints.

---

### Health Check

```
GET /health
```

Check if API is running.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### Single Prediction

```
POST /api/predict
```

**Request Body:**
```json
{
  "message": "Your text message here"
}
```

**Response:**
```json
{
  "prediction": "SPAM" | "HAM",
  "probability": 0.95,
  "original_message": "Your text message here"
}
```

---

### Batch Prediction

```
POST /api/predict_batch
```

**Request Body:**
```json
{
  "messages": ["message1", "message2", "message3"]
}
```

**Response:**
```json
{
  "results": [
    {
      "prediction": "SPAM" | "HAM",
      "probability": 0.95,
      "original_message": "message1"
    }
  ]
}
```

---

### Train Model (Upload CSV)

```
POST /api/train/upload
```

**Request:** Multipart form-data with CSV file

**CSV Format:**
```csv
text,label
"Hello friend",ham
"Win $1000 now!",spam
```

**Response:**
```json
{
  "status": "success",
  "message": "Model trained successfully!",
  "accuracy": 0.96,
  "total_samples": 5000,
  "model_type": "LinearSVC"
}
```

---

## 🤖 Model Training

### Supported Models

The system trains and compares multiple models:

1. **MultinomialNB** - Naive Bayes classifier
2. **LogisticRegression** - Linear model
3. **LinearSVC** - Support Vector Classifier (Default best)
4. **RandomForest** - Ensemble method

### Training Process

1. **Data Cleaning** - Remove duplicates, handle missing values
2. **Text Preprocessing** - Lowercase, remove URLs, special chars
3. **TF-IDF Vectorization** - Convert text to numerical features
4. **Model Training** - Train multiple models with GridSearchCV
5. **Model Selection** - Choose best performer based on accuracy
6. **Model Saving** - Save best model and vectorizer

### Hyperparameter Tuning

The system automatically performs grid search for optimal parameters:

```python
# LinearSVC Example
{
  'C': [0.1, 0.5, 1.0, 5.0],
  'loss': ['hinge', 'squared_hinge']
}
```

### Custom Training

To train with custom parameters, modify `app/core/config.py`:

```python
MODELS_CONFIG = {
    'LinearSVC': {
        'C': [0.1, 1.0, 10.0],
        'loss': ['squared_hinge']
    }
}
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file (optional):

```env
MODEL_PATH=app/core/models/model_best.pkl
VECTORIZER_PATH=app/core/models/vectorizer.pkl
DATA_PATH=data/cleaned_dataset.csv
```

### Model Configuration

Edit `app/core/config.py`:

```python
# Feature extraction
MAX_FEATURES = 40000
NGRAM_RANGE = (1, 2)

# Training
RANDOM_STATE = 42
TEST_SIZE = 0.15
```

### CORS Settings

In `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### Issue: Model not found

**Error:**
```
FileNotFoundError: Model not found at app/core/models/model_best.pkl
```

**Solution:**
```bash
python scripts/train_model.py
```

---

### Issue: CORS Error

**Error:**
```
Access to fetch blocked by CORS policy
```

**Solution:**
Check `allow_origins` in `app/main.py` includes your frontend URL.

---

### Issue: Import Error

**Error:**
```
ModuleNotFoundError: No module named 'sklearn'
```

**Solution:**
```bash
pip install -r requirements.txt
```

---

### Issue: Low Accuracy

**Solution:**
- Increase dataset size
- Add more training samples
- Adjust hyperparameters in `config.py`
- Try different models

---

## 📊 Performance Metrics

Typical performance on balanced dataset:

| Metric | Score |
|--------|-------|
| Accuracy | 96-98% |
| Precision | 95-97% |
| Recall | 94-96% |
| F1-Score | 95-97% |

---

## 🔒 Security Considerations

### Production Deployment

1. **Restrict CORS origins** to your frontend domain
2. **Add API authentication** (JWT, API keys)
3. **Rate limiting** to prevent abuse
4. **Input validation** for all endpoints
5. **HTTPS only** in production
6. **Environment variables** for sensitive data

### Example: Add API Key Authentication

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "your-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
```

---

## 🧪 Testing

### Run Tests

```bash
# Install pytest
pip install pytest

# Run tests
pytest tests/
```

### Test Coverage

```bash
pip install pytest-cov
pytest --cov=app tests/
```

---

## 📦 Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t spam-detection-api .
docker run -p 8000:8000 spam-detection-api
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- FastAPI documentation
- Scikit-learn community
- Open source contributors

---

## 📞 Support

For issues and questions:

- **GitHub Issues:** [Report Bug](https://github.com/yourusername/spam-detection-backend/issues)
- **Email:** support@example.com
- **Documentation:** [Wiki](https://github.com/yourusername/spam-detection-backend/wiki)

---

## 🗺️ Roadmap

- [ ] Add more ML models (XGBoost, BERT)
- [ ] Implement caching for predictions
- [ ] Add real-time training API
- [ ] Create admin dashboard
- [ ] Multi-language support
- [ ] Integration with messaging platforms

---

**Made with ❤️ using FastAPI and Scikit-learn**