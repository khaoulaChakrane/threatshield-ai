import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import sys
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.ml.feature_engineering import extract_url_features

ML_DIR = os.path.dirname(__file__)


def load_dataset(path):
    print(f"Chargement du dataset depuis {path}...")
    malicious, benign = [], []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["label"] == "1":
                malicious.append(row["url"])
            else:
                benign.append(row["url"])
    print(f"  → {len(malicious)} malveillantes, {len(benign)} bénignes")
    return malicious, benign


def build_dataset(malicious_urls, benign_urls):
    print("\nExtraction des features (peut prendre 1-2 minutes)...")
    data = []

    for i, url in enumerate(malicious_urls):
        try:
            features = extract_url_features(url)
            features["label"] = 1
            data.append(features)
        except:
            pass
        if (i + 1) % 500 == 0:
            print(f"  Malveillantes : {i+1}/{len(malicious_urls)}")

    for i, url in enumerate(benign_urls):
        try:
            features = extract_url_features(url)
            features["label"] = 0
            data.append(features)
        except:
            pass
        if (i + 1) % 500 == 0:
            print(f"  Bénignes : {i+1}/{len(benign_urls)}")

    return pd.DataFrame(data)


def train_model():
    dataset_path = os.path.join(ML_DIR, "phishing_dataset.csv")

    malicious_urls, benign_urls = load_dataset(dataset_path)

    df = build_dataset(malicious_urls, benign_urls)

    print(f"\nDataset final : {len(df)} URLs")
    print(f"  Malveillantes : {df['label'].sum()}")
    print(f"  Bénignes : {(df['label']==0).sum()}")

    X = df.drop("label", axis=1)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("\nEntraînement du modèle Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=10,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred) * 100
    print(f"\nPrécision : {acc:.1f}%")

    if acc == 100.0:
        print("Overfitting probable — dataset trop simple")
    elif acc >= 90.0:
        print("Bonne précision, généralisation correcte")
    else:
        print("Précision faible, dataset à améliorer")

    print("\nRapport détaillé :")
    print(classification_report(y_test, y_pred,
          target_names=["Bénin", "Malveillant"]))

    print("\nTop 5 features les plus importantes :")
    importances = sorted(
        zip(X.columns, model.feature_importances_),
        key=lambda x: x[1], reverse=True
    )[:5]
    for feat, imp in importances:
        print(f"  {feat:25} {imp*100:.1f}%")

    model_path = os.path.join(ML_DIR, "model.joblib")
    features_path = os.path.join(ML_DIR, "features.joblib")

    joblib.dump(model, model_path)
    joblib.dump(list(X.columns), features_path)

    print(f"\nModèle sauvegardé : {model_path}")


if __name__ == "__main__":
    train_model()