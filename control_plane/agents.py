import httpx
from .config import KEY, KIMI_URL, CLAUDE_URL

class KimiAgent:

    async def run(self, prompt):
        headers = {
            "Content-Type": "application/json",
            "api-key": KEY
        }
        body = {
            "model": "Kimi-K2.5",
            "messages": [{"role": "user", "content": prompt}]
        }

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(KIMI_URL, headers=headers, json=body)

        if r.status_code != 200:
            raise Exception(f"Kimi Error {r.status_code}: {r.text}")

        return r.json()["choices"][0]["message"]["content"]


class ClaudeAgent:

    def __init__(self, model):
        self.model = model

    async def run(self, prompt):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {KEY}",
            "anthropic-version": "2023-06-01"
        }
        body = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(CLAUDE_URL, headers=headers, json=body)

        if r.status_code != 200:
            raise Exception(f"Claude Error {r.status_code}: {r.text}")

        return r.json()["content"][0]["text"]
