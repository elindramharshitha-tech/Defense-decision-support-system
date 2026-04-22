from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict_risk

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = [
        data["threat_level"],
        data["sensor_activity"],
        data["communication_anomaly"],
        data["satellite_alert"]
    ]

    risk = predict_risk(features)

    return jsonify({
        "risk_level": risk,
        "decision": decision_support(risk)
    })

def decision_support(risk):
    if risk == "High":
        return "Immediate action required: deploy surveillance and defense units"
    elif risk == "Medium":
        return "Increase monitoring and verify intelligence inputs"
    else:
        return "Low risk: maintain standard defense operations"

if __name__ == "__main__":
    app.run(debug=True)
