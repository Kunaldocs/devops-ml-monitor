import os
import time
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
from flask import Flask, jsonify, request
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from modeling import train_model

app = Flask(__name__)
PREDICTIONS = Counter("prediction_requests_total", "Number of prediction requests")
HTTP_REQUESTS = Counter("http_requests_total", "Number of HTTP requests handled by the demo API")
APP_STARTED = time.time()
UPTIME = Gauge("application_uptime_seconds", "Seconds since application process started")
MODEL_PATH = Path(os.getenv("MODEL_PATH", "/models/model.joblib"))
TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5001")


def initialize_model():
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment("DevOps ML Monitor")
    model, params, metrics = train_model()
    with mlflow.start_run(run_name="startup-training") as run:
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.set_tag("purpose", "university-devops-lab")
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="DevOpsDemoModel"
        )
        mlflow.set_tag("run_id", run.info.run_id)
    joblib.dump(model, MODEL_PATH)
    return model, metrics


# MLflow must be healthy before the API starts (Compose dependency).
model, training_metrics = initialize_model()


@app.before_request
def count_request():
    HTTP_REQUESTS.inc()
    UPTIME.set(time.time() - APP_STARTED)


@app.get("/")
def index():
    return jsonify({
        "name": "DevOps ML Monitor API",
        "status": "ready",
        "model": "DevOpsDemoModel",
        "training_accuracy": round(training_metrics["accuracy"], 4),
        "endpoints": ["/health", "/predict", "/metrics"]
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy", "model_loaded": MODEL_PATH.exists()}), 200


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    features = payload.get("features")
    if not isinstance(features, list) or len(features) != 4:
        return jsonify({"error": "Send JSON with exactly four numeric features in 'features'."}), 400
    try:
        row = [float(value) for value in features]
    except (TypeError, ValueError):
        return jsonify({"error": "All features must be numeric."}), 400
    prediction = int(model.predict([row])[0])
    PREDICTIONS.inc()
    return jsonify({
        "prediction": prediction,
        "class_name": ["setosa", "versicolor", "virginica"][prediction],
        "demo_only": True
    })


@app.get("/metrics")
def metrics():
    UPTIME.set(time.time() - APP_STARTED)
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
