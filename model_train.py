import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Fake training dataset
data = {
    "gst_revenue": [10, 15, 5, 20, 8, 12, 25, 7],
    "bank_inflow": [9, 14, 3, 18, 5, 10, 24, 4],
    "litigation_flag": [0, 0, 1, 0, 1, 0, 0, 1],
    "capacity_percent": [80, 75, 40, 85, 45, 60, 90, 30],
    "approved": [1, 1, 0, 1, 0, 1, 1, 0]
}

df = pd.DataFrame(data)

X = df[["gst_revenue", "bank_inflow", "litigation_flag", "capacity_percent"]]
y = df["approved"]

model = LogisticRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("credit_model.pkl", "wb"))

print("Model trained and saved as credit_model.pkl")