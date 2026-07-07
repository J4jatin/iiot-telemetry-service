"""Pydantic schemas for industrial sensor telemetry."""
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class Metric(str, Enum):
    temperature = "temperature"
    vibration = "vibration"
    pressure = "pressure"
    humidity = "humidity"


class Severity(str, Enum):
    normal = "normal"
    warning = "warning"
    critical = "critical"


class SensorReading(BaseModel):
    """A single reading published by an industrial sensor."""

    sensor_id: str
    machine_id: str
    metric: Metric
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProcessedReading(BaseModel):
    """A reading after validation and severity classification."""

    sensor_id: str
    machine_id: str
    metric: Metric
    value: float
    unit: str
    timestamp: datetime
    severity: Severity
    reason: str | None = None
