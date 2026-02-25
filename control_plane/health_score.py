from .database import get_metrics
from .circuit_breaker import breaker

class HealthScore:

    def evaluate(self):
        metrics = get_metrics()
        scores = {}

        for model, data in metrics.items():

            calls = data.get("calls", 0)
            errors = data.get("total_errors", 0)
            latency = data.get("avg_latency_ms", 0)

            error_rate = (errors / calls) if calls > 0 else 0

            if breaker.is_open(model):
                grade = "D"
            elif error_rate > 0.3:
                grade = "C"
            elif latency > 1500:
                grade = "B"
            else:
                grade = "A"

            scores[model] = {
                "grade": grade,
                "error_rate": round(error_rate, 3),
                "avg_latency_ms": latency
            }

        return scores
