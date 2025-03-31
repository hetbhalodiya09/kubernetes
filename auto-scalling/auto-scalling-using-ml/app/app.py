from fastapi import FastAPI
from prometheus_client import make_asgi_app, Counter, Histogram

app = FastAPI()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

RESPONSE_TIME = Histogram(
    'http_response_time_seconds',
    'Response time in seconds',
    ['method', 'endpoint']
)

@app.get("/")
async def root():
    with RESPONSE_TIME.labels("GET", "/").time():
        REQUEST_COUNT.labels("GET", "/", 200).inc()
        return {"message": "Hello World"}