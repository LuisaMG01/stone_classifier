# model.py
import joblib
from sklearn.ensemble import RandomForestClassifier


def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, "model/mineral_classifier.pkl")
    return model


def load_model(path="model/mineral_classifier.pkl"):
    return joblib.load(path)
