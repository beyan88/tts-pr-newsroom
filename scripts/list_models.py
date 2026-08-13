import os
import sys

try:
    from google import genai
except ImportError:
    print("Error: google-genai is not installed.")
    sys.exit(1)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY is not set.")
    sys.exit(1)
client = genai.Client(api_key=api_key)

print("Listing available models:")
try:
    for model in client.models.list():
        if "image" in model.name.lower() or "gemini" in model.name.lower() or "banana" in model.name.lower():
            print(f"Model Name: {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
