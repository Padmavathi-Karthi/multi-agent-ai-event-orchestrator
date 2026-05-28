"""
Smoke Test — verifies Nebius API connectivity before running exercises.
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("NEBIUS_KEY")

if not API_KEY or API_KEY == "sk-your-key-here":
    print("ERROR: NEBIUS_KEY not configured.")
    sys.exit(1)

print("Testing Nebius API connection...")

try:
    client = OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=API_KEY,
    )

    resp = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[{"role": "user", "content": "Reply with exactly: READY"}],
        max_tokens=10,
        temperature=0,
    )

    answer = resp.choices[0].message.content.strip()

    if "READY" in answer.upper():
        print(f"SUCCESS: API OK — {answer}")
        print(f"Model: meta-llama/Llama-3.3-70B-Instruct")
        print(f"Tokens used: {resp.usage.total_tokens}")
    else:
        print(f"WARNING: Unexpected response — {answer}")

except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)