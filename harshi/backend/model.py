import joblib

# Load trained model
model = joblib.load("defense_model.pkl")

def predict_risk(features):
    prediction = model.predict([features])
    return prediction[0]
