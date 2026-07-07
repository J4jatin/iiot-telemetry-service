"""FastAPI application exposing health, metrics and recent-reading endpoints."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import config
from app.metrics import metrics
from app.mqtt_client import TelemetryConsumer
from app.storage import Storage

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

storage = Storage(config.DB_PATH)
consumer = TelemetryConsumer(storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if config.MQTT_ENABLED:
        try:
            consumer.start()
            log.info("Telemetry consumer started")
        except Exception as e:  # noqa: BLE001
            log.warning("MQTT consumer not started: %s", e)
    yield
    consumer.stop()


app = FastAPI(
    title="IIoT Telemetry Ingestion Service",
    description="Backend service that ingests industrial sensor telemetry over MQTT, "
    "classifies anomalies, persists readings, and exposes health/metrics endpoints.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"service": "iiot-telemetry-ingestion", "status": "running", "docs": "/docs"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mqtt_enabled": config.MQTT_ENABLED,
        "stored_readings": storage.count(),
    }


@app.get("/metrics")
def get_metrics():
    return metrics.snapshot()


@app.get("/readings/recent")
def recent(limit: int = 20):
    return {"readings": storage.recent(limit)}
