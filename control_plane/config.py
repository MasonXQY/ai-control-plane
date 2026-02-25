import os
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("AZURE_API_KEY")

if not KEY:
    raise ValueError("AZURE_API_KEY not found in environment")

KIMI_URL = "https://internal-automation-swe-ai-res.services.ai.azure.com/openai/v1/chat/completions"
CLAUDE_URL = "https://internal-automation-swe-ai-res.openai.azure.com/anthropic/v1/messages"
