# app/utils.py
import os
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")

async def call_openrouter(prompt: str, *, timeout: int = 60):
    """
    Call OpenRouter chat completion API and return assistant content text.
    Uses aiohttp for async requests.
    """
    if not OPENROUTER_API_KEY:
        return "[OpenRouter API key missing: set OPENROUTER_API_KEY in env]"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 800,
    }

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.post(OPENROUTER_URL, json=payload, headers=headers) as resp:
                body_text = await resp.text()
                try:
                    data = await resp.json()
                except Exception:
                    return f"[OpenRouter returned non-json response: status={resp.status}] {body_text}"

                try:
                    return data["choices"][0]["message"]["content"].strip()
                except Exception:
                    return f"[OpenRouter unexpected response structure] status={resp.status} body={data}"
    except asyncio.TimeoutError:
        return "[OpenRouter request timed out]"
    except Exception as e:
        return f"[OpenRouter call failed] {repr(e)}"
