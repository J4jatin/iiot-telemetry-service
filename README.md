Production target: AWS (ECS/IoT Core) · TimescaleDB (Postgres) for time-series · Redis for hot-path caching. Runs locally on SQLite + Mosquitto for zero-setup demo.

# IIoT Telemetry Ingestion Service

A backend microservice that ingests **industrial sensor telemetry over MQTT**, validates and
classifies it for anomalies, persists it, and exposes **health and metrics REST endpoints**.
Built to mirror a real Industrial-IoT (IIoT) backend/infrastructure pipeline.

**Stack:** Python · FastAPI · Pydantic · MQTT (paho / Eclipse Mosquitto) · SQLite · Docker · docker-compose · pytest · GitHub Actions CI

---

## Why this project

Industrial machines emit continuous sensor streams (temperature, vibration, pressure, humidity).
A robust IIoT backend must **ingest** those streams reliably, **validate** them, **flag anomalies**,
**store** them, and stay **observable**. This service implements that pipeline end to end as a small,
container-ready system.

## Architecture

```
 Industrial sensors (simulated)
            |  publish JSON
            v
   MQTT broker (Mosquitto)   topic: factory/<machine>/sensors/<metric>
            |  subscribe
            v
   TelemetryConsumer (paho-mqtt)
            |
            v
   Validation + threshold classification  (Pydantic + processor)
            |
            +--> SQLite storage
            +--> in-memory metrics
            ^
            |  query
   FastAPI REST API  -->  /health  /metrics  /readings/recent
```

## Components

| Module | Responsibility |
|---|---|
| `app/models.py` | Pydantic schemas + enums (validation of incoming readings) |
| `app/processor.py` | Threshold-based normal/warning/critical classification |
| `app/storage.py` | SQLite persistence layer |
| `app/metrics.py` | Thread-safe pipeline metrics |
| `app/mqtt_client.py` | MQTT subscriber -> process -> store -> metrics |
| `app/main.py` | FastAPI app (health / metrics / recent readings) |
| `simulator/publisher.py` | Publishes simulated factory sensor data |

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Service info |
| GET | `/health` | Health check + stored reading count |
| GET | `/metrics` | Messages received, invalid, anomalies, by severity |
| GET | `/readings/recent?limit=N` | Most recent processed readings |

## Run the whole system (Docker)

```bash
docker compose up --build
```

This starts the **Mosquitto broker**, the **API** (http://localhost:8000/docs), and the
**simulator** publishing live sensor data. Watch readings flow:

```bash
curl http://localhost:8000/metrics
curl http://localhost:8000/readings/recent
```

## Run locally (without Docker)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# terminal 1 - start a broker (or use Docker for just mosquitto)
docker run -p 1883:1883 eclipse-mosquitto:2

# terminal 2 - API
uvicorn app.main:app --reload

# terminal 3 - simulator
python -m simulator.publisher
```

## Tests

```bash
pip install -r requirements-dev.txt
ruff check .
pytest -v
```

## Author

Jattin Shah — M.Sc. student, TU Dresden — github.com/J4jatin
