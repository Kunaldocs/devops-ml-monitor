FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
ENV MODEL_PATH=/models/model.joblib \
    MLFLOW_TRACKING_URI=http://mlflow:5000

RUN mkdir -p /models
EXPOSE 5000
CMD ["python", "app/main.py"]
