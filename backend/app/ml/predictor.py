import joblib
import os
import pandas as pd
from app.ml.feature_engineering import extract_url_features

ML_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(ML_DIR, "model.joblib")
FEATURES_PATH = os.path.join(ML_DIR, "features.joblib")

model = None
feature_names = None

def load_model():
    global model, feature_names
    if os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH):
        model = joblib.load(MODEL_PATH)
        feature_names = joblib.load(FEATURES_PATH)
        print("Modèle ML chargé")
    else:
        print("Modèle ML non trouvé — lance python3 -m app.ml.train")

def predict_url(url: str) -> dict:
    if model is None:
        return {"error": "Modèle non chargé", "ml_score": None}

    features = extract_url_features(url)
    X = pd.DataFrame([[features[f] for f in feature_names]], columns=feature_names)

    proba = model.predict_proba(X)[0]
    ml_score = round(float(proba[1]) * 100, 2)
    verdict = "malicious" if ml_score > 50 else "benign"

    importances = model.feature_importances_
    top_features = sorted(
        zip(feature_names, importances),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    return {
        "ml_score": ml_score,
        "ml_verdict": verdict,
        "top_features": [
            {"feature": f, "importance": round(imp * 100, 1)}
            for f, imp in top_features
        ],
        "features_used": features
    }