import os
from dotenv import load_dotenv

load_dotenv()

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = "gemini-2.0-flash"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "meta-llama/llama-3-8b-instruct"