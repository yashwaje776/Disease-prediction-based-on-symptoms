from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load model + vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Load dataset (for extra info like doctor, cure)
df = pd.read_csv("dataset.csv")

@app.get("/")
def home():
    return {"message": "ML API running 🚀"}

@app.post("/predict")
def predict(data: dict):
    text = data["text"].lower()

    # Transform input
    X = vectorizer.transform([text])

    # Predict disease
    prediction = model.predict(X)[0]

    # Get extra info from dataset
    result = df[df["disease"] == prediction].iloc[0]

    return {
        "disease": prediction,
        "doctor": result["doctor"],
        "cures": result["cures"],
        "risk_level": result["risk level"]
    }