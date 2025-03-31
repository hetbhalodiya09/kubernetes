# ml-predictor/train_model.py
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import joblib

# Generate sample training data (replace with your real metrics)
# Format: [CPU Usage (%), Memory Usage (MB), Requests per Second]
X = np.array([
    [30, 512, 50],
    [60, 1024, 100],
    [90, 2048, 200],
    # Add more samples...
])

# Target: Optimal replica count
y = np.array([2, 3, 5])  # Corresponding replica counts

# Train model
model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

# Save model
joblib.dump(model, 'model/scaling_model.pkl')
print("Model saved to ml-predictor/model/scaling_model.pkl")