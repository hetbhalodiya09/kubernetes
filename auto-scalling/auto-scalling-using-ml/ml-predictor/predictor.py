import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import start_http_server, Gauge
import requests

app = FastAPI()
model = joblib.load('model/scaling_model.pkl')
prediction_gauge = Gauge('scaling_prediction', 'Predicted replica count')

class MetricsData(BaseModel):
    cpu_usage: float
    memory_usage: float
    requests_per_second: float

def get_prometheus_metrics():
    query = '''
        avg(rate(container_cpu_usage_seconds_total{container="app"}[1m])) * 100,
        avg(container_memory_usage_bytes{container="app"} / 1e6),
        rate(http_requests_total[1m])
    '''
    response = requests.get(
        "http://prometheus:9090/api/v1/query",
        params={"query": query}
    )
    return response.json()["data"]["result"][0]["value"]

@app.post("/predict")
async def predict_scaling(data: MetricsData):
    features = np.array([[data.cpu_usage, data.memory_usage, data.requests_per_second]])
    prediction = model.predict(features)[0]
    prediction_gauge.set(prediction)
    return {"replicas": int(prediction)}

if __name__ == "__main__":
    start_http_server(8001)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)