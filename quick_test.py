from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables.")

import requests

api_key = os.getenv("OPENAI_API_KEY")
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get("https://api.openai.com/v1/models", headers=headers)

print(response.status_code, response.json())



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



response = client.chat.completions.create(model="gpt-4o-mini",
messages=[{"role": "user", "content": "Hello, AI!"}])

print(response)
