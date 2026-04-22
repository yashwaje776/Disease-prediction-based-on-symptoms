from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

app = FastAPI()

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load model + vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ✅ Load dataset
df = pd.read_csv("dataset.csv")

# Optional: normalize for safety
df["disease"] = df["disease"].str.lower()

@app.get("/")
def home():
    return {"message": "ML API running 🚀"}

@app.post("/predict")
def predict(data: dict):
    try:
        # ✅ Get input safely
        text = data.get("text", "").lower()

        if not text:
            return {"error": "No input provided"}

        # ✅ Transform input
        X = vectorizer.transform([text])

        # ✅ Predict disease
        prediction = model.predict(X)[0].lower()

        # ✅ Find matching row
        result = df[df["disease"] == prediction]

        if result.empty:
            return {
                "disease": prediction,
                "doctor": "Not available",
                "cures": "Not available",
                "risk_level": "Unknown"
            }

        result = result.iloc[0]

        return {
            "disease": prediction,
            "doctor": result.get("doctor", "Not available"),
            "cures": result.get("cures", "Not available"),
            "risk_level": result.get("risk level", "Unknown")
        }

    except Exception as e:
        return {"error": str(e)}