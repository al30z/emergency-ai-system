from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from model import load_model, predict_priority

print("Step 1: Starting app...")

app = FastAPI(
    title="AI Emergency Prioritizer API",
    description="Classifies emergency messages into critical, urgent, medium, and low priority.",
    version="1.0.0"
)

#added extra remove if not workin
model = None
vectorizer = None

model = None
vectorizer = None

@app.on_event("startup")
def load_all():
    global model, vectorizer

    print("🚀 Starting model load...")

    try:
        model, vectorizer = load_model()
        print("✅ Model fully loaded!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model at startup
print("Step 2: Before loading model...")

try:
    model, vectorizer = load_model()
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Model not found. Run train.py first. Error: {e}")
    model, vectorizer = None, None


class MessageRequest(BaseModel):
    message: str

class BatchRequest(BaseModel):
    messages: List[str]


@app.get("/")
def root():
    return {"status": "running", "message": "AI Emergency Prioritizer API"}


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

#edited def predict to add time measurement for debugging model loading and prediction time
import time
@app.post("/predict")
def predict(req: MessageRequest):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    start = time.time()

    result = predict_priority(req.message, model, vectorizer)

    print("⏱ Prediction time:", time.time() - start)

    return result


@app.post("/predict/batch")
def predict_batch(req: BatchRequest):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    if not req.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty.")

    results = [predict_priority(msg, model, vectorizer) for msg in req.messages]
    results.sort(key=lambda x: x["order"])
    return {"count": len(results), "results": results}


@app.get("/demo")
def demo():
    """Demo endpoint with sample messages"""
    samples = [
        "I am trapped under rubble",
        "Need medical attention soon",
        "Request for food supplies",
        "Any updates on the situation?",
    ]
    results = [predict_priority(msg, model, vectorizer) for msg in samples]
    results.sort(key=lambda x: x["order"])
    return {"results": results}
