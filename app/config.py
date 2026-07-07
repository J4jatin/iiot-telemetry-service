"""Configuration loaded from environment variables."""
import os

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "factory/+/sensors/#")
MQTT_ENABLED = os.getenv("MQTT_ENABLED", "true").lower() == "true"
DB_PATH = os.getenv("DB_PATH", "telemetry.db")
