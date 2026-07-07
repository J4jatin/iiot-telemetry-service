"""Thread-safe in-memory metrics for the ingestion pipeline."""
from collections import Counter
from threading import Lock


class Metrics:
    def __init__(self):
        self._lock = Lock()
        self.messages_received = 0
        self.invalid_messages = 0
        self.by_severity: Counter = Counter()

    def record(self, severity: str):
        with self._lock:
            self.messages_received += 1
            self.by_severity[severity] += 1

    def record_invalid(self):
        with self._lock:
            self.invalid_messages += 1

    def snapshot(self) -> dict:
        with self._lock:
            anomalies = self.by_severity.get("warning", 0) + self.by_severity.get("critical", 0)
            return {
                "messages_received": self.messages_received,
                "invalid_messages": self.invalid_messages,
                "anomalies_detected": anomalies,
                "by_severity": dict(self.by_severity),
            }


metrics = Metrics()
