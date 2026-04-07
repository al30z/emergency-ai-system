import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_PATH = "backend/saved_model/model.pkl"
VECTORIZER_PATH = "backend/saved_model/vectorizer.pkl"

PRIORITY_ORDER = {"critical": 0, "urgent": 1, "medium": 2, "low": 3}
PRIORITY_COLOR = {
    "critical": "#FF3B30",
    "urgent": "#FF9500",
    "medium": "#FFCC00",
    "low": "#34C759",
}

def save_model(model, vectorizer):
    os.makedirs("backend/saved_model", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

def predict_priority(message: str, model, vectorizer) -> dict:
    text = message.lower().strip()
    vec = vectorizer.transform([text])
    label = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    confidence = round(float(max(proba)) * 100, 2)
    return {
        "message": message,
        "priority": label,
        "confidence": confidence,
        "color": PRIORITY_COLOR[label],
        "order": PRIORITY_ORDER[label],
    }