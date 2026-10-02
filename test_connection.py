import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

nebius_key = os.getenv("NEBIUS_API_KEY")
nebius_base_url = os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1")
tavily_key = os.getenv("TAVILY_API_KEY")

print(f"Loaded .env from: {env_path}")
print(f"Nebius Key detected: {'YES' if nebius_key else 'NO (Missing)'}")
print(f"Tavily Key detected: {'YES' if tavily_key else 'NO (Missing)'}")

if not nebius_key:
    raise ValueError("NEBIUS_API_KEY is missing or empty in your .env file.")

# 1. Test Nebius connection
print("\n--- Testing Nebius Token Factory Connection ---")
client = OpenAI(
    base_url=nebius_base_url,
    api_key=nebius_key,
)

response = client.chat.completions.create(
    model="nvidia/nemotron-3-super-120b-a12b",
    messages=[{"role": "user", "content": "Respond with: SENTRY online."}],
    temperature=0.2,
)
print("Model Output:", response.choices[0].message.content)

# 2. Test Tavily connection
print("\n--- Testing Tavily Search Connection ---")
if not tavily_key:
    print("Tavily test skipped (TAVILY_API_KEY missing).")
else:
    tavily = TavilyClient(api_key=tavily_key)
    search_result = tavily.search(query="Supabase pricing tiers", max_results=1)
    print("Search Output Title:", search_result["results"][0]["title"])