import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

#MODEL_PATH = "backend/saved_model/model.pkl"
#VECTORIZER_PATH = "backend/saved_model/vectorizer.pkl"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "saved_model", "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "saved_model", "vectorizer.pkl")

PRIORITY_ORDER = {"critical": 0, "urgent": 1, "medium": 2, "low": 3}
PRIORITY_COLOR = {
    "critical": "#FF3B30",
    "urgent": "#FF9500",
    "medium": "#FFCC00",
    "low": "#34C759",
}

# def save_model(model, vectorizer):
#     os.makedirs("backend/saved_model", exist_ok=True)
#     with open(MODEL_PATH, "wb") as f:
#         pickle.dump(model, f)
#     with open(VECTORIZER_PATH, "wb") as f:
#         pickle.dump(vectorizer, f)
def save_model(model, vectorizer):
    SAVE_DIR = os.path.join(BASE_DIR, "saved_model")
    os.makedirs(SAVE_DIR, exist_ok=True)

    with open(os.path.join(SAVE_DIR, "model.pkl"), "wb") as f:
        pickle.dump(model, f)

    with open(os.path.join(SAVE_DIR, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)

    print(f"✅ Model saved at {SAVE_DIR}")

def load_model():
    print("📂 Loading model from:", MODEL_PATH)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(f"Vectorizer not found at {VECTORIZER_PATH}")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    print("✅ Model file loaded")

    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    print("✅ Vectorizer loaded")

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