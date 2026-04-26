# from google import genai
# from config.settings import GEMINI_API_KEY

# client = genai.Client(api_key=GEMINI_API_KEY)

# def get_client():
#     return client
import requests
from config.settings import OPENROUTER_API_KEY, MODEL_NAME

URL = "https://openrouter.ai/api/v1/chat/completions"

def call_model(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",   # required sometimes
        "X-Title": "ai-agent"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(URL, headers=headers, json=data)

    result = response.json()

    # 🔴 print full response for debugging
    print("DEBUG RESPONSE:", result)

    if "choices" not in result:
        raise Exception(f"OpenRouter Error: {result}")

    return result["choices"][0]["message"]["content"]