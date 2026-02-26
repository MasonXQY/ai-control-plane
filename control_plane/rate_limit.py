import time

RATE_LIMIT = 60  # 60 requests per minute

class RateLimiter:

    def __init__(self):
        self.calls = {}

    def check(self, api_key):
        now = time.time()

        if api_key not in self.calls:
            self.calls[api_key] = []

        # Remove calls older than 60 seconds
        self.calls[api_key] = [
            t for t in self.calls[api_key]
            if now - t < 60
        ]

        if len(self.calls[api_key]) >= RATE_LIMIT:
            return False

        self.calls[api_key].append(now)
        return True

rate_limiter = RateLimiter()
