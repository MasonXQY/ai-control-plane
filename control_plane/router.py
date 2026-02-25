import asyncio
from .agents import KimiAgent, ClaudeAgent
from .observability import observability
from .cost_model import estimate_cost

class Router:

    def __init__(self):
        self.kimi = KimiAgent()
        self.opus = ClaudeAgent("claude-opus-4-6")
        self.sonnet = ClaudeAgent("claude-sonnet-4-6")

    def classify(self, prompt):
        length = len(prompt.split())

        if length > 80:
            return "opus"
        elif length < 15:
            return "sonnet"
        else:
            return "kimi"

    async def single_route(self, model, prompt):
        request_id, start = observability.start()

        if model == "kimi":
            result = await self.kimi.run(prompt)
        elif model == "opus":
            result = await self.opus.run(prompt)
        elif model == "sonnet":
            result = await self.sonnet.run(prompt)
        else:
            raise ValueError("Unknown model")

        latency = observability.record(model, start)
        cost = estimate_cost(model, len(result.split()))

        return {
            "model": model,
            "latency_ms": latency,
            "estimated_cost": cost,
            "output": result
        }

    async def ensemble(self, prompt):
        tasks = {
            "kimi": asyncio.create_task(self.kimi.run(prompt)),
            "opus": asyncio.create_task(self.opus.run(prompt)),
            "sonnet": asyncio.create_task(self.sonnet.run(prompt))
        }

        results = {}
        for name, task in tasks.items():
            try:
                results[name] = await task
            except Exception as e:
                results[name] = f"ERROR: {e}"

        best_model = max(results, key=lambda m: len(results[m]))

        return {
            "selected_model": best_model,
            "response": results[best_model],
            "all_responses": results
        }

    async def auto(self, prompt):
        model = self.classify(prompt)
        return await self.single_route(model, prompt)
