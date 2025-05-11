from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

# Simulate smartwatch data
def simulate_smartwatch_data(num_minutes=120):
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(num_minutes)][::-1]
    heart_rate = np.random.normal(loc=75, scale=5, size=num_minutes).astype(int)
    spo2 = np.random.normal(loc=98, scale=1.0, size=num_minutes).astype(int)
    temperature = np.random.normal(loc=36.6, scale=0.3, size=num_minutes)
    systolic_bp = np.random.normal(loc=120, scale=8, size=num_minutes).astype(int)
    diastolic_bp = np.random.normal(loc=80, scale=4, size=num_minutes).astype(int)

    df = pd.DataFrame({
        'timestamp': timestamps,
        'heart_rate': heart_rate,
        'spo2': spo2,
        'temperature': temperature,
        'systolic_bp': systolic_bp,
        'diastolic_bp': diastolic_bp
    })

    return df

sim_data = simulate_smartwatch_data()

@app.route("/")
def home():
    return "🩺 BP Alert API is running!"

@app.route("/bp_alert", methods=["POST"])
def bp_alert():
    data = request.get_json()
    user_sys = data.get("systolic_bp")
    user_dia = data.get("diastolic_bp")

    hist = sim_data.tail(10)
    mean_sys = hist["systolic_bp"].mean()
    mean_dia = hist["diastolic_bp"].mean()

    dev_sys = abs(user_sys - mean_sys) / (mean_sys + 1e-5)
    dev_dia = abs(user_dia - mean_dia) / (mean_dia + 1e-5)

    alert = dev_sys > 0.15 or dev_dia > 0.15
    result = {
        "mean_systolic": round(mean_sys, 2),
        "mean_diastolic": round(mean_dia, 2),
        "systolic_deviation": round(dev_sys * 100, 2),
        "diastolic_deviation": round(dev_dia * 100, 2),
        "alert": alert
    }

    return jsonify(result)
