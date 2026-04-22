import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Clean data
df = df.fillna("")

# Normalize text
df["symptoms"] = df["symptoms"].str.lower()

# Features and labels
X_text = df["symptoms"]
y = df["disease"]

# Convert text → numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X_text)

# Train model
model = LogisticRegression(max_iter=2000)
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully ✅")