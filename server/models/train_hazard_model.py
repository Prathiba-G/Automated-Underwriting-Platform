import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load labeled training data
df = pd.read_csv("data/hazard_training_data.csv")  # Columns: description, hazard_1, hazard_2, ...

# Features and labels
X = df["description"]
y = df.drop(columns=["description"])  # Multi-label hazards

# Vectorize text
vectorizer = TfidfVectorizer(max_features=1000)
X_vec = vectorizer.fit_transform(X)

# Train multi-label classifier
model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
model.fit(X_vec, y)

# Save model and vectorizer
joblib.dump(model, "server/models/hazard_detector/hazard_model.pkl")
joblib.dump(vectorizer, "server/models/hazard_detector/vectorizer.pkl")

print("✅ Hazard detection model trained and saved.")
