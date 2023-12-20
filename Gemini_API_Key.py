import os

def get_gemini_api_key() -> str:
    return os.environ.get("Gemini_API_Key", None)
