import time
import uuid

class Observability:

    def __init__(self):
        self.stats = {}

    def start(self):
        return str(uuid.uuid4()), time.time()

    def record(self, model, start_time):
        latency = (time.time() - start_time) * 1000

        if model not in self.stats:
            self.stats[model] = []

        self.stats[model].append(latency)

        return latency

    def metrics(self):
        return {
            model: {
                "calls": len(values),
                "avg_latency_ms": round(sum(values)/len(values), 2)
            }
            for model, values in self.stats.items()
        }

observability = Observability()
