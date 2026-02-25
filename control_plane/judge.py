from .agents import ClaudeAgent

class Judge:

    def __init__(self):
        self.judge_model = ClaudeAgent("claude-opus-4-6")

    async def evaluate(self, prompt, responses):
        judge_prompt = f"""
You are an expert evaluator.

Task:
{prompt}

Responses:

KIMI:
{responses.get('kimi')}

OPUS:
{responses.get('opus')}

SONNET:
{responses.get('sonnet')}

AZURE:
{responses.get('azure')}

Return ONLY a JSON object like:
{"best": "model_name", "confidence": 0-100}
"""

        verdict = await self.judge_model.run(judge_prompt)

        try:
            import json
            parsed = json.loads(verdict)
            return parsed.get("best"), parsed.get("confidence", 50)
        except:
            # fallback simple heuristic
            return "opus", 50
